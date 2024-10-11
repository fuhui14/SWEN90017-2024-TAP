import os
import uuid
from core.models import db, Transcription
import datetime
import whisper

# Load the Whisper model once during app startup
model = whisper.load_model("base")

def handle_file_upload(file_path):
    try:
        # use whisper model to transcribe the audio
        result = model.transcribe(file_path)

        # create the unique file ID
        file_id = str(uuid.uuid4())
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(days=30)

        # save the transcription result to db
        transcription = Transcription(
            file_id=file_id,
            file_name=os.path.basename(file_path),
            transcription_text=result['text'],
            status="Completed",
            created_at=datetime.datetime.utcnow(),
            expiration_date=expiration_date
        )
        db.session.add(transcription)
        db.session.commit()

        return {"success": True, "file_id": file_id}
    except Exception as e:
        return {"success": False, "error": str(e)}

