

# **Frontend-Backend Integration - Epic 3 (Transcription)**

## **Overview**

This document outlines the integration logic between the frontend (React) and backend (Django REST + Celery) for the core transcription workflow.

# 🔗 Frontend‐Backend Integration – Epic 3: Speaker Diarisation

## 🧩 Overview

When a user uploads a file and selects a speaker-labelled output format, the backend performs speaker diarisation using advanced libraries (Faster-Whisper and PyAnnote Audio). The frontend displays speaker-labeled text blocks in the transcript viewer.

---

## 🖥️ Frontend (React)

- **Trigger**: Same as Epic 2 (`transpage.js`) — user submits a transcription request
- **Format Choice**: If `output_format = diarised`, backend will engage speaker separation logic
- **Result Handling**: Response includes timestamps and speaker IDs (e.g., Speaker 1, Speaker 2), which are rendered in the result page with distinct formatting

## ⚙️ Backend (Django + Celery + PyAnnote)

### 🔹 Main Logic

**File**: `backend/speaker_identify/transcribe_with_speaker_fasterWhisper.py`

### 🔹 Key Processing Steps:

1. 🔄 Convert uploaded file to WAV (if needed)
2. 🔇 Perform noise reduction via `noisereduce` + `librosa`
3. 🧠 Use **PyAnnote Audio** to segment speakers with pretrained HuggingFace pipeline
4. ✍️ Use **Faster-Whisper** for transcription on each segmented part
5. 🧩 Merge segments and relabel each portion with the assigned speaker ID
6. 💾 Store diarised result for frontend display and download

```python
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization",
    use_auth_token=HF_TOKEN
)
diarisation = pipeline(buf)
```
### 🔹 Output Format
The result is stored in structured format:

```
[
{ "start": 0.0, "end": 5.0, "speaker": "Speaker 1", "text": "Hello, welcome..." },
{ "start": 5.0, "end": 12.0, "speaker": "Speaker 2", "text": "Thank you..." },
...
]
```
This data is sent back through the existing transcription task tracking pipeline.

### Summary of Flow
1. User requests diarised format on upload page 
2. Task is routed to diarisation handler on backend 
3. Diarised transcript is processed and stored 
4. Frontend retrieves the result and displays it with speaker annotations

### Notes
- Processing is more resource-intensive due to PyAnnote model size
- CUDA acceleration is used if available (torch.cuda.is_available())
- Diarisation logic is modular and can be bypassed for standard transcription
