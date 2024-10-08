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
    # test_audio = AudioSegment.from_file(audioPath, "wav")

    # split the audio file into chunks based on silence detection
    chunks = split_on_silence(test_audio, 
                            min_silence_len=300,  
                            silence_thresh=-40  
                            )
    
    # Calculate start times for all chunks (before filtering)
    chunk_times = []
    # Initialize the start time and total audio duration
    start_time = 0
    

    for chunk in chunks:
        chunk_duration = len(chunk)
        chunk_times.append((start_time, start_time + chunk_duration))
        start_time += chunk_duration

    for i, label in enumerate(chunk_times):
        print(f"Chunk {i} (from {chunk_times[i][0]/1000:.2f} to {chunk_times[i][1]/1000:.2f} seconds)")

    print('\n')

    # filter out chunks that are less than 600 ms
    # filtered_chunks = [chunk for chunk in chunks if len(chunk) >= 600]
    filtered_chunks = [(chunk, chunk_times[i]) for i, chunk in enumerate(chunks) if len(chunk) >= 600]
    # Now `filtered_chunks` is a list of tuples: (chunk, (start_time, end_time))


    # # save each chunk to a separate wav file
    # for i, chunk in enumerate(filtered_chunks):
    #     chunk.export(f"chunk{i}.wav", format="wav")

    encoder = VoiceEncoder()
    # embed each chunk
    embeddings = []
    filtered_chunk_times = []  # To store times of filtered chunks


    # Save each filtered chunk to a separate wav file and process
    for i, (chunk, times) in enumerate(filtered_chunks):
        chunk.export(f"chunk{i}.wav", format="wav")
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


def assign_speakers_to_transcription(result):
    if result is None:
        return None
    
    # Get the speaker segments
    segments = result['segments']

    # Get the speaker labels and chunk times using the speaker_identifier function
    labels, chunk_times = speaker_identifier('temp_audio')

    # Process the speaker segments and associate them with the speaker labels
    transcriptions = []
    for segment in segments:
        start = segment['start'] * 1000  # convert to milliseconds
        end = segment['end'] * 1000
        text = segment['text']
        print(segment['start'], segment['end'], text)

        # find the speaker label for the segment
        speaker_label = None
        for i, (chunk_start, chunk_end) in enumerate(chunk_times):
            if (chunk_start <= start <= chunk_end) or (chunk_start <= end <= chunk_end):
                speaker_label = labels[i]
                break
        
        # Add the transcription to the list
        transcriptions.append({
            'speaker': speaker_label if speaker_label is not None else 'Unknown',
            'text': text.strip(),
            'start': start / 1000,  # convert back to seconds
            'end': end / 1000
        })

    # speaker_identifier('temp_audio')
    print(transcriptions)

    # convert np.int64 to int
    for entry in transcriptions:
        if isinstance(entry["speaker"], np.int64):
            entry["speaker"] = int(entry["speaker"])


    # merge the speaker segments with same speaker identifies
    merged_data = []
    current_segment = transcriptions[0]

    for i in range(1, len(transcriptions)):
        next_segment = transcriptions[i]
        
        # if the speaker is the same, merge the segments
        if current_segment['speaker'] == next_segment['speaker']:
            current_segment['text'] += ' ' + next_segment['text']
            current_segment['end'] = next_segment['end']
        else:
            # if the speaker is different, add the current segment to the merged data and start a new segment
            merged_data.append(current_segment)
            current_segment = next_segment
    
    # add the last segment to the merged data
    merged_data.append(current_segment)

    return merged_data

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
            print(result['text'])

            transcription_with_speaker = assign_speakers_to_transcription(result)

            # Remove the temporary file
            os.remove('temp_audio')

            # Return the transcription
            # return JsonResponse({'transcription': result['text']})
            return JsonResponse({"transcription": transcription_with_speaker}, safe=False)

    else:
        form = UploadFileForm()
    return render(request, 'transcriber/index.html', {'form': form})

# Create your views here.