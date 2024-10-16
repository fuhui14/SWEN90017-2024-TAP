import os
from django.shortcuts import render
from django.http import JsonResponse
from .forms import UploadFileForm
from .transcribe_service import transcribe_audio


def transcribe(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded file to a temporary location
            file = request.FILES['file']
            with open('temp_audio', 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)

            # Transcribe the audio file
            transcription = transcribe_audio('temp_audio')

            # Remove the temporary file
            os.remove('temp_audio')

            # Return the transcription
            return JsonResponse({'transcription': transcription})

    else:
        form = UploadFileForm()
    return render(request, 'index.html', {'form': form})
