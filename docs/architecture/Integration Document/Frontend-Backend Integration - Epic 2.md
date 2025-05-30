

# **Frontend-Backend Integration - Epic 2 (Transcription)**

## **Overview**

This document outlines the integration logic between the frontend (React) and backend (Django REST + Celery) for the core transcription workflow.

# 🔗 Frontend‐Backend Integration – Epic 2: Transcription


## 🧩 Overview

When a user uploads audio files for transcription, the frontend initiates asynchronous requests to the backend to:

- Upload files and create transcription tasks
- Track the progress of each task
- Display status and results dynamically in the UI

---

## 🖥️ Frontend (React)

**Main file**: `src/transcription/transpage.js`

### 🔹 Key States & Hooks

- `email`: Stores user email for result delivery
- `files`: Tracks uploaded files
- `tasks`: Stores task metadata (taskId, progress, status, result)

### 🔹 Upload Logic

Upon file selection:
```js
const formData = new FormData();
formData.append("file", file);
formData.append("email", email);
formData.append("language", lang);
formData.append("output_format", format);
```
A POST request is sent to:
```js
fetch('/api/upload/', {
  method: 'POST',
  headers: { 'X-CSRFToken': getCookie('csrftoken') },
  body: formData
})
```

### 🔹 Progress Polling
Tasks are periodically polled with:
```js
fetch(`/api/status/?task_ids=${taskIds.join(',')}`)
```
Response updates each task’s progress and final result.

## ⚙️ Backend (Django + Celery)
### 🔹 Upload Endpoint
URL: /api/upload/
View: FileUploadAPIView (in transcription/views.py)

Processes uploaded file and enqueues transcription job:
```python
task = transcribe_audio_task.delay(file_path, email, lang, format)
```
### 🔹 Status Endpoint
URL: /api/status/
Returns:
```
[
{
"task_id": "...",
"progress": 85,
"status": "IN_PROGRESS",
"result": null
},
...
]
```
Handled by custom task tracker in Celery backend.

## 🔁 Summary of Flow
- User uploads file → frontend posts to /api/upload/
- Backend enqueues task and returns task ID
- Frontend polls /api/status/ every few seconds
- UI updates task status (e.g., progress bar, download link)

## Notes
- Error handling and timeout logic are implemented in transpage.js
- Supports multiple concurrent files and task tracking
- CSRF tokens handled via helper (getCookie)
