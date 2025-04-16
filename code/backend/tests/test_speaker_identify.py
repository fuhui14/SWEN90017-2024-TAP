import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from speaker_identify.identify_service import transcribe_with_speaker

@patch("speaker_identify.transcribe_with_speaker_resemblyzer.subprocess.run")
@patch("speaker_identify.transcribe_with_speaker_resemblyzer.convert_to_wav")
@patch("speaker_identify.transcribe_with_speaker_resemblyzer.VoiceEncoder")
@patch("speaker_identify.transcribe_with_speaker_resemblyzer.SpectralClusterer")
@patch("speaker_identify.transcribe_with_speaker_resemblyzer.whisper.load_model")
@patch("speaker_identify.transcribe_with_speaker_resemblyzer.preprocess_wav")
def test_transcribe_with_speaker_flow(
    mock_preprocess_wav,
    mock_load_model,
    mock_spectral_clusterer,
    mock_voice_encoder,
    mock_convert_to_wav,
    mock_subprocess_run,
    tmp_path
):
    """
    Simulate the full flow of speaker transcription using mocks.
    """

    # Setup dummy wav path
    fake_input_path = str(tmp_path / "fake_input.mp3")
    fake_wav_path = str(tmp_path / "converted.wav")

    mock_convert_to_wav.return_value = fake_wav_path
    mock_preprocess_wav.return_value = "mock_wav"

    # Mock encoder.embed_utterance
    mock_encoder_instance = MagicMock()
    mock_encoder_instance.embed_utterance.return_value = (
        None,
        np.array([[0.1]*256, [0.2]*256]),
        [slice(0, 1000), slice(1000, 2000)]
    )
    mock_voice_encoder.return_value = mock_encoder_instance

    # Mock clusterer.predict
    mock_clusterer_instance = MagicMock()
    mock_clusterer_instance.predict.return_value = [0, 1]
    mock_spectral_clusterer.return_value = mock_clusterer_instance

    # Mock whisper transcription result
    mock_model_instance = MagicMock()
    mock_model_instance.transcribe.return_value = {"text": "Hello world"}
    mock_load_model.return_value = mock_model_instance

    # Mock subprocess.run to avoid FileNotFoundError from missing ffmpeg
    mock_subprocess_run.return_value = None

    # Call actual function
    result = transcribe_with_speaker(fake_input_path)

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["text"] == "Hello world"