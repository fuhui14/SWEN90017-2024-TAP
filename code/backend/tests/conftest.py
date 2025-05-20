import pytest
from unittest import mock

@pytest.fixture
def dummy_audio_file(tmp_path):
    f = tmp_path / "test.wav"
    f.write_bytes(b"dummy audio content")
    return str(f)

@pytest.fixture(autouse=True)
def mock_email_send(monkeypatch):
    monkeypatch.setattr("emails.send_email.send_email", lambda *args, **kwargs: print("Mock email sent"))
