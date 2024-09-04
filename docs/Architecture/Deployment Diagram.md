# Transcription Aide Platform - Deployment Diagram

Deployment diagrams is used in modeling the physical aspects of Transaction Aide Platform (TAP) also named as the static deployment view of a system (topology of the hardware).

## Deplotment Diagram

![Component_Diagram](<../imgs/Architecture%20diagram/Deployment_Diagram.png>)

## Overview

### User's Computer

- **Web Browser**:
    - This is the client's interface. The user interacts with the system through a web browser, which sends HTTP requests over the internet to the server hosting the application.

### Application Server

- **Transcription Aide Platform**: 
  - This is the main component deployed on the application server. It handles the back-end logic of Transcription Aide Platform. It's responsible for processing user requests, business logic, and generating responses that are sent back to the user's web browser as well as invoking database APIs.

- **Database**: 
  - This component contains the data necessary for the Transcription Aide Platform to function. It stores, manages, and provides access to the data required by the Web Application, such as transcription records.

### Transcription Engine Component

- **Function**:
    - Is responsible for converting audio files into text. This component performs the core 
      functionality of the TAP system.

- **Interactions**:
    - Receives files for transcription via the **Process Transcription API**.
    - After processing, the results are stored using the **Data Storage API**.

### Connections

- **HTTP over Internet**: 
  - The Web Browser on the user's computer communicates with the Web Application on the Application Server over HTTP, which is a standard protocol for web communication.

- **Native Database Connection**:
  - The Database Connection API interacts with the Database directly using a native database connection, facilitating data retrieval and storage.
