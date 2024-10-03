import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
from config.settings import *
from text_file import text_file
import os


def send_email(receiver, subject, content, file_content, file_type='txt'):
    msg = MIMEMultipart()
    msg['From'] = Header(SMTP_USER, 'utf-8')
    msg['To'] = Header(receiver, 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    body = content
    msg.attach(MIMEText(body + '\n', 'plain', 'utf-8'))
    file = None
    if file_type == 'txt':
        file = text_file(file_content)
    elif file_type == 'file_path':
        file = file_content
    if file_type != 'none':
        if os.path.exists(file):
            with open(file, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(file)}',
                )
                msg.attach(part)
        else:
            print(f"File {file} doesn't exist")

    server = None
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, [receiver], msg.as_string())
        print("succeed")
        if file_type != 'none' and os.path.exists(file):
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
               'This is a test for txt', 'txt')
