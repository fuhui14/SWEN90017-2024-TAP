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
  - The `User` class has a one-to-many association with the `File` interface, meaning a user can upload multiple files.


### 2. QueueSystem
- **Attributes:**
  - `waitingQueue`: Queue of `Files`
  - `estimatedWaitingTime`: Time (available runtime of the system)
  - `maxConcurrentRuns`: int (maximum number of concurrent file processing)
- **Methods:**
  - `addFileToQueue(File)`: Adds a file to the processing queue.
  - `convertWaitingLength()`: Converts the waiting queue into a processing state.
  - `processNextInQueue()`: Processes the next file in the queue.
  - `deleteFromQueue(File)`: Deletes a file from the queue.
- **Relationships:**
  - The `QueueSystem` has a one-to-many relationship with the `File` interface, managing the files that need to be processed.
  - The `QueueSystem` has a one-to-many relationship with the `Transcription` class, which performs the actual transcription process.


### 3. File (Interface)
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
- **Inheritance**:
  - This class serves as a parent class to AudioFile and VideoFile subclasses (but they don't seem to have specific attributes or methods in the diagram).



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
  - `processingProgress`: int (progress of the transcription)
  - `errorReports`: List of Errors
- **Methods:**
  - `generateTranscription()`: Generates the transcription text from the associated file.
  -  `generateTranslation()`: Generates the translation of the transcription text to a specified language.
  - `identifySpeakers()`: Differentiates and labels different speakers in the transcription.
  - `cancelTranscription(File file)`: Allow the user to cancel the transcription during the process.
- **Relationships:**
  - The `Transcription` class interacts with the `EmailService` class to send the completed transcription to the user.
  - The `Transcription` class is associated with the `HistoryRecord` class, which stores the history of transcriptions.



### 5. EmailService
- **Attributes:**
  - `smtpServer`: The SMTP server used to send emails.
  - `port`: The port used for the email service.
- **Methods:**
  - `sendTranscriptionResult(email: String)`: Sends the transcription result to the user via email.
- **Relationships:**
  - The `EmailService` class interacts with the `Transcription` class to send the transcription results to the user's email.



### 6. HistoryRecord
- **Attributes:**
  - `file`: Reference to the associated file.
  - `expireTime`: The time when the record will expire.
  - `email`: The email address of the user.
- **Relationships:**
  - The `History` class has a one-to-one relationship with the `User` class, representing that a user can access their transcription history.



### 7. FileManager
- **Attributes:**
  - `historyRecords`: List of HistoryRecord
- **Methods:**
  - `viewSubmissionHistory()`: Views the history of submissions.
  - `viewFileFromHistory()`: Views a file from the submission history.
  - `downloadFileFromRecord()`: Downloads the file from a particular record.
- **Relationships:**
  - The `FileManager` class interacts with the `HistoryRecord` class to manage and access the transcription history.

