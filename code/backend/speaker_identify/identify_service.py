import os
from resemblyzer import VoiceEncoder, preprocess_wav
from pathlib import Path
import numpy as np
from pydub import AudioSegment
from pydub.silence import split_on_silence
from sklearn.cluster import DBSCAN
import librosa
import noisereduce as nr
from io import BytesIO

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

def numpy_to_audiosegment(audio, sr):
    audio = (audio * 32767).astype(np.int16)
    byte_io = BytesIO(audio.tobytes())
    return AudioSegment.from_raw(byte_io, sample_width=2, frame_rate=sr, channels=1)

def preprocess_audio(audioPath):
    pre_audio, sr = librosa.load(audioPath, sr=16000)
    noise_background = pre_audio[0:2000]
    reduced_noise = nr.reduce_noise(y=pre_audio, sr=sr, y_noise=noise_background)
    audio = numpy_to_audiosegment(reduced_noise, sr)
    audio = audio + 20
    return audio

def speaker_identifier(audioPath):
    audioPath = convert_to_wav(audioPath)
    test_audio = preprocess_audio(audioPath)
    chunks = split_on_silence(test_audio, min_silence_len=300, silence_thresh=-50)
    filtered_chunks = [chunk for chunk in chunks if len(chunk) >= 600]

    encoder = VoiceEncoder()
    embeddings = []
    for i, chunk in enumerate(filtered_chunks):
        chunk.export(f"chunk{i}.wav", format="wav")
        wav_chunk = preprocess_wav(f"chunk{i}.wav")
        embed = encoder.embed_utterance(wav_chunk)
        embeddings.append(embed)

    embeddings = np.array(embeddings)
    clustering = DBSCAN(metric="cosine", eps=0.16, min_samples=1).fit(embeddings)
    labels = clustering.labels_

    num_speakers = len(set(labels))
    print(f"Number of speakers detected: {num_speakers}")
    for i, label in enumerate(labels):
        print(f"Chunk {i} is from speaker {label}")

    for i in range(len(filtered_chunks)):
        os.remove(f"chunk{i}.wav")
    os.remove(audioPath)
