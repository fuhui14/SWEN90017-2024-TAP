import pytest
from unittest import mock
from transcription.models import File, Transcription
from transcription.tasks import process_transcription_and_send_email, cleanup_expired_files
from django.utils import timezone
import datetime
from freezegun import freeze_time
from unittest.mock import patch
from emails.send_email import FileType
import uuid


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


@pytest.mark.django_db
@patch("transcription.tasks.send_email")
def test_transcription_email_body_content(mock_send_email):
    file = File.objects.create(
        email="user@example.com",
        upload_id=uuid.uuid4(),
        original_filename="test.wav",
        storage_path="dummy/path/test.wav",
        file_size=1234,
        status="uploaded"
    )

    transcription = Transcription.objects.create(
        file=file,
        transcribed_text="This is the actual transcription content."
    )

    # Call the function
    process_transcription_and_send_email(
        transcription.id,
        portal_link="http://dummy.portal/link",
        file_type=FileType.PDF
    )

    assert mock_send_email.called

    args, kwargs = mock_send_email.call_args

    receiver = kwargs["receiver"]
    subject = kwargs["subject"]
    content = kwargs["content"]
    file_content = kwargs["file_content"]
    file_type = kwargs["file_type"]

    print("\n=== EMAIL RECEIVER ===")
    print(receiver)
    print("\n=== EMAIL SUBJECT ===")
    print(subject)
    print("\n=== EMAIL BODY ===")
    print(content)
    print("\n=== FILE TYPE ===")
    print(file_type)

    if file_type == FileType.PDF:
        expected_ext = ".pdf"
    elif file_type == FileType.DOCX:
        expected_ext = ".docx"
    elif file_type == FileType.TXT:
        expected_ext = ".txt"
    else:
        expected_ext = None

    assert receiver == "user@example.com"
    assert "Transcription Result" in subject
    assert content.startswith("Here is your transcription result.")
    assert "http://dummy.portal/link" in content
    assert "actual transcription content" in file_content

    if expected_ext:
        assert file_type.name.lower() in expected_ext, f"Attachment extension mismatch: {expected_ext}"

