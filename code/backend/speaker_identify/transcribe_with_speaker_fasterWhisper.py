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
    print("1. load audio and reduce noise...")
    # y_denoised = reduce_noise(wav_fpath)


    nr_kwargs = {
        # FFT 大小（2 的幂次方可加速底层 FFT 实现）
        "n_fft": 2048,                                    # :contentReference[oaicite:1]{index=1}
        # 窗口长度，默认为 n_fft，保持频域分辨率
        "win_length": 2048,                               # :contentReference[oaicite:2]{index=2}
        # 帧移长度，通常取 n_fft 的 1/4 至 1/2
        "hop_length": 512,                                # :contentReference[oaicite:3]{index=3}
        # 噪声减少比例（0.0–1.0），0.8 适中兼顾去噪与保真
        "prop_decrease": 0.8,                             # :contentReference[oaicite:4]{index=4}
        # 关闭静态模式，启用非平稳噪声算法，自动随时间更新门限
        "stationary": False,                              # :contentReference[oaicite:5]{index=5}
        # 非平稳算法的时间常数（秒），控制门限平滑幅度
        "time_constant_s": 2.0,                           # :contentReference[oaicite:6]{index=6}
        # 频域掩码在 Hz 维度的平滑范围
        "freq_mask_smooth_hz": 500,                       # :contentReference[oaicite:7]{index=7}
        # 时域掩码在 ms 维度的平滑范围
        "time_mask_smooth_ms": 50,                        # :contentReference[oaicite:8]{index=8}
        # 静态模式阈值倍数，仅在 stationary=True 时生效
        "n_std_thresh_stationary": 1.5,                   # :contentReference[oaicite:9]{index=9}
    }


    y, sr = librosa.load(wav_fpath, sr=None)      # 保持原采样率
    y_denoised = nr.reduce_noise(y=y, sr=sr, **nr_kwargs)     # 频谱门控降噪

    # 2. 将降噪后音频写入内存缓冲（WAV 格式）
    buf = io.BytesIO()
    sf.write(buf, y_denoised, sr, format="WAV")
    buf.seek(0)

    # 3. 说话人分离
    print("2. 执行说话人分离…")
    if torch.cuda.is_available():
        diarizer_device = "cuda"
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        diarizer_device = "mps"
    else:
        diarizer_device = "cpu"
    print(f"Pyannote device used: {diarizer_device}")

    diarizer = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        #use_auth_token=HF_TOKEN
    ).to(torch.device("cpu"))
    # 直接使用内存流进行分离
    diarization = diarizer({"uri": "meeting", "audio": wav_fpath})
    # 提取每个分段 (start, end, speaker)
    segments = [(turn.start, turn.end, spk)
                for turn, _, spk in diarization.itertracks(yield_label=True)]
    if not segments:
        print("Warning: 没有检测到任何说话人片段。")

    # 4. 依次转录每段并显示进度
    print("3. 转录并显示进度…")
    whisper_device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Whisper device used: {whisper_device}")
    model = WhisperModel("medium", device=whisper_device, compute_type="int8")
    transcripts = []
    total_duration = segments[-1][1]  # 以最后一段的 end 作为总时长估计

    with tqdm(total=total_duration, unit="s", desc="转录进度") as pbar:
        elapsed = 0.0
        for start, end, speaker in segments:
            # 从缓冲中读取对应片段
            buf.seek(0)
            data, _ = sf.read(buf,
                                dtype="float32",
                                start=int(start * sr),
                                stop=int(end * sr))
            buf2 = io.BytesIO()
            sf.write(buf2, data, sr, format="WAV")
            buf2.seek(0)

            # 转录
            segments_out, info = model.transcribe(
                buf2,
                beam_size=5,
                initial_prompt="meeting record",  # 可根据领域调整
                word_timestamps=False,
                log_progress=False               # 这是针对于每一个segment的个人进度，整体已由外层 tqdm 打印
            )
            text = " ".join(seg.text for seg in segments_out)

            # 更新进度条
            pbar.update(end - elapsed)
            elapsed = end
            pbar.set_postfix_str(f"Speaker {speaker}")

            # 处理转录结果
            if not re.search(r'\w', text):
                print(f"Warning: 转录结果为空，可能是音频片段过短或无语音。")
                continue
            # 合并相同说话人的文本
            if (transcripts != [] and speaker == transcripts[-1][2]):
                # 如果当前说话人与上一个相同，则合并文本
                transcripts[-1] = (
                    transcripts[-1][0],
                    end,
                    speaker,
                    transcripts[-1][3] + " " + text
                )
            else:
                # 否则添加新记录
                transcripts.append((start, end, speaker, text))

    print(transcripts)

    # 5. 打印最终结果
    print("\n=== 转录与分离结果 ===")
    for start, end, spk, txt in sorted(transcripts, key=lambda x: x[0]):
        print(f"[{start:.2f}-{end:.2f}] Speaker {spk}: {txt}")

    return transcripts


def convert_to_wav(file_path):
    try:
        file_name = os.path.splitext(file_path)[0]
        output_file = f"{file_name}.wav"
        audio = AudioSegment.from_file(file_path)
        audio.export(output_file, format="wav")
        return output_file
    except Exception as e:
        print(e)
        return None