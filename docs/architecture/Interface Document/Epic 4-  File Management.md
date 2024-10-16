
# **Interface Document for Epic 4: File Management**

## **1. Overview**

This document outlines the interface design and functionality for **Epic 4: File Management** of the Transcription Aide Platform (TAP). It describes the UI elements, interactions, and backend API integrations required for managing transcription result files, including saving, retrieving, and managing file expiration.

### **Epic Summary:**
- **Epic ID**: 4
- **Epic Name**: File Management
- **Objective**: To provide functionality for saving, retrieving, and automatically managing the deletion of transcription result files.


## **2. Interface Layout and Elements**

### **2.1 Save Transcription Results**

- **UI Element**: Save Confirmation Icon
- **Label**: "(Save Transcription Result Icon)"
- **Description**: Automatically saves transcription results to a local database after processing.
- **Validation**: The progress bar dynamically updates based on the file processing status.
  - **Component**: `<div class="save-confirmation">Your transcription results have been saved.</div>`


### **2.2  View History of Transcriptions**

- **UI Element**: History Section
- **Label**: "Transcription History"
- **Description**: Displays a list of the user's previous transcriptions, showing the file name, creation date, and expiration date.

  - **Component**: `<table><thead><tr><th>File Name</th><th>Creation Date</th><th>Expiration Date</th></tr></thead><tbody><tr><td>audio1.docx</td><td>01-10-2024</td><td>01-11-2024</td></tr></tbody></table>`


### **2.3 File Expiration**

- **UI Element**: Expiration Date Display
- **Label**: "File Expiration Date"
- **Description**: Users can see when their files will be automatically deleted from the system.
  - **Component**: `<div class="expiration-date">Your file will be deleted on: 01-11-2024</div>`


### **2.4 Download Transcription Files**

- **UI Element**: Download Button
- **Label**: "Download Icon"
- **Description**: Allows users to download their transcription files from the history section.
    - **Component**: `<button type="button">Download</button>`



## **3. Interaction Flow**

1. **Automatic Saving of Transcriptions:**:
   - Once the transcription is complete, the system automatically saves the file to the database.

2. **Viewing Transcription History:**:
   - Users can navigate to the history section to view and manage their past transcriptions, including downloading or viewing expiration dates.

3. **File Expiration**:
   - Files are automatically deleted after 30 days, and users are shown the expiration date in the history section.

4. **Downloading Transcriptions**:
   - Users can download files directly from their history section.



## **4. Backend API Requirements**

### **4.1 Save Transcription Result API**

- **Endpoint**: `/api/save-transcription`
- **Method**: `POST`
- **Description**: Automatically saves the transcription result to the local database after processing.
- **Parameters**:
  - **field** (string): The unique ID of the transcribed file.
  - **fileData** (binary): The actual transcription file data.
  - **expirationDate** (date): The date when the file will be deleted.


### **4.2 Retrieve Transcription History API**

- **Endpoint**: `/api/history`
- **Method**: `GET`
- **Description**: Retrieves the user's transcription history, including file names, creation dates, and expiration dates.
- **Response**:
  - **Success**: Returns the transcription history.
  - **Error**: Returns an error if no history is found for the user.




## **5. Error Handling**

### **5.1 Failed to Save File**
- **Scenario**: If the system fails to save the transcription result, an error is displayed to the user.
- **Error Message**: "Failed to save transcription result. Please try again."

### **5.2 Failed to Download File**
- **Scenario**: If the user attempts to download a file that no longer exists, an error is displayed.
- **Error Message**: "File not found. It may have been expired."



## **6. UI Considerations**

- **Accessibility**: Ensure all form elements (input fields, dropdowns, and buttons) are accessible to users with disabilities (e.g., using screen readers).
- **Responsiveness**: The interface should be responsive and adapt to different screen sizes, ensuring optimal user experience on both desktop and mobile devices.
- **Visual Feedback**: Provide visual feedback (e.g., checkmarks, progress indicators) to inform users that their input has been received and processed.

