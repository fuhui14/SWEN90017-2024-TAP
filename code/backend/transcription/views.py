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

from speaker_identify.assign_speaker_service import assign_speakers_to_transcription
from speaker_identify.pyannote_transcrip_speaker import pyannote_transcrip_speaker
from .forms import UploadFileForm
from .models import File, Transcription
from .tasks import process_transcription_and_send_email
from emails.send_email import send_email, FileType

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
                # transcribe the audio file
                # transcription = transcribe_audio(file_path)
                # transcription_with_speaker = assign_speakers_to_transcription(transcription,
                #                                                               file_path)
                transcription_with_speaker = pyannote_transcrip_speaker(file_path)
                print(f"Transcription result: {transcription_with_speaker}")

                transcribed_data = Transcription.objects.create(
                    file=db_file,
                    transcribed_text=transcription_with_speaker
                )
                print("Transcription saved in database")

                # Synchronously trigger email notification
                process_transcription_and_send_email(transcribed_data.id)

            except Exception as e:
                print(f"Error during transcription or saving transcription for file {file_path}: {e}")
                send_email(
                    receiver=email,
                    subject="Transcription Failed",
                    content=f"An error occurred during transcription: {str(e)}",
                    file_content="",
                    file_type=FileType.NONE
                )
                return JsonResponse({'error': f'Transcription error: {str(e)}'}, status=500)

            # return the transcription result
            print("Returning transcription result")
            return JsonResponse({"transcription": transcription_with_speaker}, safe=False)

        else:
            print("Form is not valid")
            errors = form.errors.as_json()
            print(f"Form errors: {errors}")
            return JsonResponse({'error': f'Invalid form submission: {errors}'}, status=400)

    else:
        print("GET request received; rendering form")
        form = UploadFileForm()
    return render(request, 'index.html', {'form': form})

def transcribe_audio(audio_path):
    print('Transcribing audio file at path: ' + audio_path)
    try:
        system_platform = platform.system()
        # if the system is Windows, convert the path to a raw string
        if system_platform == 'Windows':
            audio_path = r'{}'.format(audio_path)
            print('Path:::' + audio_path)

        result = model.transcribe(audio_path)
        return result
    except FileNotFoundError as fnf_error:
        print(f"File not found error during transcription: {fnf_error}")
        raise
    except Exception as e:
        print(f"General error during transcription: {e}")
        raise