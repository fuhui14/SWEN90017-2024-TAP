import torch
import os
from speechbox import ASRDiarizationPipeline
from speechbox.diarize import ASRDiarizationPipeline
from datasets import load_dataset
from dotenv import load_dotenv
from pydub import AudioSegment



def pyannote_transcrip_speaker(audioPath):

    # device = "cuda:0" if torch.cuda.is_available() else "cpu"
    # device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
    if torch.cuda.is_available():
        device = torch.device("cuda:0")
    elif torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")

    load_dotenv()  # automatically load variables from .env file
    hf_token = os.environ.get("HF_TOKEN")

    pipeline = ASRDiarizationPipeline.from_pretrained("openai/whisper-tiny", device=device, use_auth_token=hf_token)

    audioPath = convert_to_wav(audioPath)
    transcription = pipeline(audioPath);

    return transcription


def convert_to_wav(file_path):
    try:
        file_name = os.path.splitext(file_path)[0]
        output_file = f"{file_name}.wav"
        audio = AudioSegment.from_file(file_path)
        audio.export(output_file, format="wav")
        return output_file
    except Exception as e:
        print(e)
        return None