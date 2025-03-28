from resemblyzer import preprocess_wav, VoiceEncoder
from pathlib import Path
from spectralcluster import SpectralClusterer
import whisper
from pathlib import Path
import torch
from .identify_service import *

def transcribe_with_speaker_resemblyzer(audioPath):
    # give the file path to your audio file
    audio_file_path = convert_to_wav(audioPath)
    wav_fpath = Path(audio_file_path)

    wav = preprocess_wav(wav_fpath)

    if torch.cuda.is_available():
        device = "cuda"
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"
    encoder = VoiceEncoder(device)

    _, cont_embeds, wav_splits = encoder.embed_utterance(wav, return_partials=True, rate=16)
    print("Embedding shape:", cont_embeds.shape)

    clusterer = SpectralClusterer(
        min_clusters=2,
        max_clusters=100)
    labels = clusterer.predict(cont_embeds)

    # create labelling
    labelling = create_labelling(labels,wav_splits)

    # start transcribing
    model = whisper.load_model("base")
    transcription = []

    for seg in labelling:
        speaker, seg_start, seg_end = seg
        seg_filename = f"segment_{speaker}_{seg_start:.2f}_{seg_end:.2f}.wav"
        print(f"Processing segment: {seg_filename} ({seg_start:.2f}s - {seg_end:.2f}s)")
        trim_audio(audio_file_path, seg_filename, seg_start, seg_end)
        # use Whisper to transcribe the segment
        result = model.transcribe(seg_filename)
        transcript_text = result["text"].strip()
        # save the transcript
        transcription.append({
            "speaker": speaker,
            "text": transcript_text,
            "start": seg_start,
            "end": seg_end
        })

    print("Final Transcription:\n", transcription)

    #remove the temporary segment files
    for seg in labelling:
        speaker, seg_start, seg_end = seg
        seg_filename = f"segment_{speaker}_{seg_start:.2f}_{seg_end:.2f}.wav"
        if Path(seg_filename).exists():
            Path(seg_filename).unlink()
        print(f"Deleted temporary file: {seg_filename}")
    
    return transcription