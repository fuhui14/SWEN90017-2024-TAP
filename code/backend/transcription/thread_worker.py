# transcription/thread_worker.py

import whisper
from .models import Transcription
from emails.utils import send_error_report_email
from .tasks import process_transcription_and_send_email
from .task_registry import task_status, task_result, task_lock
from speaker_identify.transcribe_with_speaker_fasterWhisper import transcribe_with_speaker_fasterWhisper

from translation.translate import translate
from emails.utils import format_transcription_content

# thread worker for transcribing audio
def transcribe_audio_task(task_id, db_file, file_path, email, output_format_str, frontend_link, language):
    print("Start transcribing audio, task_id:", task_id)
    with task_lock:
        task_status[task_id] = "processing"

    try:
         
        # Change: use the fasterWhisper version with task_id support
        transcription_with_speaker = transcribe_with_speaker_fasterWhisper(task_id, file_path)

        # translate the transcription text
        formatted_text = format_transcription_content(transcription_with_speaker)
        translated_text = translate(formatted_text, language)

        # Save transcription result to the database
        transcribed_data = Transcription.objects.create(
            file=db_file,
            transcribed_text=translated_text
        )

        # Determine file type based on the format specified by the frontend
        from emails.send_email import FileType
        if output_format_str == "pdf":
            file_type = FileType.PDF
        elif output_format_str == "docx":
            file_type = FileType.DOCX
        else:
            file_type = FileType.TXT

        # Send transcription result via email
        process_transcription_and_send_email(
            transcribed_data.id,
            portal_link=frontend_link,
            file_type=file_type,
            language=language
        )

        # Mark task as completed and store the final result
        with task_lock:
            task_status[task_id] = "completed"
            task_result[task_id] = translated_text

        print("Transcription completed, task_id:", task_id)

    except Exception as e:
        print("Error in transcribe_audio_task, task_id:", task_id, e)
        with task_lock:
            task_status[task_id] = "error"
            task_result[task_id] = str(e)
        send_error_report_email(email, str(e))
