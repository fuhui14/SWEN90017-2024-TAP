# Transcribtion Aide Platform - UML Sequence Diagram
This diagram illustrates the user interactions with the transcription system, including uploading files, performing transcription and translation, accessing previous records, and downloading past files.

## UML Sequence Diagram

![alt text](<Sequence diagram.png>)

## Sequence Diagram Shape Description

| **Shape**              | **Name**                   | **Meaning**                                                                                          | **Examples in The Diagram**                                                                            |
|------------------------|----------------------------|-------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------|
| **Stick Figure**        | Actor                      | Represents a user or an external system that interacts with the process.                               | The stick figure labeled "Actor" represents the user interacting with the transcription system.           |
| **Rectangle**           | Lifeline                  | Represents the lifespan of an object or participant in the process over time.                          | The rectangles labeled "UI," "Transcription," "File," "emailService," "QueueSystem," and "History."      |
| **Arrow (Dashed Line)** | Message or Communication  | Indicates a message or communication between participants, showing the flow of information.            | The dashed arrows between lifelines, such as "Click Transcription Button" and "Upload a file."           |
| **Solid Arrow Line**    | Synchronous Message       | Represents a call for action or a request from one participant to another that expects an immediate response. | Arrows connecting actions like "Show Success Message" or "Go processing page."                         |
| **Rectangle (Alt Box)** | Alternative Fragment      | Shows conditional logic or an alternative flow within the sequence.                                    | The "Alt" box around "file uploaded" or "file not uploaded" shows alternative paths based on conditions. |
| **Brackets**            | Condition                 | Represents a specific condition that needs to be met for an action to occur.                            | The conditions within brackets such as "[file uploaded]" or "[error]."                                  |
| **Vertical Bar**        | Activation Bar            | Indicates when a particular object is active or controlling the process at that time.                   | The narrow vertical bars along each lifeline, like during "Process the file" or "Show Transcription Page."|

## Sequence Diagram Explanation
### **1. "File Upload and Transcription Process"** (Left Side of the Diagram)

#### **Description:**

This sequence diagram details the entire process where a user interacts with the system to upload a file and have it transcribed.

- **User Actions**:
  - The user starts the process by clicking the transcription button, uploading a file, and setting parameters such as the transcription language and email.
  - The user may encounter a scenario where the file upload is successful or fails, prompting either a success or error message.

- **System Actions**:
  - Once the file is successfully uploaded, the system moves to the transcription page and starts processing the file.
  - The system performs the transcription based on the language set by the user.
  - After transcription is complete, the system displays the transcription result to the user.
  - The user is then given the option to download the transcription result.

- **End**:
  - The process ends when the user downloads the transcribed file and closes the page, marking the completion of the transaction.

This diagram covers the interaction between the user and the system, illustrating how a file is uploaded, processed, transcribed, and then delivered back to the user.

### **2. "User History Access and Download Process"** (Right Side of the Diagram)

#### **Description:**

This sequence diagram describes how a user accesses their history of previously transcribed files and downloads them.

- **User Actions**:
  - The user starts by clicking on the "History" option within the system's interface.
  - Upon accessing the history page, the user can view previous transcriptions and select any file for download.

- **System Actions**:
  - The system retrieves the user's history records and displays them on the history page.
  - The user’s request to download a file is processed by the system, which then delivers the file.
  - If there are no available history records or an issue with the retrieval, the system notifies the user accordingly.

- **End**:
  - The process concludes once the user successfully downloads the selected file from their history, and the page is closed.

This diagram showcases how a user can access their transcription history, manage past records, and download files as needed.

