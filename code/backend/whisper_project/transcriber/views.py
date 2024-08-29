#from django.shortcuts import render
import os
import whisper
from django.shortcuts import render
from django.http import JsonResponse
from .forms import UploadFileForm

from resemblyzer import VoiceEncoder, preprocess_wav
from pathlib import Path



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
            fpath = Path("temp_audio")

            # Remove the temporary file
            os.remove('temp_audio')

            wav = preprocess_wav(fpath)

            encoder = VoiceEncoder()
            embed = encoder.embed_utterance(wav)
            np.set_printoptions(precision=3, suppress=True)
            print(embed)

            # Return the transcription
            return JsonResponse({'transcription': result['text']})

    else:
        form = UploadFileForm()
    return render(request, 'transcriber/index.html', {'form': form})

# Create your views here.
