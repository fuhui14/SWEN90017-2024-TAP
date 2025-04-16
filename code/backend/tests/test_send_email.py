import pytest
from unittest import mock
from emails.send_email import send_email, FileType
import os


@pytest.mark.parametrize("file_type,patch_target,filename", [
    (FileType.TXT, "emails.send_email.text_file", "result.txt"),
    (FileType.DOCX, "emails.send_email.docx_file", "result.docx"),
    (FileType.PDF, "emails.send_email.pdf_file", "result.pdf"),
])
@mock.patch("smtplib.SMTP")
def test_send_email_with_attachment(mock_smtp, tmp_path, file_type, patch_target, filename):
    """
    Test sending an email with a TXT, DOCX, or PDF attachment.
    Ensure the temporary file is generated and deleted after sending.
    """
    sample_text = "This is test content for attachment."
    email = "user@example.com"

    file_path = tmp_path / filename
    file_path.write_text(sample_text)

    with mock.patch(patch_target, return_value=str(file_path)):
        send_email(
            receiver=email,
            subject="Test Email",
            content="This is a test email",
            file_content=sample_text,
            file_type=file_type
        )

    # SMTP flow validation
    mock_smtp.assert_called_once()
    smtp_instance = mock_smtp.return_value
    smtp_instance.starttls.assert_called_once()
    smtp_instance.login.assert_called_once()
    smtp_instance.sendmail.assert_called_once()

    # File should be deleted
    assert not file_path.exists()

@mock.patch("smtplib.SMTP")
def test_send_email_without_attachment(mock_smtp):
    """
    Test sending an email without any attachment (FileType.NONE).
    """
    send_email(
        receiver="test@example.com",
        subject="No Attachment",
        content="This is a body without attachments.",
        file_content="",
        file_type=FileType.NONE
    )

    mock_smtp.assert_called_once()
    smtp_instance = mock_smtp.return_value
    smtp_instance.starttls.assert_called_once()
    smtp_instance.login.assert_called_once()
    smtp_instance.sendmail.assert_called_once()


@mock.patch("smtplib.SMTP", side_effect=Exception("SMTP server error"))
def test_send_email_failure_handling(mock_smtp_error):
    """
    Ensure the function handles SMTP errors gracefully.
    """
    try:
        send_email(
            receiver="fail@example.com",
            subject="Failure Test",
            content="This should trigger an SMTP error.",
            file_content="Some content",
            file_type=FileType.TXT
        )
    except Exception:
        pytest.fail("send_email raised an unexpected exception")

    mock_smtp_error.assert_called_once()
