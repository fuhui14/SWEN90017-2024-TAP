import whisper

# Load the Whisper model once during app startup
model = whisper.load_model("base")

def transcribe_audio(audio_path):
    """
    Transcribes the given audio file using the Whisper model.
    """
    result = model.transcribe(audio_path)
    return result['text']
