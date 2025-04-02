from emails.send_email import send_email, FileType
from .models import Transcription

from django.utils import timezone
import datetime
from .models import File
from celery import shared_task

import redis
from django.conf import settings
from speaker_identify.identify_service import transcribe_with_speaker
import platform

from emails.utils import send_error_report_email

def process_transcription_and_send_email(transcription_id):
    """
    Function: Sends transcription results via email when processing is done.
    """
    try:

        transcription = Transcription.objects.get(id=transcription_id)
        email = transcription.file.email  # Get user email
        transcription_text = transcription.transcribed_text
        file_path = transcription.file.storage_path  # Path to the saved audio file

        # Choose file format (TXT, DOCX, or PDF)
        file_type = FileType.TXT  # Change if needed

        # Send the email
        send_email(email, "Your Transcription Result", transcription_text, transcription_text, file_type)
        print("Email sent successfully")

        return f"Transcription result sent to {email}"

    except Transcription.DoesNotExist:
        return f"Transcription {transcription_id} not found"
@shared_task
def cleanup_expired_files():
    # 计算三个月（90 天）之前的时间点
    expiration_date = timezone.now() - datetime.timedelta(days=90)
    # 查询并删除过期文件
    expired_files = File.objects.filter(upload_timestamp__lt=expiration_date)
    count = expired_files.count()
    expired_files.delete()
    return f"成功删除了 {count} 个过期文件。"

def transcribe_audio(audio_path, model):
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

@shared_task(bind=True)
def process_file(self, db_file_id, file_path):
    task_id = self.request.id
    print(f"[{task_id}] Redis URL: {settings.CELERY_BROKER_URL}")
    r = redis.from_url(settings.CELERY_BROKER_URL)
    db_file = File.objects.get(id=db_file_id)
    email = db_file.email
    # transcribe the audio file
    try:
        transcription_with_speaker = transcribe_with_speaker(file_path)

        transcribed_data = Transcription.objects.create(
            file=db_file,
            transcribed_text=transcription_with_speaker
        )
        print("Transcription saved in database")

        # Trigger email notification asynchronously
        process_transcription_and_send_email(transcribed_data.id)
    except FileNotFoundError as fnf_error:
        print(f"File not found during transcription: {fnf_error}")
        send_error_report_email(email, str(e))
    except Exception as e:
        print(f"Error during transcription {file_path}: {e}")
        send_error_report_email(email, str(e))
    finally:
        r.lrem("user_task_queue", 0, task_id)
