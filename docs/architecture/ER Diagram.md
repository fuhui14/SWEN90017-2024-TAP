# Transcription Aide Platform - ER Diagram

The ER diagram presented illustrates the core components and their relationships within a transcription system designed to handle audio and video file transcriptions. The primary goal of this system is to efficiently manage file uploads, process transcriptions, and handle details regarding various speakers within the transcriptions.

## ER Diagram

![ER Diagram](../imgs/Architecture%20diagram/ER_Diagram.png)

## ER Diagram Explanation

### 1. File

**Attributes:**

- `fileID` (PK): A unique identifier for each file.
- `fileName`: The name of the uploaded file.
- `fileType`: The type of the file (e.g., "audio" or "video").
- `uploadDate`: The date when the file was uploaded.
- `filePath`: The storage path where the file is saved.
- `status`: The current processing status of the file (e.g., "Pending", "Processing", "Completed").
- `uploaderEmail`: The email address of the user who uploaded the file.

**Relationships:**

- The File entity is directly associated with the Transcription entity through a one-to-one relationship, indicating that each file can have exactly one transcription associated with it.

### 2. Transcription

**Attributes:**

- `transcriptionID` (PK): A unique identifier for each transcription.
- `fileID` (FK): Reference to the associated file, linking back to the File entity.
- `transcriptionText`: The resulting text from the transcription process.
- `transcriptionDate`: The date when the transcription was completed.
- `outputFormat`: The format of the transcription output (e.g., "txt" or "docx").
- `language`: The language of the transcription.
- `status`: The current status of the transcription (e.g., "Completed", "Failed").
- `uploaderEmail`: Email of the user who requested the transcription, mirroring from the File entity.

**Relationships:**

- Each Transcription is linked to multiple SpeakingEvents through a one-to-many relationship, facilitating the association of multiple speaker segments within a single transcription.

### 3. SpeakingEvent

**Attributes:**

- `transcriptionID` (FK): Foreign key that links to the Transcription entity.
- `speakerName`: The name of the speaker.
- `startTime`: The starting time of the speaking event within the file.
- `endTime`: The ending time of the speaking event within the file.

**Relationships:**

- The SpeakingEvent entity captures individual speaking segments within a transcription, associated with a specific Transcription through its foreign key.
