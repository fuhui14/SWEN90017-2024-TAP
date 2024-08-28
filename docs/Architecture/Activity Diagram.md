# Transcribtion Aide Platform - Activity Diagram
The activity diagrams visually present a series of actions and flow of control in the system. They illustrate the processes of file upload and transcription, as well as user access to history records and file downloads.

![image](https://github.com/user-attachments/assets/2a08e1bb-375e-4ee9-9fba-e8761e638bf8)

## Activity Diagram Shape Description

| **Shape**                  | **Name**                         | **Meaning**                                                                 | **Examples in The Diagram**                                                                 |
|----------------------------|----------------------------------|------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|
| **Oval (or Ellipse)**       | Start and End Nodes              | Represents the start and end points of the process.                           | Start: The solid oval at the top of the diagram. <br> End: The double-bordered oval at the bottom. |
| **Rectangle**              | Activity or Action               | Depicts activities or actions performed by the user or system.                | "Upload files, set language, email and output format" (User action). <br> "Process uploaded file" (System action). |
| **Diamond**                | Decision Node                    | Represents a decision point where the process flow branches based on a condition. | "Transcribe success?" in the transcription process. <br> "Record expire?" in the history access process. |
| **Horizontal Bar**         | Synchronization Bar (Fork/Join)  | Used to synchronize parallel flows or indicate a split/merge in the process flow. | Used after generating the output file to split the flow into "Send result to user" and "Save result in database". |
| **Arrow (Line)**           | Flow Line                        | Indicates the direction of flow from one activity to the next.                | Connects all shapes to show the order of actions, e.g., from "Upload files" to "Receive result". |

## Activity Diagram Explaination
### **1. "File Upload and Transcription Process"** (Left Diagram)

#### **Description:**

This diagram illustrates the complete process where a user uploads a file and the system performs transcription.

- **User Actions**:
  - The user initiates the process by uploading a file and setting parameters such as language, email, and output format.
  - The system then processes the uploaded file and begins the transcription process.

- **System Actions**:
  - Upon receiving the uploaded file, the system processes it.
  - The system calls the transcription API to convert the audio to text.
  - The system then checks if the transcription was successful:
    - If the transcription is successful, the system invokes a translation API (if applicable) and generates the final output file.
    - If the transcription fails, the system generates an error message.
  - After generating the output file, the system performs two actions:
    - Sends the transcription result to the user via the email provided.
    - Saves the transcription result in the database for future access.
  
- **End**:
  - The user receives the transcription result, and the process concludes.

This diagram outlines the entire process from file upload to transcription completion and result delivery to the user, including handling different scenarios such as successful transcription or failure.

### **2. "User History Access and Download Process"** (Right Diagram)

#### **Description:**

This diagram illustrates the process by which a user accesses their history and downloads previously transcribed files.

- **User Actions**:
  - The user starts by clicking the "History" option and entering their email to request access to their history.
  - The system sends an access link to the user's email.
  - The user receives the link via email and clicks it to access the history records.

- **System Actions**:
  - After receiving the user's request, the system sends a link to access the history records to the user's email.
  - Upon the user clicking the link, the system checks the user's history records:
    - If a record has expired (based on the system's retention policy, e.g., after 30 days), the system removes it from the history.
    - If the record is still valid, the system includes it in the list of available records.
  - The system then displays the history to the user, allowing them to select a file to download.

- **End**:
  - After the user selects a file to download, the system sends the file to the user, and the user receives the file, concluding the process.

This diagram shows how a user securely accesses and manages their transcription history through the system, including handling expired records and file downloads.
