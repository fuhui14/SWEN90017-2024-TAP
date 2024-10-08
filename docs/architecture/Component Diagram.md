# Transcription Aide Platform - Component Diagram

This document provides an explanation of the Transaction Aide Platform (TAP) 
Component Diagram, which illustrates the main components of the TAP system and their 
interactions. The diagram serves as a visual representation of how different parts of the system 
communicate with each other via various APIs and services, ensuring the successful execution of 
tasks such as file upload, transcription processing, email notifications, and data storage.

## UML Component Diagram

![Component_Diagram](<../imgs/Architecture%20diagram/Component_Diagram.jpeg>)

## Components Overview

### Notification Component

- **Function**:
    - Handles the delivery of notifications to users. This could include updates on the status 
      of transcription tasks or completion notifications.

- **Interactions**:
    - Utilizes the **Send Email API** to dispatch email notifications to users when certain events
      occur, such as the completion of a transcription.

### User Interface (UI) Component

- **Function**: 
  - Is responsible for the user-facing aspects of the TAP system. It 
    allows users to interact with the platform, such as uploading files, selecting options for 
    transcription, and viewing notifications.

- **Interactions**: 
  - Communicates with the **Upload File API** within the Services package to upload 
    files for processing.
  - Interacts with the **Process Transcription API** to show the progress of the transcription.

### Transcription Engine Component

- **Function**:
    - Is responsible for converting audio files into text. This component performs the core 
      functionality of the TAP system.

- **Interactions**:
    - Receives files for transcription via the **Process Transcription API**.
    - After processing, the results are stored using the **Data Storage API**.

### Admin Portal Component

- **Function**: 
  - Provides administrative functionalities, allowing administrators to view stored data and 
    transcription tasks.

- **Interactions**:
  - Accesses stored data through the **Data Storage API** to retrieve and review transcription 
    files and results.

### File Management Component

- **Function**: 
  - Is in charge of handling files within the system. It manages the storage, retrieval, and 
    organization of files that are uploaded by users or generated by the system.
  
- **Interactions**:
  - Connects to the **Queue Management API** to manage the flow of files through the transcription 
    queue. 
  - Uses the **Data Storage API** to store and retrieve files as needed.
  
### Queue System Component

- **Function**: 
  - Manages the order and flow of files awaiting transcription. It ensures that files are 
    processed in a systematic manner.

- **Interactions**:
  - Interfaces with the **Queue Management API** to manage the processing queue. 
  - Sends files to the **Process Transcription API** for transcription once they reach the front of 
    the queue.

### Services Package

- **Function**:
  - Encompasses the core services that provide the necessary APIs for the different components 
    of the Transaction Aide Platform (TAP) to interact and perform their respective functions. 
    This package acts as the backbone of the system, enabling smooth communication and data 
    flow between components.

- **API Gateway**
  - **Function**:
    - Is the central access point for all API requests within the TAP system. It serves as an 
      intermediary that processes, routes, and secures API calls between the client-side 
      components (like the UI and Admin Portal) and the backend services (like the Transcription
      Engine and Storage Service). 
    - It ensures that requests made by the UI Component for file uploads and transcription 
      processing are directed to the appropriate services via the **Upload File API** and **Process 
      Transcription API**.
    
  - **Interactions**:
    - **Upload File API**:
      - The API Gateway handles file upload requests from the UI Component, ensuring the files 
        are securely transmitted and ready for processing.
    - **Process Transcription API**:
      - It manages the requests for transcription processing, routing them to the Transcription 
        Engine for conversion from audio/video to text.

- **Storage Service**
  - **Function**:
    - Is responsible for the storage, retrieval, and management of all files and data within the 
      TAP system. It ensures that uploaded files, transcription results, and other important 
      data are securely stored and accessible to the necessary components. 
    - This service is crucial for maintaining data integrity and providing persistent storage 
      that can be accessed and managed by other components like File Management and Admin Portal.
  
  - **Interactions**:
    - **Data Storage API**:
      - Provides an interface for the File Management and Admin Portal components to store and 
        retrieve data. It ensures that data requests are processed correctly, allowing files 
        and transcription results to be accessed when needed.

- **Email Service**
  - **Function**:
    - Handles the sending of email notifications within the TAP system. It is responsible for 
      ensuring that users receive timely updates about the status of their files, including 
      notifications when transcription is complete.
    - This service is particularly important for keeping users informed about the progress and 
      results of their transcription requests.

  - **Interactions**:
    - **Send Email API**: 
      - Is used by the Notification Component to trigger email notifications. The Email Service 
        takes the request and sends out the appropriate email to the user, ensuring they are 
        kept up to date on their transcription tasks.
