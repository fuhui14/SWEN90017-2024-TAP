# Transcription Aide Platform - Use Case Diagram

The use case diagram presented is a visual representation of the functional requirements and the interactions between the user and the Transcription Aide Platform. The diagram illustrates the key actions a user can perform within the system, such as uploading files, selecting transcription languages, choosing output formats, and managing results. It also shows how the system responds by providing options like receiving results, handling errors, and allowing users to download or delete results. The primary purpose of this diagram is to ensure that the system's functionalities and the user's interactions are clearly defined and understood.

## Use Case Diagram

![Use Case Diagram](../imgs/Architecture%20diagram/Use_Case_Diagram.png)

## Use Case Diagram Relationship Type Description

| **Relationship Type** | **Description** | **Symbol Representation**                    |
|------------------------|----------------------------|-------------------------------------------------------------------------------------------------------|
| **Association** | Relationship between an actor and a use case                      | **Actor" **————** "Use case"       |
| **Generalization** | Relationship between actors or<br>between parent and child use cases                  |       "Parent use case" **<————** "Child use cases"  |
| **Include** | Relationship between use cases<br>(the included use case always executes)  | "Confirm" **--<<<include>include>>-->** "Receive the Results"  |
| **Extend** | Relationship between use cases<br>(the extended use case executes only under certain conditions)       | "Receive Error Reports" **--<<<extend>extend>>-->** "Confirm"  |

## Use Case Diagram Explanation

### 1. System
- **Transcription Aide Platform**
  - Represented by a large rectangle, labeled with the system name, defining the scope of the system.

### 2. Actor
Represented by a small stick figure. 
The actor is an external entity and is placed outside the system (the large rectangle).
- **User**
  - The primary participant.
- **Email**
  - The Secondary participant.
 
### 3. Use Case
Represented by an oval shape, placed inside the rectangle, indicating actions that occur within the application.
- **Input Email Adress**
  - The user enters their email address to receive the transcript results.
- **Select Output File Format**
  - The user can choose the desired file format for the output.
  - Here are some child use cases representing the available formats, such as .doc, .txt, etc.
- **Select Transcription Language**
  - The user can choose the desired output language, which refers to the transcription result translated into the target language.
  - Here are some child use cases representing the available languages, such as English, Spanish, etc.
- **Upload the File**
  - The user uploads the files to be transcribed.
  - They can be an audio or video files.
  - The uploaded file can also be deleted by the user.
- **Confirm**
  - After completing the above actions, the user clicks ‘Confirm’ to submit the uploaded file to the system for transcription.
  - The user will automatically receive the transcription results via the provided email once the transcription is complete.
  - If there is an issue with the transcription, the user will also automatically receive an Error Report via the provided email.
- **View History Result**
  - The user enters the email address for which they want to view historical transcription results.
  - On the history page, the user can manually download past transcription results or completely delete them.

### 4. Relationship
For a detailed explanation, please refer to the table above.
- **Association**
  - User ———— (Input Email Address / Select Output File Format / Select Transcription Language / Upload the File / Confirm / View History Results)
- **Generalization**
  - Select Output File Format <———— (.doc / .txt / .pdf)
  - Select Transcription Language <———— (English / Spanish / Chinese)
- **Include**
  - Confirm ----> Receive the Results
  - View History Results ----> Input Email Address
- **Extend**
  - (Video / Audio) <---- Delete Files
  - Confirm <---- Receive Error Reports
  - Input Email Address <---- (Download the Results Manually / Delete the Results)
