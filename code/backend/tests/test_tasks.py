import pytest
from unittest import mock
from transcription.models import File, Transcription
from transcription.tasks import process_transcription_and_send_email, cleanup_expired_files
from django.utils import timezone
import datetime
from freezegun import freeze_time


@pytest.mark.django_db
@mock.patch("transcription.tasks.send_email")
def test_process_transcription_and_send_email_success(mock_send_email):
    file = File.objects.create(
        email="testuser@example.com",
        original_filename="test.wav",
        storage_path="/fake/path/test.wav",
        file_size=12345,
        status="completed"
    )

    transcription = Transcription.objects.create(
        file=file,
        transcribed_text="Hello world!"
    )

    result = process_transcription_and_send_email(
        transcription.id,
        portal_link="http://frontend.test/history?token=abc"
    )

    mock_send_email.assert_called_once()
    assert "sent" in result or "testuser" in result


@pytest.mark.django_db
def test_process_transcription_and_send_email_invalid_id():
    result = process_transcription_and_send_email(9999)
    assert "not found" in result

@freeze_time("2024-01-01")
@pytest.mark.django_db
def test_cleanup_expired_files():
    # Create expired file
    expired = File.objects.create(
        email="expired@example.com",
        original_filename="expired.wav",
        storage_path="/fake/expired.wav",
        file_size=1000,
        status="uploaded"
    )
    expired.upload_timestamp = timezone.now() - datetime.timedelta(days=100)
    expired.save(update_fields=["upload_timestamp"])

    # Create recent file
    recent = File.objects.create(
        email="recent@example.com",
        original_filename="recent.wav",
        storage_path="/fake/recent.wav",
        file_size=2000,
        status="uploaded"
    )
    recent.upload_timestamp = timezone.now() - datetime.timedelta(days=10)
    recent.save(update_fields=["upload_timestamp"])

    # Run cleanup
    result = cleanup_expired_files()

    # Check
    assert File.objects.filter(email="expired@example.com").count() == 0
    assert File.objects.filter(email="recent@example.com").count() == 1
    assert "1" in result or "deleted" in result
