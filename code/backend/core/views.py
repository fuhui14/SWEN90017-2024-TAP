from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.conf import settings
from django.core.files.storage import default_storage
from transcription.transcribe_service import handle_file_upload
from core.models import db, Transcription
import os
import uuid
import datetime

@api_view(['POST'])
def upload_audio_file(request):
    # Get file from request
    if 'file' not in request.FILES:
        return Response({"error": "No file part"}, status=status.HTTP_400_BAD_REQUEST)

    file = request.FILES['file']

    # check if the file is null
    if not file.name:
        return Response({"error": "No selected file"}, status=status.HTTP_400_BAD_REQUEST)

    # check if the format of the file is approved
    allowed_extensions = {'wav', 'mp3', 'm4a', 'flac', 'ogg', 'aac'}
    if file.name.split('.')[-1].lower() not in allowed_extensions:
        return Response({"error": "Unsupported file format"}, status=status.HTTP_400_BAD_REQUEST)

    # save the file to db
    file_name = default_storage.save(os.path.join(settings.MEDIA_ROOT, file.name), file)
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    # create a unique file ID
    file_id = str(uuid.uuid4())
    expiration_date = datetime.datetime.utcnow() + datetime.timedelta(days=30)

    # save the transcription record in db
    transcription = Transcription(
        file_id=file_id,
        file_name=file_name,
        transcription_text=None,
        status="Queued",
        created_at=datetime.datetime.utcnow(),
        expiration_date=expiration_date
    )
    db.session.add(transcription)
    db.session.commit()

    # add the task to the Celery queue
    handle_file_upload.delay(file_id, file_path)

    # return response to the client
    return Response({
        "message": "File uploaded successfully!",
        "fileId": file_id,
        "estimatedProcessingTime": "10 minutes"
    }, status=status.HTTP_200_OK)