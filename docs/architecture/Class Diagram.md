# Transcription Aide Platform - Class Diagram

The class diagram presented is a visual representation of the core components and their relationships within a transcription system. The system facilitates the upload, processing, and management of audio and video files, converting them into text transcriptions. The primary goal of the system is to streamline the transcription process while ensuring that users can easily upload files, receive transcription results, and access their submission history.

## Class Diagram

![class_diagram](../imgs/Architecture%20diagram/class_diagram.png)

## Class Diagram Explanation

### 1. User
- **Attributes:**
  - `email`: Stores the email address of the user.
- **Methods:**
  - `uploadFile(File file)`: Allows the user to upload a file for transcription.
  - `receiveTranscriptionNotification()`: Allows the user to receive notifications about their transcription status.
- **Relationships:**
  - The `User` class has a one-to-many association with the `File` interface (1..*), meaning a user can upload multiple files.

### 2. File (Interface)
- **Attributes:**
  - `fileID`: A unique identifier for each file.
  - `fileName`: The name of the uploaded file.
  - `fileType`: The type of the file (e.g., "audio" or "video").
  - `uploadDate`: The date when the file was uploaded.
  - `filePath`: The storage path where the file is saved.
  - `status`: The current processing status of the file (e.g., "Pending", "Processing", "Completed").
- **Methods:**
  - `processFile()`: A method to process the file for transcription.
- **Relationships:**
  - The `File` interface is implemented by the `AudioFile` and `VideoFile` classes, indicating that files can be either audio or video types.
  - The `File` class is associated with the `QueueSystem`, where it is added to the queue for processing.

### 3. QueueSystem
- **Attributes:**
  - `queue`: A queue structure holding `File` objects awaiting processing.
  - `maxConcurrent`: The maximum number of files that can be processed simultaneously.
- **Methods:**
  - `addToQueue(File file)`: Adds a file to the processing queue.
  - `processNext()`: Processes the next file in the queue.
  - `currentWaitingLength()`: Returns the number of files currently in the queue.
  -`deletFromQueue(File file)`: Deletes a file from the queue when the user cancels the file.
- **Relationships:**
  - The `QueueSystem` has a one-to-many relationship with the `File` interface, managing the files that need to be processed.

### 4. Transcription
- **Attributes:**
  - `transcriptionID`: A unique identifier for each transcription.
  - `fileID`: Reference to the associated file.
  - `transcriptionText`: The resulting text from the transcription process.
  - `transcriptionDate`: The date when the transcription was completed.
  - `outputFormat`: The format of the transcription output (e.g., "txt" or "docx").
  - `language`: The language of the transcription.
  - `speakers`: A map of speakers, where each speaker is mapped to their corresponding text.
  - `status`: The current status of the transcription (e.g., "Completed", "Failed").
- **Methods:**
  - `generateTranscription()`: Generates the transcription text from the associated file.
  - `identifySpeakers()`: Differentiates and labels different speakers in the transcription.
  - `cancelTranscription(File file)`: Allow the user to cancel the transcription during the process.
- **Relationships:**
  - The `Transcription` class is associated with the `File` interface, indicating that each transcription is generated from a specific file.
  - The `Transcription` class interacts with the `EmailService` class to send the completed transcription to the user.

### 5. EmailService
- **Attributes:**
  - `smtpServer`: The SMTP server used to send emails.
  - `port`: The port used for the email service.
- **Methods:**
  - `sendTranscriptionResult(email: String)`: Sends the transcription result to the user via email.
- **Relationships:**
  - The `EmailService` class interacts with the `Transcription` class to send the transcription results to the user's email.

### 6. History
- **Attributes:**
  - `submissionHistory`: A list of `Transcription` objects representing the user's past transcriptions.
- **Methods:**
  - `viewSubmissionHistory()`: Allows the user to view the history of their submitted transcriptions.
  - `deleteOldTranscriptions()`: Deletes transcriptions that are older than a certain threshold (e.g., 30 days).
- **Relationships:**
  - The `History` class has a one-to-one relationship with the `User` class, representing that a user can access their transcription history.
