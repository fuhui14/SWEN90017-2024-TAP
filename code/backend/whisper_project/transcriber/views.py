#from django.shortcuts import render
import os
import whisper
from django.shortcuts import render
from django.http import JsonResponse
from .forms import UploadFileForm

from resemblyzer import VoiceEncoder, preprocess_wav
from pathlib import Path
import numpy as np

from pydub import AudioSegment
from pydub.silence import split_on_silence
from scipy.spatial.distance import cosine
from sklearn.cluster import DBSCAN
import librosa
import noisereduce as nr
from io import BytesIO

# progress: resemblyzer to extract embeddings from audio chunks
# use pydub to split audio into chunks, compare similarity between chunks
# if similarity is less than 0.3, then chunks are from different speakers
# modify the min_silence_len and silence_thresh parameters to improve speaker identification
# use DBSCAN to cluster the embeddings

# todo: process different audio formats, improve speaker identification

def convert_to_wav(file_path):
    try:
        # split the file name and extension type
        file_name = os.path.splitext(file_path)[0]

        # create a new file name with the .wav extension
        output_file = f"{file_name}.wav"

        # load the audio file and export it as a .wav file
        audio = AudioSegment.from_file(file_path)
        audio.export(output_file, format="wav")
        return output_file
    
    except Exception as e:
        print(e)
        return None
    
def numpy_to_audiosegment(audio, sr):
    # convert the numpy array to an AudioSegment
    # * 32767 to convert the audio from float to int16
    audio = (audio * 32767).astype(np.int16)

    # crete a byte stream
    byte_io = BytesIO(audio.tobytes())

    #create an AudioSegment from the byte stream
    audio_segment = AudioSegment.from_raw(byte_io, sample_width=2, frame_rate=sr, channels=1)
    return audio_segment

def preprocess_audio(audioPath):
    # load the audio file
    pre_audio, sr = librosa.load(audioPath, sr=16000)

    # reduce the noise in the audio file, use the first 2000 ms as the noise background
    noise_backgournd = pre_audio[0:2000]
    reduced_noise = nr.reduce_noise(y = pre_audio, sr = sr, y_noise = noise_backgournd)

    # convert the numpy array to an AudioSegment
    audio = numpy_to_audiosegment(reduced_noise, sr)

    # increase the volume of the audio file
    audio = audio + 20

    return audio

def speaker_identifier(audioPath):
    # use pydub to load the audio file
    # test_audio = AudioSegment.from_file(audioPath, "m4a")

    # filtered_audio = test_audio - 20 

    # filtered_audio.export("output_audio.wav", format="wav")
    audioPath = convert_to_wav(audioPath)

    test_audio = preprocess_audio(audioPath)

    # split the audio file into chunks based on silence detection
    chunks = split_on_silence(test_audio, 
                            min_silence_len=300,  
                            silence_thresh=-50  
                            )

    # filter out chunks that are less than 600 ms
    filtered_chunks = [chunk for chunk in chunks if len(chunk) >= 600]

    # save each chunk to a separate wav file
    for i, chunk in enumerate(filtered_chunks):
        chunk.export(f"chunk{i}.wav", format="wav")

    encoder = VoiceEncoder()

    # embed each chunk
    embeddings = []
    for i, chunk in enumerate(filtered_chunks):
        wav_chunk = preprocess_wav(f"chunk{i}.wav")
        embed = encoder.embed_utterance(wav_chunk)
        embeddings.append(embed)


    # transform the embeddings into a numpy array
    embeddings = np.array(embeddings)

    # use DBSCAN to cluster the embeddings
    clustering = DBSCAN(metric="cosine", eps=0.16, min_samples=1).fit(embeddings)
    labels = clustering.labels_

    # print the number of speakers detected
    num_speakers = len(set(labels))
    print(f"Number of speakers detected: {num_speakers}")

    for i, label in enumerate(labels):
        print(f"Chunk {i} is from speaker {label}")

    # # remove the temporary files
    for i in range(len(filtered_chunks)):
        os.remove(f"chunk{i}.wav")

    os.remove(audioPath)

# Load the Whisper model
model = whisper.load_model("base")

def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded file to a temporary location
            file = request.FILES['file']
            with open('temp_audio', 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            
            # Transcribe the audio file using Whisper
            result = model.transcribe('temp_audio')

            speaker_identifier('temp_audio')
            
            # Remove the temporary file
            os.remove('temp_audio')

            # Return the transcription
            return JsonResponse({'transcription': result['text']})

    else:
        form = UploadFileForm()
    return render(request, 'transcriber/index.html', {'form': form})

# Create your views here.
