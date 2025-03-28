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
    # use pydub to load the audio file
    # test_audio = AudioSegment.from_file(audioPath, "m4a")

    # filtered_audio = test_audio - 20 

    # filtered_audio.export("output_audio.wav", format="wav")
    audioPath = convert_to_wav(audioPath)

    test_audio = preprocess_audio(audioPath)
    # test_audio = AudioSegment.from_file(audioPath, "wav")

    # split the audio file into chunks based on silence detection
    chunks = split_on_silence(test_audio, 
                            min_silence_len=300,  
                            silence_thresh=-40  
                            )
    
    silence_times = detect_silence(test_audio, 
                                min_silence_len=300, 
                                silence_thresh=-40)
    
    for silence_start, silence_end in silence_times:
        print(f"Silence: Start = {silence_start/1000} s, End = {silence_end/1000} s")
    
    # Calculate start times for all chunks (before filtering)
    chunk_times = []
    # Initialize the original start time to 0
    current_time = 0

    # Calculate the start and end times of each non-silent chunk based on silence
    for start, end in silence_times:
        # If there is audio before the current silence, add a chunk for it
        if current_time < start:
            # The chunk starts with the current time and ends where the silence starts
            chunk_times.append((current_time, start))

        # Update the previous end to the end of the current silence
        current_time = end

    # Add the final chunk if there is any audio after the last silence
    if current_time < len(test_audio):
        chunk_times.append((current_time, len(test_audio)))

    for i, label in enumerate(chunk_times):
        print(f"Chunk {i} (from {chunk_times[i][0]/1000:.2f} to {chunk_times[i][1]/1000:.2f} seconds)")

    # filter out chunks that are less than 600 ms
    # filtered_chunks = [chunk for chunk in chunks if len(chunk) >= 600]
    filtered_chunks = [(chunk, chunk_times[i]) for i, chunk in enumerate(chunks) if len(chunk) >= 600]
    # Now `filtered_chunks` is a list of tuples: (chunk, (start_time, end_time))


    # # save each chunk to a separate wav file
    for i, chunk in enumerate(chunks):
        chunk.export(f"chunk{i}.wav", format="wav")

    encoder = VoiceEncoder()
    # embed each chunk
    embeddings = []
    filtered_chunk_times = []  # To store times of filtered chunks


    # Save each filtered chunk to a separate wav file and process
    for i, (chunk, times) in enumerate(filtered_chunks):
        wav_chunk = preprocess_wav(f"chunk{i}.wav")
        embed = encoder.embed_utterance(wav_chunk)
        embeddings.append(embed)

        # Keep the times only for the filtered chunks
        filtered_chunk_times.append(times)

    # transform the embeddings into a numpy array
    embeddings = np.array(embeddings)

    # use DBSCAN to cluster the embeddings
    clustering = DBSCAN(metric="cosine", eps=0.16, min_samples=1).fit(embeddings)
    labels = clustering.labels_

    # print the number of speakers detected
    num_speakers = len(set(labels))
    print(f"Number of speakers detected: {num_speakers}")

    for i, label in enumerate(labels):
        print(f"Chunk {i} (from {filtered_chunk_times[i][0]/1000:.2f} to {filtered_chunk_times[i][1]/1000:.2f} seconds) is from speaker {label}")

    # remove the temporary files
    for i in range(len(filtered_chunks)):
        os.remove(f"chunk{i}.wav")

    os.remove(audioPath)

    return labels, filtered_chunk_times