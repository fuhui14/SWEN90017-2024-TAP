from celery import shared_task
from emails.send_email import send_email, FileType
from .models import Transcription

@shared_task
def process_transcription_and_send_email(transcription_id):
    """
    Celery task: Sends transcription results via email when processing is done.
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
