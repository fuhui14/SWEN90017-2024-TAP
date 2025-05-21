import json
from datetime import timedelta
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from transcription.models import Transcription

# Import Fernet encryption utilities and Django settings
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
import traceback  # For detailed error logging
import ast  # <--- Added this import for ast.literal_eval


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
        print("Unsupported HTTP method for download.")
        return JsonResponse({"error": "Only POST method is supported."}, status=405)

    # Parse the incoming JSON payload
    try:
        body = json.loads(request.body)  # This JSON is for the request itself, not the transcription data
        record_id = body.get("id")
        if not record_id:
            print("Record ID missing in download request.")
            return JsonResponse({"error": "Record ID is missing."}, status=400)
        print(f"Download request for record ID: {record_id}")
    except json.JSONDecodeError as e:  # This handles if the request body is not valid JSON
        print(f"JSONDecodeError in download request body: {e}")
        return JsonResponse(
            {"error": "Request body must be valid JSON."}, status=400
        )

    # Retrieve the transcription record
    try:
        transcription = (
            Transcription.objects.select_related("file").get(id=record_id)
        )
    except Transcription.DoesNotExist:
        print(f"Transcription record ID {record_id} does not exist.")
        return JsonResponse({"error": "Record does not exist."}, status=404)
    except Exception as e:
        print(f"Database query error for ID {record_id}: {e}")
        return JsonResponse({"error": "Error querying database."}, status=500)

    # --- Start Enhanced Debugging for Transcription Content ---
    print(f"--- Debug Processing for Record ID {record_id} ---")
    raw_text_content = transcription.transcribed_text
    print(f"DEBUG_DOWNLOAD [1]: Type of raw_text_content: {type(raw_text_content)}")
    print(
        f"DEBUG_DOWNLOAD [2]: raw_text_content (first 500 chars): {raw_text_content[:500] if raw_text_content else 'None or empty'}")

    if not raw_text_content:
        print(f"DEBUG_DOWNLOAD [2a]: No transcription content available for record ID {record_id}.")
        return JsonResponse(
            {"error": "No transcription content available for download."}, status=404
        )

    formatted_text_output = ""
    transcription_data = None
    try:
        # MODIFICATION: Use ast.literal_eval instead of json.loads
        print("DEBUG_DOWNLOAD [3]: Attempting to parse content with ast.literal_eval from raw_text_content...")
        transcription_data = ast.literal_eval(raw_text_content)

        print(f"DEBUG_DOWNLOAD [4]: Parsed transcription_data type: {type(transcription_data)}")
        print(f"DEBUG_DOWNLOAD [5]: Parsed transcription_data content (or part of it):")
        if isinstance(transcription_data, list):
            print(f"   Length: {len(transcription_data)}, First 3 elements: {transcription_data[:3]}")
        else:
            print(f"   Content (repr, first 500 chars): {repr(transcription_data)[:500]}")

        if not isinstance(transcription_data, list):
            print(
                f"DEBUG_DOWNLOAD [6]: Transcription data for record ID {record_id} is NOT a list as expected. Actual Type: {type(transcription_data)}")
            formatted_text_output = raw_text_content
            print(f"   Using raw_text_content as fallback output.")
        else:
            print(f"DEBUG_DOWNLOAD [6]: Transcription data is a list. Processing {len(transcription_data)} segments.")
            formatted_segments = []
            for i, segment in enumerate(transcription_data):
                print(f"   --- Processing segment {i} ---")
                print(f"   DEBUG_DOWNLOAD [7.{i}]: Raw segment: {segment}")
                print(f"   DEBUG_DOWNLOAD [8.{i}]: Segment type: {type(segment)}")
                if isinstance(segment, dict):
                    speaker_id_str = segment.get("speaker")
                    text = segment.get("text")
                    print(
                        f"   DEBUG_DOWNLOAD [9.{i}]: Extracted speaker_id_str: '{speaker_id_str}' (type: {type(speaker_id_str)})")
                    text_snippet = (text[:70] + '...') if text and len(text) > 70 else text
                    print(f"   DEBUG_DOWNLOAD [10.{i}]: Extracted text: '{text_snippet}' (type: {type(text)})")

                    if speaker_id_str is not None and text is not None:
                        try:
                            speaker_num = int(speaker_id_str) + 1
                            speaker_label = f"Speaker {speaker_num}"
                            print(f"   DEBUG_DOWNLOAD [11.{i}]: Calculated speaker_label: '{speaker_label}'")
                            formatted_segments.append(f"{speaker_label}: {text}")
                        except ValueError:
                            print(
                                f"   DEBUG_DOWNLOAD [11.{i}]: ValueError - Speaker ID '{speaker_id_str}' is not an integer. Using raw ID for label.")
                            speaker_label = f"Speaker {speaker_id_str}"
                            formatted_segments.append(f"{speaker_label}: {text}")
                    else:
                        print(f"   DEBUG_DOWNLOAD [11.{i}]: Skipping segment due to missing speaker_id_str or text.")
                else:
                    print(f"   DEBUG_DOWNLOAD [8.{i}]: Segment is not a dictionary. Skipping.")

            print(f"DEBUG_DOWNLOAD [12]: All formatted_segments before join: {formatted_segments}")
            formatted_text_output = "\n\n".join(formatted_segments)
            output_snippet = (formatted_text_output[:450] + '\n...') if len(
                formatted_text_output) > 450 else formatted_text_output
            print(f"DEBUG_DOWNLOAD [13]: Final formatted_text_output (first 500 chars or so): \n{output_snippet}")

    # MODIFICATION: Catch errors relevant to ast.literal_eval
    except (ValueError, SyntaxError, TypeError) as e:
        print(f"!!! Error during ast.literal_eval for record ID {record_id}: {e}")
        print(f"    Content that failed to parse (first 500 chars): {raw_text_content[:500]}")
        formatted_text_output = raw_text_content
        print(f"    Using raw_text_content as fallback output due to parsing error.")
    except Exception as e:  # Catch any other unexpected errors
        print(f"!!! Unexpected error during transcription formatting for ID {record_id}: {e}")
        print(traceback.format_exc())
        formatted_text_output = raw_text_content
        print(f"    Using raw_text_content as fallback output due to unexpected error.")

    print(f"--- End Debug Processing for Record ID {record_id} ---")
    # --- End Enhanced Debugging ---

    # Determine filename
    base_filename = (
        transcription.file.original_filename
        if transcription.file and transcription.file.original_filename
        else "transcription"
    )
    if '.' in base_filename:
        base_filename = base_filename.rsplit('.', 1)[0]

    file_extension = "txt"
    content_type = "text/plain"
    final_filename = f"{base_filename}.{file_extension}"

    response = HttpResponse(formatted_text_output, content_type=content_type)
    response["Content-Disposition"] = f'attachment; filename="{final_filename}"'
    print(f"Download response prepared for {final_filename}. Content type: {content_type}.")
    return response