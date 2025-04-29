import pytest
from unittest import mock
from emails.send_email import send_email, FileType
import os
import email


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
    email_addr = "user@example.com"

    file_path = tmp_path / filename
    file_path.write_text(sample_text)

    with mock.patch(patch_target, return_value=str(file_path)):
        send_email(
            receiver=email_addr,
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

@pytest.mark.parametrize("file_type,expected_extension", [
    (FileType.TXT, ".txt"),
    (FileType.DOCX, ".docx"),
    (FileType.PDF, ".pdf"),
])
@mock.patch("smtplib.SMTP")
def test_send_email_attachment_extension_correct(mock_smtp, tmp_path, file_type, expected_extension):
    """
    Verify that the email sent contains the correct file extension based on the selected file_type.
    """
    sample_text = "Sample content for attachment."
    receiver = "user@example.com"
    subject = "Test Email with Attachment"
    content = "Please find the attachment."

    dummy_file_path = tmp_path / f"test{expected_extension}"
    dummy_file_path.write_text(sample_text)

    patch_target = {
        FileType.TXT: "emails.send_email.text_file",
        FileType.DOCX: "emails.send_email.docx_file",
        FileType.PDF: "emails.send_email.pdf_file",
    }[file_type]

    with mock.patch(patch_target, return_value=str(dummy_file_path)):
        send_email(
            receiver=receiver,
            subject=subject,
            content=content,
            file_content=sample_text,
            file_type=file_type
        )

    mock_smtp.assert_called_once()
    smtp_instance = mock_smtp.return_value
    smtp_instance.starttls.assert_called_once()
    smtp_instance.login.assert_called_once()
    smtp_instance.sendmail.assert_called_once()

    # Decode the email MIME message
    args, kwargs = smtp_instance.sendmail.call_args
    raw_message = args[2]
    parsed_email = email.message_from_string(raw_message)

    attachment_filename = None
    for part in parsed_email.walk():
        if part.get_content_disposition() == "attachment":
            attachment_filename = part.get_filename()
            break

    assert attachment_filename is not None, "No attachment found in the email."
    assert attachment_filename.endswith(expected_extension), f"Attachment extension mismatch: {attachment_filename}"
