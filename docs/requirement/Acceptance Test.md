# Acceptance Test

This section outlines the user-facing flow used to demonstrate acceptance criteria to the client during the final testing meeting.

## Procedure
### 🖥️ 1. Access the Platform
- Navigate to the Transcription Platform website on a local machine 
- Display the landing page with navigation menu and introduction

### 📤 2. Upload Audio File
- Click on Upload or Transcribe
- Select a sample audio file (e.g., .wav or .mp3)
- Confirm the selection and click Submit

### 📶 3. Transcription In Progress
- System shows a loading animation or progress indicator
- Real-time feedback indicates that transcription has started

### 📬 4. Email Input
- Enter a valid email address into the input field
- Verify placeholder text and format validation
- Click Send or Confirm

### ✅ 5. Transcription Result Confirmation
- Display success message: “Transcription completed. The result has been sent to your email.”

### 📂 6. Navigate to History Section
- Click on History from the navigation bar 
- List previously uploaded files with:
  - File name
  - Transcription status
  - Expiry date (human-readable format, e.g., “30 May 2025”)

### 🔍 7. View Transcription Result
- Click on any listed record 
- Display:
  - Speaker-labeled transcript (e.g., Speaker 1, Speaker 2)
  - Timestamps 
  - Diarised segments
- Confirm download option is available (only .txt for now)

## 📝 Notes from Client Feedback (May 30 Meeting)
1. 📅 Date Format: Adjusted to day/month/year for Australian users 
2. 🔘 UI Visibility: Added clearer “Transcribe” button for action prompt 
3. 📤 Download Format: Currently supports .txt; consider .docx or .pdf for future 
4. 🧪 Accuracy: Confirmed FastWhisper is used for better performance over standard Whisper 
5. ⚙️ Deployment: Client asked for minimum hardware specs; provided verbally and in documentation

