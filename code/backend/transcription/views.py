# transcription/views.py

import os
import uuid
import platform
import json
import time
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.utils import timezone
from datetime import timedelta
from pathlib import Path
import shutil
import whisper
import threading

from speaker_identify.identify_service import transcribe_with_speaker
from .forms import UploadFileForm
from .models import File, Transcription
from .tasks import process_transcription_and_send_email
from emails.send_email import send_email, FileType
from emails.utils import send_error_report_email
from transcription.thread_worker import transcribe_audio_task
from transcription.task_registry import task_status, task_result, task_lock
from transcription.thread_executor import executor

# load whisper model when the server starts
model = whisper.load_model("base")


@csrf_exempt
def transcribe(request):
    print("Received a request to transcribe")
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid")

            # get user email
            email = form.cleaned_data.get('email')
            print(f"User email: {email}")

            # get all uploaded files
            upload_files = request.FILES.getlist('file')
            tasks = []

            # handle outputFormat and portal base URL
            output_format_str = form.cleaned_data.get("outputFormat", "txt").lower()
            portal_base = settings.FRONTEND_BASE_URL

            # loop over each uploaded file
            for uploaded_file in upload_files:
                # 1) generate upload_id and save file to disk
                upload_id = uuid.uuid4()
                original_filename = uploaded_file.name
                print(f"Original filename: {original_filename}, Upload ID: {upload_id}")

                sanitized_email = email.replace('@', '_at_').replace('.', '_dot_')
                storage_dir = os.path.join(
                    settings.MEDIA_ROOT, 'uploads', sanitized_email, upload_id.hex
                )
                os.makedirs(storage_dir, exist_ok=True)
                file_path = os.path.join(storage_dir, original_filename)
                with open(file_path, 'wb') as f:
                    for chunk in uploaded_file.chunks():
                        f.write(chunk)
                print("File saved successfully")

                # 2) save metadata to DB
                db_file = File.objects.create(
                    email=email,
                    upload_id=upload_id,
                    original_filename=original_filename,
                    storage_path=file_path,
                    file_size=uploaded_file.size,
                    status='uploaded'
                )
                print(f"File metadata saved in database with ID: {db_file.id}")

                # 3) enqueue transcription task
                task_id = str(uuid.uuid4())
                print(f"New Task ID: {task_id}")
                portal_link = f"{portal_base}/history?token={db_file.portal_token}"

                with task_lock:
                    task_status[task_id] = "queued"

                executor.submit(
                    transcribe_audio_task,
                    task_id,
                    db_file,
                    file_path,
                    email,
                    output_format_str,
                    portal_link
                )

                # 4) collect info for response
                tasks.append({
                    "task_id": task_id,
                    "filename": original_filename,
                    "upload_id": upload_id.hex
                })

            # return all task entries
            return JsonResponse({"tasks": tasks})

        else:
            print("Form is not valid")
            errors = form.errors.as_json()
            print(f"Form errors: {errors}")
            return JsonResponse({'error': f'Invalid form submission: {errors}'}, status=400)

    # GET → render the upload form
    print("GET request received; rendering form")
    form = UploadFileForm()
    return render(request, 'index.html', {'form': form})


@csrf_exempt
@require_POST
def send_history_portal_link(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        email = data.get("email")
        if not email:
            return JsonResponse({"error": "Email is required."}, status=400)

        latest_file = File.objects.filter(email=email).order_by('-upload_timestamp').first()
        if not latest_file:
            return JsonResponse({"error": "No transcription history found for this email."}, status=404)

        portal_link = f"{settings.FRONTEND_BASE_URL}/history?token={latest_file.portal_token}"
        subject = "Your transcription history link"
        body = (
            f"Hello,\n\n"
            f"You can view your transcription history at the following link:\n"
            f"{portal_link}\n\n"
            f"Best regards,\nTranscription Aide Platform"
        )
        send_email(
            receiver=email,
            subject=subject,
            content=body,
            file_content=None,
            file_type=FileType.NONE
        )
        return JsonResponse({"message": "Portal link sent successfully."})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON."}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_GET
def transcription_history_by_token(request, token):
    try:
        file = File.objects.get(token=token)
    except File.DoesNotExist:
        return JsonResponse({'error': 'Invalid token'}, status=404)

    expiration_threshold = timezone.now() - timedelta(days=90)
    user_files = File.objects.filter(
        email=file.email,
        upload_timestamp__gte=expiration_threshold
    ).order_by('-upload_timestamp')

    history = []
    for f in user_files:
        transcription = Transcription.objects.filter(file=f).first()
        history.append({
            'file_name': f.original_filename,
            'creation_date': f.upload_timestamp.strftime('%Y-%m-%d'),
            'expiration_date': (f.upload_timestamp + timedelta(days=90)).strftime('%Y-%m-%d'),
            'transcription_text': transcription.transcribed_text if transcription else '',
            'download_link': f'/api/download/{f.upload_id}/'
        })
    return JsonResponse({'history': history})


@require_GET
def task_status_view(request, task_id):
    from transcription.task_registry import task_status, task_result

    task_id_str = str(task_id)
    status = task_status.get(task_id_str)
    if status is None:
        return JsonResponse({"status": "not_found"}, status=404)

    if status == "processing":
        progress = task_result.get(task_id_str, 0.0)
        return JsonResponse({"status": "processing", "progress": progress})
    elif status == "completed":
        result = task_result.pop(task_id_str, None)
        if result is None:
            return JsonResponse({"status": "expired", "message": "Result already retrieved."})
        return JsonResponse({"status": "completed", "transcription": result})
    elif status == "error":
        return JsonResponse({"status": "error", "error": task_result.get(task_id_str, "Unknown error")})

    return JsonResponse({"status": status})


@require_GET
def transcription_stream(request):
    task_id = request.GET.get('id')
    if not task_id:
        return JsonResponse({'error': 'Missing id parameter.'}, status=400)

    with task_lock:
        if task_id not in task_status:
            return JsonResponse({'error': 'Invalid id.'}, status=404)

    def event_stream():
        while True:
            with task_lock:
                status_entry = task_status.get(task_id)
                result_entry = task_result.get(task_id)

            if status_entry == "processing":
                pct = task_result.get(task_id, 0.0) * 100
                yield f"data: {json.dumps({'type':'progress','progress': pct})}\n\n"

            elif status_entry == "completed":
                yield f"data: {json.dumps({'type':'result','transcripts': result_entry})}\n\n"
                break

            elif status_entry == "error":
                yield f"data: {json.dumps({'type':'error','message': result_entry})}\n\n"
                break

            time.sleep(0.5)

    return StreamingHttpResponse(
        event_stream(),
        content_type='text/event-stream',
    )
