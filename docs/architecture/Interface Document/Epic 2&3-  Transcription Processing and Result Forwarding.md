
# **Interface Document for Epic 2&3: Transcription Processing and Result Forwarding**

## **1. Overview**

This document outlines the interface design and functionality for **Epic 2: Transcription Processing** and **Epic 3: Result Forwarding** of the Transcription Aide Platform (TAP). It describes the user interface (UI) elements, interactions, and backend API integrations required to process multiple audio files using OpenAI's Whisper technology, manage speaker differentiation, and display the processing status to users.

### **Epic Summary:**
- **Epic ID**: 2 & 3
- **Epic Name**: Transcription Processing & Result Forwarding
- **Objective**: To handle multiple file transcriptions using a queue, show real-time processing progress, and send the transcription results via email in user-specified formats, while handling errors effectively.


## **2. Interface Layout and Elements**

### **2.1 Multiple File Transcription Queue**

- **UI Element**: Progress Bar
- **Label**: "Processing..."
- **Description**: Displays the progress of each file being transcribed, including the percentage completed and an estimate of time remaining.
- **Validation**: The progress bar dynamically updates based on the file processing status.
  - **Component**: `<progress value="25" max="100">25%</progress>`
  - **Validation**: Regex for validating progress status.

### **2.2 Speaker Differentiation**

- **UI Element**: Text Labels
- **Label**: "Speaker 1, Speaker 2, etc."
- **Description**: Transcriptions will display labels for different speakers identified during the transcription process.

  - **Component**: `<span>Speaker 1: "Text spoken by speaker 1"</span>`
  - **Speaker Separation**: Automatically applied based on Whisper's speaker identification feature.


### **2.3 Display Processing Status**

- **UI Element**: Progress Indicator
- **Label**: "Processing Status"
- **Description**: Users can view the current processing status, including estimated time of completion and the file's position in the queue.
  - **Component**: `<div class="processing-status">Your file is #2 in the queue. Estimated completion: 10 minutes</div>`


### **2.4 Automatic Email Transcription Results**

- **UI Element**: Email Notification (Automated)
- **Label**: (no label)
- **Description**: After the transcription is completed, the system automatically sends the transcription results to the user’s pre-configured email address. No additional input is required from the user on this page.



### **2.5 Automatic Redirection to History Page **

- **UI Element**: Redirect Action (Automated)
- **Label**: (no label)
- **Description**:  Upon completing the transcription, the system automatically redirects users to the History Page where they can view, download, and manage their transcription files.


## **3. Interaction Flow**

1. **User Uploads Files for Transcription**:
   - The user uploads one or more files to the system.
   - The system adds the files to a queue and begins processing them one by one.

2. **Real-Time Status Display**:
   - As each file is processed, the user can see the percentage completed and the estimated time remaining.
   - The queue position is also displayed.

3. **Speaker Differentiation**:
   - The system automatically identifies different speakers in the transcription, labeling them accordingly (e.g., "Speaker 1").

4. **Automatic Transcription Result Forwarding**:
   - Once the transcription is complete, the results are automatically emailed to the user using the email address provided in Epic 1.
   - The user receives the results in the pre-selected format (TXT, DOCX, PDF) and language (as configured in Epic 1).

5. **Automatic Redirection to Finished Page**:
   - Upon completing the transcription, the system automatically redirects users to the Transcription Finished Page, where they can view and download their transcriptions.


## **4. Backend API Requirements**

### **4.1 Transcription Queue API**

- **Endpoint**: `/api/transcription-queue`
- **Method**: `POST`
- **Description**: Handles the processing of multiple files in a queue, ensuring they are processed in the order received.
- **Parameters**:
  - **file** (file): One or more audio files (or video files in future iterations).
  - **outputFormat** (string): The selected output format (`docx`, `txt`).
  - **language** (string): The selected transcription language.


### **4.2 Transcription Status API**

- **Endpoint**: `/api/transcription-status`
- **Method**: `GET`
- **Description**: Provides real-time updates on the status of transcription, including the queue position and percentage completion.
- **Response**:
  - **Success**: Returns the current status (e.g., "Processing", "Completed", "Failed").
  - **Error**: Returns an error if the file ID is invalid.


### **4.3 Automatic Email Transcription Results API**

- **Endpoint**: `/api/send-results`
- **Method**: `POST`
- **Description**: Automatically sends the transcription results to the pre-configured email address once the transcription is complete.
- **Parameters**:
    - **fileId (string)**: The unique ID of the transcribed file.
    - **outputFormat (string)**: The format chosen for the transcription results (already selected in Epic 1).



## **5. Error Handling**

### **5.1 Failed Transcription Process**
- **Scenario**: If the transcription fails for any reason (e.g., file corruption or system issues), the user will receive an error message.
- **Error Message**: "Transcription failed. Please try again later."

### **5.2 Queue Overflow Error**
- **Scenario**: If too many files are in the queue, resulting in a delay.
- **Error Message**: "The queue is full. Please try uploading your file later."

### **5.3 Transcription Results Not Sent**
- **Scenario**: If the system fails to send the transcription results via email after processing, an error message will be shown, and the user will be notified via email of the failure.
- **Error Message**: "Failed to send transcription results. Please check your inbox later."


## **6. UI Considerations**

- **Accessibility**: Ensure all form elements (input fields, dropdowns, and buttons) are accessible to users with disabilities (e.g., using screen readers).
- **Responsiveness**: The interface should be responsive and adapt to different screen sizes, ensuring optimal user experience on both desktop and mobile devices.
- **Visual Feedback**: Provide visual feedback (e.g., checkmarks, progress indicators) to inform users that their input has been received and processed.

