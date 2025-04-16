# import io
# import uuid
# from unittest import TestCase
# from unittest.mock import patch
#
# from django.core.files.uploadedfile import SimpleUploadedFile
# from django.test import Client, override_settings
# from django.urls import reverse
#
# from transcription.models import File, Transcription
#
# class AdminPortalEmailTests(TestCase):
#
#     def setUp(self):
#         override = override_settings(MEDIA_ROOT='uploads/')
#         override.enable()
#         self.addCleanup(override.disable)
#
#     @patch("transcription.tasks.send_email")  # Mock send_email
#     @patch('transcription.views.transcribe_audio')
#     @patch('transcription.views.assign_speakers_to_transcription')
#     def test_email_contains_portal_link(self, mock_speaker, mock_transcribe, mock_send):
#         # Arrange
#         mock_transcribe.return_value = "This is a test transcript."
#         mock_speaker.return_value = "Speaker 1: This is a test transcript."
#         mock_send.return_value = None
#
#         client = Client()
#
#         # Create a fake file
#         audio_content = io.BytesIO(b"fake audio data")
#         uploaded_file = SimpleUploadedFile("sample.wav", audio_content.read(), content_type="audio/wav")
#
#         # Act
#         response = client.post(
#             reverse("transcribe"),
#             {"email": "test@example.com", "file": uploaded_file}
#         )
#
#         # Assert
#         self.assertEqual(response.status_code, 200)
#
#         # Get token from the created File instance
#         file = File.objects.filter(email="test@example.com").latest("upload_timestamp")
#         expected_link = f"http://localhost:3000/history?token={file.portal_token}"
#
#         # Check that the email was sent and contains the portal link
#         mock_send.assert_called_once()
#         args, kwargs = mock_send.call_args
#         email_body = args[2]
#         self.assertIn(expected_link, email_body)
