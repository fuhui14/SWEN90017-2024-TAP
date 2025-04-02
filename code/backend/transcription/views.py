import os
import uuid
import platform
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pathlib import Path
import shutil
import whisper

from speaker_identify.identify_service import transcribe_with_speaker
from .forms import UploadFileForm
from .models import File, Transcription
from .tasks import process_transcription_and_send_email
from emails.send_email import send_email, FileType
from emails.utils import send_error_report_email

import redis
from .tasks import process_file

# load whisper model when the server starts
model = whisper.load_model("base")

transcribe_queue_max = 5
r = redis.from_url(settings.CELERY_BROKER_URL)

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

            # save the uploaded file 
            file = request.FILES['file']

            # generate a unique ID for the upload
            upload_id = uuid.uuid4() 
            original_filename = file.name
            print(f"Original filename: {original_filename}, Upload ID: {upload_id}")

            # generate the storage path for the file
            # use at and dot instead of @ and . in the email address
            sanitized_email = email.replace('@', '_at_').replace('.', '_dot_')
            storage_dir = os.path.join(settings.MEDIA_ROOT, 'uploads', sanitized_email, upload_id.hex)
            try:
                os.makedirs(storage_dir, exist_ok=True)
            except OSError as e:
                print(f"Error creating directory: {e}")
                return JsonResponse({'error': f'Unable to create storage directory: {str(e)}'}, status=500)

            # get the full path to save the file
            file_path = os.path.join(storage_dir, original_filename)
            print(f"Storage directory: {storage_dir}, File path: {file_path}")
            
            # check if the queue is full
            if is_queue_overloaded():
                print("Queue is full")
                return JsonResponse({'error': 'Queue is full'}, status=503)
            
            # check if the file is already in the queue
            task_id = form.cleaned_data.get('taskid')
            if is_task_in_queue(task_id):
                print(f"Task {task_id} already in queue")
                return JsonResponse({'error': 'Task already in queue'}, status=400)

            try:
                with open(file_path, 'wb') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                print("File saved successfully")
            except Exception as e:
                print(f"Error saving file: {e}")
                return JsonResponse({'error': f'Error saving file: {str(e)}'}, status=500)

            # check if the file exists
            if not os.path.exists(file_path):
                print(f"File does not exist after saving: {file_path}")
                return JsonResponse({'error': f'File not found after saving: {file_path}'}, status=500)

            # save the file metadata to the database
            try:
                db_file = File.objects.create(
                    email=email,
                    upload_id=upload_id,
                    original_filename=original_filename,
                    storage_path=file_path,
                    file_size=file.size,
                    status='uploaded'
                )
                print(f"File metadata saved in database with ID: {db_file.id}")
            except Exception as e:
                print("Error saving file metadata to the database:", e)
                return JsonResponse({'error': f'Database error: Unable to save file metadata: {str(e)}'}, status=500)

            # transcribe the audio file
            try:
                print(f"Starting transcription for file: {file_path}")
                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"The file at {file_path} does not exist")

                task = process_file.delay(db_file.id, file_path)
                
                r.rpush("user_task_queue", task.id)

            except Exception as e:
                print(f"Error during transcription or saving transcription for file {file_path}: {e}")
                send_error_report_email(email, str(e))
                return JsonResponse({'error': f'Transcription error: {str(e)}'}, status=500)

            return JsonResponse({"task_id": task.id})

        else:
            print("Form is not valid")
            errors = form.errors.as_json()
            print(f"Form errors: {errors}")
            return JsonResponse({'error': f'Invalid form submission: {errors}'}, status=400)

    else:
        print("GET request received; rendering form")
        form = UploadFileForm()
    return render(request, 'index.html', {'form': form})

# def transcribe_audio(audio_path):
#     print('Transcribing audio file at path: ' + audio_path)
#     try:
#         system_platform = platform.system()
#         # if the system is Windows, convert the path to a raw string
#         if system_platform == 'Windows':
#             audio_path = r'{}'.format(audio_path)
#             print('Path:::' + audio_path)

#         result = model.transcribe(audio_path)
#         return result
#     except FileNotFoundError as fnf_error:
#         print(f"File not found error during transcription: {fnf_error}")
#         raise
#     except Exception as e:
#         print(f"General error during transcription: {e}")
#         raise


def get_task_queue():
    queue = r.lrange("user_task_queue", 0, -1)
    return [t.decode() for t in queue]


def is_task_in_queue(task_id: str) -> bool:
    return task_id in get_task_queue()


def get_task_position(task_id: str) -> int | None:
    queue = get_task_queue()
    try:
        return queue.index(task_id)
    except ValueError:
        return None


def get_queue_position(request):
    task_id = request.GET.get("task_id")
    if not task_id:
        return JsonResponse({"error": "task_id required"})

    pos = get_task_position(task_id)
    if pos is None:
        return JsonResponse({"task_id": task_id, "position": "任务已完成或不存在"})
    return JsonResponse({"task_id": task_id, "position": pos})


def is_queue_overloaded(queue_name="user_task_queue"):
    r = redis.from_url(settings.CELERY_BROKER_URL)
    length = r.llen(queue_name)
    return length > transcribe_queue_max