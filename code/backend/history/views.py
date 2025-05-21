import json
from datetime import timedelta
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from transcription.models import Transcription

# Import Fernet encryption utilities and Django settings
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings


@csrf_exempt
def admin_history(request):
    print(f"Received request with method: {request.method}")

    if request.method == "POST":
        # Parse the incoming JSON payload
        try:
            body = json.loads(request.body)
            print(f"Request JSON parsed successfully: {body}")
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            return JsonResponse(
                {"error": "Request body must be valid JSON."}, status=400
            )

        encrypted = body.get("enc")
        print(f"Extracted encrypted value: {encrypted}")
        if not encrypted:
            print("No encrypted data provided in the request.")
            return JsonResponse({"error": "Missing encrypted data."}, status=400)

        # Decrypt the email using Fernet
        try:
            f = Fernet(settings.FERNET_KEY)
            print(f"Fernet instance created using key: {settings.FERNET_KEY}")
            decrypted_bytes = f.decrypt(encrypted.encode(), ttl=2592000)  # 30 days
            email = decrypted_bytes.decode("utf-8")
            print(f"Decrypted email: {email}")
        except InvalidToken as e:
            print(f"InvalidToken error during decryption: {e}")
            return JsonResponse({"error": "Invalid encrypted data."}, status=403)
        except Exception as e:
            print(f"Exception during decryption: {e}")
            return JsonResponse({"error": "Error during decryption."}, status=500)

        # Look up transcription records for the decrypted email
        try:
            transcriptions = (
                Transcription.objects.select_related("file")
                .filter(file__email=email)
            )
            count = transcriptions.count()
            print(f"Found {count} transcription record(s) for email: {email}")
        except Exception as e:
            print(f"Database query error: {e}")
            return JsonResponse({"error": "Error querying database."}, status=500)

        # Build the response payload
        history_data = []
        for transcription in transcriptions:
            # Use the File model's upload_timestamp as the creation date
            creation_date = (
                transcription.file.upload_timestamp
                if transcription.file and transcription.file.upload_timestamp
                else timezone.now()
            )
            expiry_date = creation_date + timedelta(days=30)
            days_left = max((expiry_date - timezone.now()).days, 0)

            record = {
                "id": transcription.id,
                "taskName": (
                    transcription.file.original_filename
                    if transcription.file and transcription.file.original_filename
                    else ""
                ),
                "taskType": "Transcription",
                "creationDate": creation_date.isoformat(),
                "daysLeft": days_left,
                "outputType": "text",
                "status": "Completed" if transcription.transcribed_text else "Failed",
            }
            history_data.append(record)
            print(f"Processed transcription record: {record}")

        print("Returning history data to client.")
        return JsonResponse(history_data, safe=False)

    # Unsupported HTTP method
    print("Unsupported HTTP method encountered.")
    return JsonResponse({"error": "Only POST method is supported."}, status=405)


@csrf_exempt
def download_history(request):
    print(f"Download request received with method: {request.method}")
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method is supported."}, status=405)

    # Parse the incoming JSON payload
    try:
        body = json.loads(request.body)
        record_id = body.get("id")
        if not record_id:
            return JsonResponse({"error": "Record ID is missing."}, status=400)
        print(f"Download request for record ID: {record_id}")
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        return JsonResponse(
            {"error": "Request body must be valid JSON."}, status=400
        )

    # Retrieve the transcription record
    try:
        transcription = (
            Transcription.objects.select_related("file").get(id=record_id)
        )
    except Transcription.DoesNotExist:
        print("Transcription record does not exist.")
        return JsonResponse({"error": "Record does not exist."}, status=404)
    except Exception as e:
        print(f"Database query error: {e}")
        return JsonResponse({"error": "Error querying database."}, status=500)

    # Retrieve transcribed text content
    text_content = transcription.transcribed_text
    if not text_content:
        return JsonResponse(
            {"error": "No transcription content available for download."}, status=404
        )

    # Return the transcription as a plain-text file download
    response = HttpResponse(text_content, content_type="text/plain")

    # Use original filename from File model if provided; otherwise, fall back to a default name
    filename = (
        transcription.file.original_filename
        if transcription.file and transcription.file.original_filename
        else "transcription"
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}.txt"'
    print("Download response prepared, returning file to client.")
    return response
