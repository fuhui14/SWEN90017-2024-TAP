import os
from resemblyzer import VoiceEncoder, preprocess_wav, sampling_rate
from pathlib import Path
import numpy as np
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.silence import detect_silence
from sklearn.cluster import DBSCAN
import librosa
import noisereduce as nr
from io import BytesIO
from spectralcluster import SpectralClusterer
import subprocess

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