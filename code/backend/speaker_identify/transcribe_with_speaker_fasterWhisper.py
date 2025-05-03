import io
import os
from pydub import AudioSegment
from pathlib import Path

import librosa                                # load audio
import noisereduce as nr                      # noise reduction algorithm :contentReference[oaicite:0]{index=0}
import soundfile as sf                        # read/write audio files
import torch
from pyannote.audio import Pipeline           # speaker identification pipline :contentReference[oaicite:1]{index=1}
from faster_whisper import WhisperModel       # faster Whisper deduction :contentReference[oaicite:2]{index=2}
from tqdm import tqdm
import re


def transcribe_with_speaker_fasterWhisper(audioPath):
    """
    Transcribe audio with speaker identification using faster-whisper and pyannote.
    :param audio_path: Path to the input audio file.
    :return: List of tuples containing start time, end time
    """

    # 0. convert to wav
    audio_file_path = convert_to_wav(audioPath)
    wav_fpath = Path(audio_file_path)

    # 1. load audio and reduce noise
    print(f"Loading audio file: {wav_fpath}...")
    y_denoised, sr = reduce_noise(wav_fpath)
    
    # 2. write to buffer
    buf = io.BytesIO()
    sf.write(buf, y_denoised, sr, format="WAV")
    buf.seek(0)
    print("Audio loaded and noise reduced.")

    # 3. speaker diarization
    print("Processing speaker diarization...")
    if torch.cuda.is_available():
        diarizer_device = "cuda"
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        diarizer_device = "mps"
    else:
        diarizer_device = "cpu"
    print(f"Pyannote device used: {diarizer_device}")
    # load the pre-trained model
    diarizer = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        #use_auth_token=HF_TOKEN
    ).to(torch.device("cpu"))
    # we use wav file path instead of buffer because the original file is more accurate
    diarization = diarizer({"uri": "meeting", "audio": wav_fpath})
    # extract segments with speaker labels
    segments = [(turn.start, turn.end, spk)
                for turn, _, spk in diarization.itertracks(yield_label=True)]
    if not segments:
        print("Warning: No segments found. Please check the audio file.")
        return []
    print("Speaker diarization completed.")


    # 4. for each segment, transcribe and show progress
    print("Transcribing segments...")
    # no mps support for faster_Whisper yet
    whisper_device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Whisper device used: {whisper_device}")
    model = WhisperModel("medium", device=whisper_device, compute_type="int8")
    transcripts = []
    total_duration = segments[-1][1]  # use the end time of the last segment

    with tqdm(total=total_duration, unit="s", desc="transcription progress") as pbar:
        elapsed = 0.0
        for start, end, speaker in segments:
            # for each segment, we need to read the audio data from the buffer
            buf.seek(0)
            data, _ = sf.read(buf,
                                dtype="float32",
                                start=int(start * sr),
                                stop=int(end * sr))
            buf2 = io.BytesIO()
            sf.write(buf2, data, sr, format="WAV")
            buf2.seek(0)

            # transcribe the segment
            # here the parameters are set to default values
            segments_out, info = model.transcribe(
                buf2,
                beam_size=5,
                initial_prompt="meeting record",  # can change to other prompts
                word_timestamps=False,
                log_progress=False  # this is for the segment progress, the overall progress is printed by the outer tqdm
            )
            text = " ".join(seg.text for seg in segments_out)

            # update the progress bar
            pbar.update(end - elapsed)
            elapsed = end
            pbar.set_postfix_str(f"Speaker {speaker}")

            # add the transcript to the list
            transcripts.append((start, end, speaker, text))
    
    # clean up the transcripts
    transcripts = cleanup_transcripts(transcripts)

    # format the transcripts
    transcripts = format_transcripts(transcripts)

    # print the results
    print("\n=== Transcription Results: ===")
    for start, end, spk, txt in sorted(transcripts, key=lambda x: x[0]):
        print(f"[{start:.2f}-{end:.2f}] Speaker {spk}: {txt}")

    return transcripts


def convert_to_wav(file_path):
    """
    Convert audio file to WAV format using pydub.
    """
    try:
        file_name = os.path.splitext(file_path)[0]
        output_file = f"{file_name}.wav"
        audio = AudioSegment.from_file(file_path)
        audio.export(output_file, format="wav")
        return output_file
    except Exception as e:
        print(e)
        return None
    

def reduce_noise(wav_fpath):
    """
    Use noisereduce to reduce noise in the audio file.
    """
    nr_kwargs = {
        "n_fft": 2048,                                    # :contentReference[oaicite:1]{index=1}
        "win_length": 2048,                               # :contentReference[oaicite:2]{index=2}
        "hop_length": 512,                                # :contentReference[oaicite:3]{index=3}
        "prop_decrease": 0.8,                             # :contentReference[oaicite:4]{index=4}
        "stationary": False,                              # :contentReference[oaicite:5]{index=5}
        "time_constant_s": 2.0,                           # :contentReference[oaicite:6]{index=6}
        "freq_mask_smooth_hz": 500,                       # :contentReference[oaicite:7]{index=7}
        "time_mask_smooth_ms": 50,                        # :contentReference[oaicite:8]{index=8}
        "n_std_thresh_stationary": 1.5,                   # :contentReference[oaicite:9]{index=9}
    }

    y, sr = librosa.load(wav_fpath, sr=None)      # keep original sample rate
    y_denoised = nr.reduce_noise(y=y, sr=sr, **nr_kwargs)     # apply noise reduction
    return y_denoised, sr


def cleanup_transcripts(transcripts):
    """
    Clean up the transcripts by removing empty segments and combining consecutive segments with the same speaker.
    """
    cleaned_transcripts = []
    for start, end, speaker, text in transcripts:
        # remove segments with no text
        if not re.search(r'\w', text):
            print(f"Warning: Speaker {speaker} at [{start:.2f}-{end:.2f}] has no text. Skipping.")
            continue
        # combine consecutive segments with the same speaker
        if (cleaned_transcripts != [] and speaker == cleaned_transcripts[-1][2]):
            # if the last segment is the same speaker, combine them
            cleaned_transcripts[-1] = (
                cleaned_transcripts[-1][0],
                end,
                speaker,
                cleaned_transcripts[-1][3] + " " + text
            )
        else:
            # else, add a new segment
            cleaned_transcripts.append((start, end, speaker, text))
    return cleaned_transcripts


def format_transcripts(transcripts):
    """
    format the transcripts to unify the format
    format: {
        "start": start_time,
        "end": end_time,
        "speaker": speaker_id,
        "text": text
    }
    where start_time and end_time are in seconds with 2 decimal places
    and speaker_id is an integer starting from 1.
    """
    formatted_transcripts = []
    for start, end, speaker, text in transcripts:
        # format the start and end times to 2 decimal places
        start = f"{start:.2f}"
        end = f"{end:.2f}"
        # speaker count starts from 1
        speaker = int(speaker.split("_")[-1]) + 1
        # format the text to remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        formatted_transcripts.append({
            "start": start, 
            "end": end, 
            "speaker": speaker, 
            "text": text
        })
    return formatted_transcripts