<<<<<<< Updated upstream
=======
import os
import uuid
from django.conf import settings
from django.http import JsonResponse
from .forms import UploadFileForm
from .transcribe_service import transcribe_audio
from .models import File, Transcription  # Ensure File and Transcription models are defined

def transcribe(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            file = request.FILES['file']
            upload_id = uuid.uuid4()
            original_filename = file.name

            storage_dir = os.path.join(settings.MEDIA_ROOT, 'uploads', email, upload_id.hex)
            os.makedirs(storage_dir, exist_ok=True)
            file_path = os.path.join(storage_dir, original_filename)

            with open(file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)

            # Save file metadata to database
            db_file = File.objects.create(
                email=email,
                upload_id=upload_id,
                original_filename=original_filename,
                storage_path=file_path,
                file_size=file.size,
                status='uploaded'
            )

            # Transcribe audio file and save transcription
            try:
                transcription = transcribe_audio(file_path)
                Transcription.objects.create(
                    file=db_file,
                    transcribed_text=transcription
                )
                return JsonResponse({"transcription": transcription}, safe=False)
            except Exception as e:
                return JsonResponse({'error': 'Transcription error'}, status=500)

        else:
            return JsonResponse({'error': 'Invalid form submission'}, status=400)

    return JsonResponse({'error': 'GET request not allowed'}, status=405)
>>>>>>> Stashed changes
