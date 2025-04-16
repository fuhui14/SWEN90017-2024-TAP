# import pytest
# from django.urls import reverse
# from transcription.models import File, Transcription
# from django.utils import timezone
# from cryptography.fernet import Fernet
# from django.conf import settings
# import json
#
#
# @pytest.mark.django_db
# def test_admin_history_success(client):
#     """
#     Test the /api/admin/history/ endpoint returns valid transcription history
#     when given a correctly encrypted email.
#     """
#     email = "testuser@example.com"
#
#     # Create a file and transcription record
#     file = File.objects.create(
#         email=email,
#         original_filename="test.wav",
#         storage_path="/fake/path/test.wav",
#         file_size=1234,
#         status="completed",
#         upload_timestamp=timezone.now() - timezone.timedelta(days=10)
#     )
#
#     Transcription.objects.create(
#         file=file,
#         transcribed_text="Hello, this is a test transcription."
#     )
#
#     # Encrypt email
#     f = Fernet(settings.FERNET_KEY)
#     enc = f.encrypt(email.encode()).decode()
#
#     response = client.post(
#         "/api/admin/history/",
#         data=json.dumps({"enc": enc}),
#         content_type="application/json"
#     )
#
#     assert response.status_code == 200
#     history = response.json()
#     assert isinstance(history, list)
#     assert len(history) == 1
#     assert history[0]["taskName"] == "test.wav"
#     assert history[0]["status"] == "Completed"
#
#
# @pytest.mark.django_db
# def test_admin_history_invalid_token(client):
#     """
#     If an invalid encrypted value is provided, the server should return 403.
#     """
#     response = client.post(
#         "/api/admin/history/",
#         data=json.dumps({"enc": "thisisnotvalid"}),
#         content_type="application/json"
#     )
#     assert response.status_code == 403
#     assert "error" in response.json()
#
#
# def test_admin_history_missing_enc(client):
#     """
#     If 'enc' is missing, should return 400 Bad Request.
#     """
#     response = client.post(
#         "/api/admin/history/",
#         data=json.dumps({}),
#         content_type="application/json"
#     )
#     assert response.status_code == 400
#     assert "error" in response.json()
#
#
# def test_admin_history_wrong_method(client):
#     """
#     If method is GET instead of POST, should return 405.
#     """
#     response = client.get("/api/admin/history/")
#     assert response.status_code == 405
#     assert "error" in response.json()
