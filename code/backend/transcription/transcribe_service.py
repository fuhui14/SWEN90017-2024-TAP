import whisper

# Load the Whisper model once during app startup
model = whisper.load_model("base")

def transcribe_audio(audio_path):
    """
    Transcribes the given audio file using the Whisper model.
    """
    print('xxxxx: ' + audio_path)
    try:
        result = model.transcribe(audio_path)
        return result
    except FileNotFoundError as fnf_error:
        print(f"File not found error during transcription: {fnf_error}")
        raise
    except Exception as e:
        print(f"General error during transcription: {e}")
        raise