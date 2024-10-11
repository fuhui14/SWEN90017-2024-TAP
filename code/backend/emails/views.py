from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from core.models import Transcription
from send_email import *

@api_view(['POST'])
def download_file(request):
    file_id = request.data.get('file_id', None)
    file_format = request.data.get('format', None)
    receiver_email = request.data.get('email', None)

    if not file_id or not file_format or not receiver_email:
        return Response({"error": "file_id, format, and email are required"}, status=status.HTTP_400_BAD_REQUEST)

    valid_formats = ['txt', 'docx', 'pdf']
    if file_format not in valid_formats:
        return Response({"error": "Invalid format. Supported formats are: txt, docx, pdf."}, status=status.HTTP_400_BAD_REQUEST)

    transcription = Transcription.query.filter_by(file_id=file_id).first()

    if not transcription:
        return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

    if transcription.status != "Completed":
        return Response({"message": "Transcription is still in progress. Please try again later."}, status=status.HTTP_200_OK)

    transcription_text = transcription.transcription_text

    if file_format == 'txt':
        file_type = FileType.TXT
    elif file_format == 'docx':
        file_type = FileType.DOCX
    elif file_format == 'pdf':
        file_type = FileType.PDF

    subject = f"Transcription File {file_id} - {file_format.upper()}"
    content = "Here is your transcribed file."

    try:
        send_email(receiver=receiver_email, subject=subject, content=content, file_content=transcription_text, file_type=file_type)
        return Response({"message": "File sent successfully!"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)