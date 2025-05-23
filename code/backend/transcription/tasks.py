from emails.send_email import send_email, FileType
from .models import Transcription

from django.utils import timezone
import datetime
from .models import File

def process_transcription_and_send_email(transcription_id, portal_link=None, file_type=FileType.TXT, language="en"):
    """
    Function: Sends transcription results via email when processing is done.
    """
    try:
        transcription = Transcription.objects.get(id=transcription_id)
        email = transcription.file.email  # Get user email
        transcription_text = transcription.transcribed_text

        # Compose email body
        body = "Here is your transcription result.\n\n"
        body += "Best regards,\nTranscription Aide Platform"

        send_email(
            receiver=email,
            subject="Your Transcription Result",
            content=body,
            file_content=transcription_text,
            file_type=file_type
        )

        return f"Transcription result sent to {email}"

    except Transcription.DoesNotExist:
        return f"Transcription {transcription_id} not found"

def cleanup_expired_files():
    # Calculate the timestamp from 90 days (3 months) ago
    expiration_date = timezone.now() - datetime.timedelta(days=90)
    # Query and delete expired files
    expired_files = File.objects.filter(upload_timestamp__lt=expiration_date)
    count = expired_files.count()
    expired_files.delete()
    return f"Successfully deleted {count} expired files."
