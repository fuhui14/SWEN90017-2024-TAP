import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
from enum import Enum

from config.settings import *
from text_file import text_file
from docx_file import docx_file
from pdf_file import pdf_file
import os


class FileType(Enum):
    NONE = 1
    PATH = 2
    TXT = 3
    DOCX = 4
    PDF = 5


# file_type {'txt', 'file_path', 'none'}
# TXT means encode the file_content into a txt file and send to the receiver
# PATH means the file_content is the path of the attached file
# NONE means no file attached
def send_email(receiver, subject, content, file_content, file_type=FileType.TXT):
    if not isinstance(file_type, FileType):
        file_type = FileType.NONE
        print("file_type format error: file_type has been set to NONE")
    msg = MIMEMultipart()
    msg['From'] = Header(SMTP_USER, 'utf-8')
    msg['To'] = Header(receiver, 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    body = content
    msg.attach(MIMEText(body + '\n', 'plain', 'utf-8'))
    file = None
    if file_type == FileType.TXT:
        file = text_file(file_content)
    elif file_type == FileType.DOCX:
        file = docx_file(file_content)
    elif file_type == FileType.PDF:
        file = pdf_file(file_content)
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
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, [receiver], msg.as_string())
        print("succeed")
        if file is not None and os.path.exists(file):
            try:
                os.remove(file)
            except Exception as e:
                print(f"error: {e}")
    except Exception as e:
        print(f"error: {e}")
    finally:
        server.quit()


if __name__ == "__main__":
    send_email('yupengyuanchina@gmail.com', 'test', 'test with file',
               'This is a test for pdf', FileType.DOCX)
