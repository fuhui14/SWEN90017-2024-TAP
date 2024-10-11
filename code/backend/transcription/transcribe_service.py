from .celery import app
import os
import uuid
from core.models import db, Transcription
import datetime
import whisper

# Load the Whisper model once during app startup
model = whisper.load_model("base")

@app.task
def handle_file_upload(file_id, file_path):
    try:
        # use whisper model to transcribe the audio
        result = model.transcribe(file_path)

        # update the transcription result in the database
        transcription = Transcription.query.filter_by(file_id=file_id).first()
        if transcription:
            transcription.transcription_text = result['text']
            transcription.status = "Completed"
            db.session.commit()
        return {"success": True}
    except Exception as e:
        # update the transcription status as failed
        transcription = Transcription.query.filter_by(file_id=file_id).first()
        if transcription:
            transcription.status = "Failed"
            db.session.commit()
        return {"success": False, "error": str(e)}
