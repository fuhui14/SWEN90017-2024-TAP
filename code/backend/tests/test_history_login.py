# import pytest
# from django.urls import reverse
# from transcription.models import File
# from django.utils import timezone
# from cryptography.fernet import Fernet
# from django.conf import settings
# from unittest.mock import patch
# import json
#
#
# @pytest.mark.django_db
# @patch("emails.send_email.send_email")
# def test_send_history_link_success(mock_send_email, client):
#     """
#     Test sending a history link email for a user with valid upload history.
#     """
#     email = "test@example.com"
#
#     # Create a file record
#     File.objects.create(
#         email=email,
#         original_filename="history.wav",
#         storage_path="/fake/history.wav",
#         file_size=1000,
#         status="uploaded",
#         upload_timestamp=timezone.now()
#     )
#
#     # Send POST request with valid email
#     response = client.post(
#         "/api/send-history-link/",
#         data=json.dumps({"email": email}),
#         content_type="application/json"
#     )
#
#     assert response.status_code == 200
#     assert "message" in response.json()
#     mock_send_email.assert_called_once()
#     assert email in mock_send_email.call_args.kwargs["receiver"]
#
#
# def test_send_history_link_missing_email(client):
#     """
#     If 'email' field is missing in request, should return 400.
#     """
#     response = client.post(
#         "/api/send-history-link/",
#         data=json.dumps({}),
#         content_type="application/json"
#     )
#
#     assert response.status_code == 400
#     assert "error" in response.content.decode() or "message" in response.json()
#
#
# @pytest.mark.django_db
# def test_send_history_link_no_history(client):
#     """
#     If no matching File record exists for the provided email, should return 404.
#     """
#     response = client.post(
#         "/api/send-history-link/",
#         data=json.dumps({"email": "noexist@example.com"}),
#         content_type="application/json"
#     )
#
#     assert response.status_code == 404
#     assert "error" in response.json()
#
#
# def test_send_history_link_wrong_method(client):
#     """
#     Sending a GET request instead of POST should return 405.
#     """
#     response = client.get("/api/send-history-link/")
#     assert response.status_code == 405
#     assert "message" in response.json()
