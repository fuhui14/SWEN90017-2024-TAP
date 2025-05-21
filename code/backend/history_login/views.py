import json
import urllib.parse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from cryptography.fernet import Fernet
from django.conf import settings

# The email-sending helper is assumed to be implemented elsewhere in your project.
# Adjust the import path to match your project structure, for example:
# from emails.send_email import send_email
from emails.send_email import send_email


@csrf_exempt
def send_history_link(request):
    """
    Receive an email address from the frontend, encrypt it, generate a
    history-access link, and email that link to the user.

    Expected JSON payload from the frontend:
        { "email": "user@example.com" }
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return JsonResponse(
                {"message": "Request body must be valid JSON."}, status=400
            )

        email = data.get("email")
        if not email:
            print("Email is missing from request data")
            return JsonResponse({"message": "Email is required."}, status=400)

        # Encrypt the email address with Fernet symmetric encryption
        try:
            f = Fernet(settings.FERNET_KEY)
            encrypted_bytes = f.encrypt(email.encode("utf-8"))
            encrypted_email = encrypted_bytes.decode("utf-8")
        except Exception as e:
            print(f"Encryption error: {e}")
            return JsonResponse(
                {"message": "Failed to encrypt email address."}, status=500
            )

        # Build the history-access URL
        frontend_url = getattr(settings, "FRONTEND_URL", "http://127.0.0.1:3000")
        history_link = f"{frontend_url}/history?enc={urllib.parse.quote(encrypted_email)}"

        # Compose the email
        subject = "Your transcription-history access link"
        content = (
            "Hello,\n\n"
            "Please click the following link to view your transcription history:\n"
            f"{history_link}\n\n"
            "This link will remain valid for 30 days."
        )

        # Send the email (no attachment required, so file_content is empty)
        try:
            send_email(receiver=email, subject=subject, content=content, file_content="")
        except Exception as e:
            print(f"Send email error: {e}")
            return JsonResponse({"message": "Failed to send email."}, status=500)

        return JsonResponse(
            {"message": "The login link has been sent to your email. Please check your inbox."}
        )

    print("Unsupported HTTP method")
    return JsonResponse({"message": "Only the POST method is supported."}, status=405)
