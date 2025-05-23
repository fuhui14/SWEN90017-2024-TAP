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

def format_transcription_content(transcription_data):
    """
    Format structured transcription data (list of dicts) into readable string.
    Remove timestamps and preserve only speaker and text.
    """
    if isinstance(transcription_data, str):
        try:
            import ast
            transcription_data = ast.literal_eval(transcription_data)
        except Exception:
            return transcription_data  # fallback to raw text

    if not isinstance(transcription_data, list):
        return str(transcription_data)

    lines = []
    for segment in transcription_data:
        speaker = segment.get("speaker", 0)  # use as-is (0-based)
        text = segment.get("text", "")
        lines.append(f"Speaker {speaker}: {text}")

    return "\n\n".join(lines)
