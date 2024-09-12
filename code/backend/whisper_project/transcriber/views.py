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

# progress: resemblyzer to extract embeddings from audio chunks
# use pydub to split audio into chunks, compare similarity between chunks
# if similarity is less than 0.3, then chunks are from different speakers
# todo: process different audio formats, improve speaker identification
# modify the min_silence_len and silence_thresh parameters to improve speaker identification
# use DBSCAN to cluster the embeddings
# todo: reduce the noise, try librosa

def load_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    if audio.sample_width == 2:
        return audio
    else:
        audio = audio.set_sample_width(2)
        return audio.export("temp_converted.wav", format="wav")

def speaker_identifier(audio):
    # use pydub to load the audio file
    test_audio = AudioSegment.from_file(audio, "m4a")

    filtered_audio = test_audio - 20 

    # filtered_audio.export("output_audio.wav", format="wav")

    # split the audio file into chunks based on silence detection
    chunks = split_on_silence(test_audio, 
                            min_silence_len=300,  
                            silence_thresh=-40  
                            )

    # save each chunk to a separate wav file
    for i, chunk in enumerate(chunks):
        chunk.export(f"chunk{i}.wav", format="wav")

    encoder = VoiceEncoder()

    # embed each chunk
    embeddings = []
    for i, chunk in enumerate(chunks):
        wav_chunk = preprocess_wav(f"chunk{i}.wav")
        embed = encoder.embed_utterance(wav_chunk)
        embeddings.append(embed)


    # transform the embeddings into a numpy array
    embeddings = np.array(embeddings)

    # use DBSCAN to cluster the embeddings
    clustering = DBSCAN(metric="cosine", eps=0.3, min_samples=1).fit(embeddings)
    labels = clustering.labels_

    # print the number of speakers detected
    num_speakers = len(set(labels))
    print(f"Number of speakers detected: {num_speakers}")

    for i, label in enumerate(labels):
        print(f"Chunk {i} is from speaker {label}")

    # remove the temporary files
    for i in range(len(chunks)):
        os.remove(f"chunk{i}.wav")


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
