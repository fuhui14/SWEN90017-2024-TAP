from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.conf import settings
from django.core.files.storage import default_storage
from transcription.transcribe_service import handle_file_upload
import os

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

    # call the service of transcribe for the file
    result = handle_file_upload(file_path)

    # return the response
    if result["success"]:
        return Response({
            "message": "File uploaded successfully!",
            "fileId": result["file_id"],
            "estimatedProcessingTime": "10 minutes"
        }, status=status.HTTP_200_OK)
    else:
        return Response({"error": result["error"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)