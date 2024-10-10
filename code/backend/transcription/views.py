import os
from django.shortcuts import render
from django.http import JsonResponse

from code.backend.speaker_identify.assign_speaker_service import assign_speakers_to_transcription
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

            transcription_with_speaker = assign_speakers_to_transcription(transcription)

            # Remove the temporary file
            os.remove('temp_audio')

            # Return the transcription
            return JsonResponse({"transcription": transcription_with_speaker}, safe=False)

    else:
        form = UploadFileForm()
    return render(request, 'index.html', {'form': form})