import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest import mock

from transcription.models import File, Transcription

@pytest.mark.django_db
def test_upload_transcribe_success(client, tmp_path):
    dummy_audio = SimpleUploadedFile("test.wav", b"dummy-audio-content", content_type="audio/wav")
    with mock.patch("transcription.views.transcribe_with_speaker") as mock_transcribe:
        mock_transcribe.return_value = "This is a dummy transcription."

        response = client.post(reverse("transcribe"), {
            "email": "test@example.com",
            "file": dummy_audio,
        })

    assert response.status_code == 200
    assert "transcription" in response.json()
    assert File.objects.count() == 1
    assert Transcription.objects.count() == 1

@pytest.mark.django_db
def test_upload_form_invalid(client):
    response = client.post(reverse("transcribe"), {
        "email": "not-an-email"
    })
    assert response.status_code == 400
    assert "error" in response.json()
