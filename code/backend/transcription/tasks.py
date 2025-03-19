from celery import shared_task
from emails.send_email import send_email, FileType
from .models import Transcription

from django.utils import timezone
import datetime
from .models import File

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
