# Transcription Aide Platform - UML Sequence Diagram
This diagram illustrates the user interactions with the transcription system, including uploading files, performing transcription and translation, accessing previous records, and downloading past files.

## UML Sequence Diagram

![alt text](<../imgs/Architecture diagram/Sequence diagram.png>)


## Sequence Diagram Shape Description

| **Shape**              | **Name**                   | **Meaning**                                                                                          | **Examples in The Diagram**                                                                            |
|------------------------|----------------------------|-------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------|
| **Stick Figure**        | Actor                      | Represents a user or an external system that interacts with the process.                               | The stick figure labeled "Actor" represents the user interacting with the transcription system.           |
| **Rectangle**           | Lifeline                  | Represents the lifespan of an object or participant in the process over time.                          | The rectangles labeled "UI," "Transcription," "File," "emailService," "QueueSystem," and "History."      |
| **Dashed Line Arrow** | Message or Communication  | Indicates a message or communication between participants, showing the flow of information.            | The dashed arrows between lifelines, such as "Show Success Message" and "File Uploaded"           |
| **Solid Arrow Line**    | Synchronous Message       | Represents a call for action or a request from one participant to another that expects an immediate response. | Arrows connecting actions like "addFileToQueue(file1)" or "Click Confirm Button"                         |
| **Rectangle (Alt Box)** | Alternative Fragment      | Shows conditional logic or an alternative flow within the sequence.                                    | The "Alt" box around "file uploaded" or "file not uploaded" shows alternative paths based on conditions. |
| **Brackets**            | Condition                 | Represents a specific condition that needs to be met for an action to occur.                            | The conditions within brackets such as "[file uploaded]" or "[error]."                                  |
| **Vertical Bar**        | Activation Bar            | Indicates when a particular object is active or controlling the process at that time.                   | The narrow vertical bars along each lifeline, like during "Process the file" or "Show Transcription Page."|

## Sequence Diagram Explanation
### **1. "File Upload and Transcription Process"** (Left Side of the Diagram)

#### **Description:**

This sequence diagram details the entire process where a user interacts with the system to upload a file and have it transcribed.

- **User Actions**:
  - The user clicks on the "Transcription" button, uploads a file, and selects parameters such as transcription language and an optional email.
  - The user receives feedback based on whether the file upload is successful or results in an error.

- **System Actions**:
  - After confirming the action, the system sends the file and parameters to the queue system for processing.
  - The system processes the file once there is available capacity in the queue, executing transcription based on the selected language.
  - Once transcription is complete, the system displays the results on the page and sends a copy of the transcription via email.
- **End**:
  - The process ends when the user downloads the transcribed file and closes the page, marking the completion of the transaction.


### **2. "User History Access and Download Process"** (Right Side of the Diagram)

#### **Description:**

This sequence diagram describes how a user accesses their history of previously transcribed files and downloads them.

- **User Actions**:
  - The user navigates to the "History" section, where they need to input their email to retrieve access to past records.
  - Upon accessing the history page, the user selects any previously processed file for download.

- **System Actions**:
  - The system retrieves the user’s transcription history, displaying it on the history page.
  - The user’s request to download a file is processed, and the file is delivered to the user for download.
  - If the system cannot retrieve the history or an error occurs, an appropriate error message is shown.

- **End**:
  - The process ends when the user downloads a file and exits the page.


