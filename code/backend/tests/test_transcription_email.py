# import os
# import sys
# import fitz  # PyMuPDF
# from django.test import TestCase
# from rest_framework.test import APIClient
# from django.core.files.uploadedfile import SimpleUploadedFile
# from unittest.mock import patch
# from emails.send_email import FileType
# from emails.pdf_file import pdf_file
# from emails.text_file import text_file
# from emails.docx_file import docx_file
#
# ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(ROOT_DIR)
#
# class TranscriptionEmailTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.sample_audio_path = os.path.join(os.path.dirname(__file__), "sample.wav")
#
#     def extract_text_from_pdf(self, filepath):
#         with fitz.open(filepath) as pdf:
#             text = ""
#             for page in pdf:
#                 text += page.get_text()
#         return text
#
#     def extract_text_from_txt(self, filepath):
#         with open(filepath, 'r', encoding='utf-8') as f:
#             return f.read()
#
#     def extract_text_from_docx(self, filepath):
#         from docx import Document
#         doc = Document(filepath)
#         return "\n".join([p.text for p in doc.paragraphs])
#
#     def generate_and_check_attachment(self, file_content, file_type):
#         generators = {
#             FileType.PDF: pdf_file,
#             FileType.TXT: text_file,
#             FileType.DOCX: docx_file
#         }
#         extractors = {
#             FileType.PDF: self.extract_text_from_pdf,
#             FileType.TXT: self.extract_text_from_txt,
#             FileType.DOCX: self.extract_text_from_docx
#         }
#         generate = generators[file_type]
#         extract = extractors[file_type]
#         temp_file = generate(file_content)
#         content = extract(temp_file)
#         self.assertIn("Speaker 1", content)
#
#     @patch("transcription.views.process_transcription_and_send_email")
#     @patch("transcription.views.transcribe_audio", return_value="Speaker 1: Hello\nSpeaker 2: Hi")
#     @patch("transcription.views.assign_speakers_to_transcription", return_value="Speaker 1: Hello\nSpeaker 2: Hi")
#     def test_transcription_success_and_email_sent(self, mock_assign, mock_transcribe, mock_process):
#         for output_format, file_type in [("pdf", FileType.PDF), ("txt", FileType.TXT), ("docx", FileType.DOCX)]:
#             with open(self.sample_audio_path, "rb") as f:
#                 sample_file = SimpleUploadedFile("sample.wav", f.read(), content_type="audio/wav")
#
#             response = self.client.post("/transcription/", {
#                 "email": "test@example.com",
#                 "file": sample_file,
#                 "output_format": output_format,
#                 "language": "english"
#             })
#             self.assertEqual(response.status_code, 200)
#             self.generate_and_check_attachment("Speaker 1: Hello\nSpeaker 2: Hi", file_type)
#             mock_process.assert_called()
#             mock_process.reset_mock()
#
#     @patch("transcription.views.send_email")
#     @patch("transcription.views.transcribe_audio", side_effect=Exception("Simulated transcription failure"))
#     def test_transcription_failure_triggers_error_email(self, mock_transcribe, mock_send):
#         with open(self.sample_audio_path, "rb") as f:
#             sample_file = SimpleUploadedFile("sample.wav", f.read(), content_type="audio/wav")
#
#         response = self.client.post("/transcription/", {
#             "email": "fail@example.com",
#             "file": sample_file,
#             "output_format": "pdf",
#             "language": "english"
#         })
#
#         self.assertEqual(response.status_code, 500)
#         mock_send.assert_called_once()
#
#         _, kwargs = mock_send.call_args
#         self.assertEqual(kwargs["receiver"], "fail@example.com")
#         self.assertIn("Failed", kwargs["subject"])
#         self.assertIn("Simulated transcription failure", kwargs["content"])