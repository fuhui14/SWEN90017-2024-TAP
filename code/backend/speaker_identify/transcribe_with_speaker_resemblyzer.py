import whisper
import torch
import os
from resemblyzer import VoiceEncoder, preprocess_wav, sampling_rate
from pathlib import Path
import numpy as np
from pydub import AudioSegment
import noisereduce as nr
from io import BytesIO
from spectralcluster import SpectralClusterer
import subprocess

def transcribe_with_speaker_resemblyzer(audioPath):
    # give the file path to your audio file
    audio_file_path = convert_to_wav(audioPath)
    wav_fpath = Path(audio_file_path)

    wav = preprocess_wav(wav_fpath)

    if torch.cuda.is_available():
        device = "cuda"
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"
    encoder = VoiceEncoder(device)

    _, cont_embeds, wav_splits = encoder.embed_utterance(wav, return_partials=True, rate=16)
    print("Embedding shape:", cont_embeds.shape)

    clusterer = SpectralClusterer(
        min_clusters=2,
        max_clusters=100)
    labels = clusterer.predict(cont_embeds)

    # create labelling
    labelling = create_labelling(labels,wav_splits)

    # start transcribing
    model = whisper.load_model("base")
    transcription = []

    for seg in labelling:
        speaker, seg_start, seg_end = seg
        seg_filename = f"segment_{speaker}_{seg_start:.2f}_{seg_end:.2f}.wav"
        print(f"Processing segment: {seg_filename} ({seg_start:.2f}s - {seg_end:.2f}s)")
        trim_audio(audio_file_path, seg_filename, seg_start, seg_end)
        # use Whisper to transcribe the segment
        result = model.transcribe(seg_filename)
        transcript_text = result["text"].strip()
        # save the transcript
        transcription.append({
            "speaker": speaker,
            "text": transcript_text,
            "start": seg_start,
            "end": seg_end
        })

    print("Final Transcription:\n", transcription)

    #remove the temporary segment files
    for seg in labelling:
        speaker, seg_start, seg_end = seg
        seg_filename = f"segment_{speaker}_{seg_start:.2f}_{seg_end:.2f}.wav"
        if Path(seg_filename).exists():
            Path(seg_filename).unlink()
        print(f"Deleted temporary file: {seg_filename}")
    
    # remove the original wav file
    if wav_fpath.exists():
        wav_fpath.unlink()
        print(f"Deleted original file: {wav_fpath}")

    # remove the original audio file
    audioPath = Path(audioPath)
    if audioPath.exists():
        audioPath.unlink()
        print(f"Deleted original file: {audioPath}")
    
    return transcription

def create_labelling(labels,wav_splits):
    
    times = [((s.start + s.stop) / 2) / sampling_rate for s in wav_splits]
    labelling = []
    start_time = 0

    for i,time in enumerate(times):
        if i>0 and labels[i]!=labels[i-1]:
            temp = [str(labels[i-1]),start_time,time]
            labelling.append(tuple(temp))
            start_time = time
        if i==len(times)-1:
            temp = [str(labels[i]),start_time,time]
            labelling.append(tuple(temp))

    return labelling


def trim_audio(input_file, output_file, start, end):
    """
    use ffmpeg cut audio, from start to end (in seconds)
    """
    command = [
        "ffmpeg", "-y", "-i", input_file,
        "-ss", str(start),
        "-to", str(end),
        "-c", "copy", 
        output_file
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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