# Software Requirements Specification (SRS) for Transcription Aide Platform

## 1. Introduction
- **Purpose**: To build a transcription platform based on OpenAI's Whisper software to facilitate audio file transcriptions for a research team within a secure local network environment.
- **Scope**: The platform will consist of a web interface and local machine execution that handles audio file uploads, transcription, and speaker identification without requiring user login. This system will only be used within the research group

## 2. General Description
- **Product Functions**:
  1. File upload via a simple web interface.
  2. Execution of transcription on the local machine.
  3. Email notification with transcription results.
  4. Identification of different speakers in the transcription.
  5. Short-term storage of transcriptions in a local database.

- **User Characteristics**: Researchers in residential care settings who require transcription of recorded group conversations for qualitative data analysis.

- **Assumptions and Dependencies**:
  - The platform will operate within a secure LAN.
  - Users will be limited to a small research team (about 3 concurrent users).

## 3. System Features

### Functional Requirements
Functional requirements describe the specific functions and features the system must provide, focusing on what the system is supposed to do.

- **File Upload**:
  - Support uploading audio files.
  - Support uploading video files. (optional)
  - The user can select a format for the output file. (Optional)
  - Drag-and-drop functionality for file uploads. (optional)
  - The user can input his email address to receive the transcription result.

- **Transcription Processing**:
  - Implementation of a queue system to handle multiple file transcriptions.
  - Use the up-to-date OpenAI Whisper model. (optional)
  - Ability to differentiate speakers labeled as "Speaker 1, 2, 3, etc."
  - Send transcription results to the user through email.
  - Send system error reports to users through email.
  - Support 'txt' output format.
  - Support 'docx' output format. (optional)
  - Support the Chinese language. (optional)
 
- **File Management**:
  - Save transcription result files in the local database.
  - Temporary storage of files with an automated deletion policy after 30 days.
  - Have an admin portal to see the history record.
  - The system can send a link through email to allow the user to enter the admin portal.
  - Download history transcription result files in the admin portal.

### Non-Functional Requirements
Non-functional requirements describe how the system operates and the quality standards it must meet, focusing on how the system should perform.

- **Security and Compliance**:
  - Ensure secure access within the LAN.
  - No high-level security protocols specified, but data privacy is crucial due to sensitive research data.

- **Interactivity and Accessibility**:
  - Desktop-based web interface with minimal design.
  - No requirement for a mobile version.
  - Simple and user-friendly interface for uploading and receiving results.

- **Performance Requirements**:
  - The system should efficiently handle up to 3 concurrent (or in queue) transcriptions.
  - Expected to manage audio files up to 4 hours in length.
  - Improvement in transcription processing time, aiming for less than 4 hours for 1-hour audio files.
  - Optional use of additional open-source libraries to enhance speaker diarization capabilities.



- **Security Requirements**:
  - Ensuring data privacy for sensitive research information.
  - Implementation of network security measures within the LAN.
