

# **Frontend-Backend Integration - Epic 4 (File Management)**

## **Overview**

This document outlines the integration logic between the frontend (React) and backend (Django REST + Celery) for the core transcription workflow.

# 🔗 Frontend‐Backend Integration – Epic 4: File Management

## 🧩 Overview

Users receive a secure encrypted link via email that directs them to the file history page. The frontend uses this encrypted token to fetch the user's past transcription records and enables file downloads.

## 🖥️ Frontend (React)

**Main file**: `src/history/history.js`

### 🔹 Key States & Hooks

- `searchParams`: Parses the `enc` query parameter from the URL
- `historyData`: Stores the list of transcription records
- `loading`, `error`: For feedback and exception handling

### 🔹 Fetch History Logic

```js
const encrypted = searchParams.get('enc');
fetch("http://127.0.0.1:8000/history/api/admin/history/", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ enc: encrypted }),
})
```
- Retrieves transcription record list from backend
- Sorted by creation date (newest to oldest)
- Response data used to populate the history UI

### 🔹 Download File
Each listed item includes a download icon:
```
<a href={downloadURL} download>...</a>
```

## ⚙️ Backend (Django)
### 🔹 History Endpoint
URL: /history/api/admin/history/
Method: POST
Input:
```
{ "enc": "<encrypted_token>" }
```
Output:
```
[
  {
    "filename": "meeting.mp3",
    "status": "Completed",
    "creationDate": "...",
    "downloadURL": "...",
    "expires": "..."
  },
  ...
]
```
- Token is decrypted server-side to identify user
- Expired or invalid tokens are rejected
- Results are filtered by user ID and sorted by date

### Summary of Flow

1. User clicks link with ?enc=... parameter 
2. Frontend sends encrypted token to backend 
3. Backend authenticates and returns history 
4. User sees a list of transcription records 
5. Clickable download links provided for available files

### Notes
- Pagination implemented (10 files per page)
- Expiration info shown in the UI
- Robust error handling for expired/missing tokens