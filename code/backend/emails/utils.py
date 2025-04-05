from emails.send_email import send_email, FileType

def send_error_report_email(receiver, error_message):
    subject = "Transcription Failed"
    content = f"An error occurred during transcription: {error_message}"
    send_email(
        receiver=receiver,
        subject=subject,
        content=content,
        file_content="",
        file_type=FileType.NONE
    )
