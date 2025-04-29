from emails.send_email import send_email, FileType
from .models import Transcription

from django.utils import timezone
import datetime
from .models import File

def process_transcription_and_send_email(transcription_id, portal_link=None, file_type=FileType.TXT):
    """
    Function: Sends transcription results via email when processing is done.
    """
    try:
        transcription = Transcription.objects.get(id=transcription_id)
        email = transcription.file.email  # Get user email
        transcription_text = transcription.transcribed_text

        # Compose email body with optional portal link
        body = "Here is your transcription result.\n\n"
        if portal_link:
            body += f"You can view all your transcription history here:\n{portal_link}\n\n"
        body += "Best regards,\nTranscription Aide Platform"

        content = f"{transcription_text}\n\nYou can view all your transcriptions at: {portal_link}"
        send_email(email, "Your Transcription Result", content, transcription_text, file_type)

        return f"Transcription result sent to {email}"

    except Transcription.DoesNotExist:
        return f"Transcription {transcription_id} not found"

def cleanup_expired_files():
    # 计算三个月（90 天）之前的时间点
    expiration_date = timezone.now() - datetime.timedelta(days=90)
    # 查询并删除过期文件
    expired_files = File.objects.filter(upload_timestamp__lt=expiration_date)
    count = expired_files.count()
    expired_files.delete()
    return f"成功删除了 {count} 个过期文件。"
