import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
from enum import Enum
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.conf import settings
from emails.text_file import text_file
from emails.docx_file import docx_file
from emails.pdf_file import pdf_file


class FileType(Enum):
    NONE = 1
    PATH = 2
    TXT = 3
    DOCX = 4
    PDF = 5


def format_content(content):
    if isinstance(content, dict) and "message" in content:
        return content["message"]
    elif isinstance(content, list):
        return "\n".join(content)
    return content

def send_email(receiver, subject, content, file_content, file_type=FileType.TXT):
    if not isinstance(file_type, FileType):
        file_type = FileType.NONE
        print("file_type format error: file_type has been set to NONE")
    msg = MIMEMultipart()
    msg['From'] = Header(settings.SMTP_USER, 'utf-8')
    msg['To'] = Header(receiver, 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    body = content
    msg.attach(MIMEText(body + '\n', 'plain', 'utf-8'))
    file = None
    formatted_content = format_content(file_content)
    if file_type == FileType.TXT:
        file = text_file(formatted_content)
    elif file_type == FileType.DOCX:
        file = docx_file(formatted_content)
    elif file_type == FileType.PDF:
        file = pdf_file(formatted_content)
    elif file_type == FileType.PATH:
        file = file_content
    if file is not None and os.path.exists(file):
        with open(file, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {os.path.basename(file)}',
            )
            msg.attach(part)
    elif file is not None:
        print(f"File {file} doesn't exist")

    server = None
    try:
        server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT, timeout=10)
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_USER, [receiver], msg.as_string())
        print("Email sent successfully")
        if file is not None and os.path.exists(file):
            try:
                os.remove(file)
            except Exception as e:
                print(f"Error deleting file: {e}")
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        if 'server' in locals() and server:
            server.quit()


if __name__ == "__main__":
    send_email('garciayfh@gmail.com', 'test', 'test with file',
               {'message': 'This is a test for pdf', 'status': 'success'}, FileType.PDF)