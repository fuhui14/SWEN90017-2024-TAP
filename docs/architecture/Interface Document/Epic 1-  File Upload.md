
# **Interface Document for Epic 1: File Upload**

## **1. Overview**

This document outlines the interface design and functionality for **Epic 1: File Upload** of the Transcription Aide Platform (TAP). It includes a description of the user interface (UI) elements, user interactions, and backend API integrations required to implement the file upload and transcription features as described in Epic 1.

### **Epic Summary:**
- **Epic ID**: 1
- **Epic Name**: File Upload
- **Objective**: To allow users to upload one or more audio/video files, input their email address to receive transcription results, select output format, and specify the transcription language.


## **2. Interface Layout and Elements**

### **2.1 Input Email Address**

- **UI Element**: Text Input Field
- **Label**: "Input your Email Address"
- **Description**: Users enter their email address to receive the transcription results. The email input should be validated in real-time.
- **Validation**: The email must be in the proper format (e.g., example@email.com). A green checkmark appears next to the input field when the email is valid.
  
  - **Component**: `<input type="email" placeholder="Enter your email" required>`
  - **Validation**: Regex for validating email format.

### **2.2 File Upload Section**

#### **2.2.1 Upload Audio File**

- **UI Element**: File Upload Button + Drag-and-Drop Area
- **Label**: "Upload"
- **Description**: Users can either click to upload or drag-and-drop one or more audio files. Supported formats are displayed (.wav, .mp3, .m4a, .flac, .ogg, .aac).
- **Supported Formats**: `.wav`, `.mp3`, `.m4a`, `.flac`, `.ogg`, `.aac`
  
  - **Component**: `<input type="file" accept="audio/*" multiple>`
  - **Drag-and-Drop**: Users can drag files into the designated area to initiate upload.

#### **2.2.2 Upload Video File (Future Scope)**
- **UI Element**: File Upload Button + Drag-and-Drop Area
- **Label**: "Upload Video File"
- **Description**: Allows users to upload video files to transcribe. This feature will support video formats such as `.mp4` and `.mov`.
- **Supported Formats**: `.mp4`, `.mov`

> **Note**: This feature is marked as "Could Have" and is not critical for the initial release. It will be developed in future sprints.

### **2.3 Select Output Format**

- **UI Element**: Dropdown Menu
- **Label**: "Select a format for the output file"
- **Description**: Users can select the desired file format for the transcription results (e.g., `.docx`, `.txt`, etc.).
- **Options**:
  - `.docx`
  - `.txt`
  
  - **Component**: `<select name="outputFormat"> <option value="docx">docx</option> <option value="txt">txt</option> </select>`

### **2.4 Select Transcription Language**

- **UI Element**: Dropdown Menu
- **Label**: "Select transcription language"
- **Description**: Users can choose the language in which the transcription will be provided. 
- **Options**: 
  - English
  - Spanish
  - French
  
  - **Component**: `<select name="language"> <option value="English">English</option> <option value="Spanish">Spanish</option> <option value="French">French</option> </select>`

### **2.5 Confirmation Button**

- **UI Element**: Button
- **Label**: "Confirm"
- **Description**: After selecting the email address, file, output format, and transcription language, the user clicks the "Confirm" button to submit the information and start the transcription process.
  
  - **Component**: `<button type="submit">Confirm</button>`


## **3. Interaction Flow**

1. **User Inputs Email Address**:
   - The user inputs their email address in the designated text field.
   - Real-time validation is performed to ensure the email is in the correct format. A green checkmark is shown if valid.

2. **User Uploads Audio or Video File**:
   - Users can either drag-and-drop a file or use the file picker to upload audio files (in future releases, video files).
   - The file upload area supports multiple file uploads, and the file format must match the supported audio types.

3. **User Selects Output Format**:
   - The user selects the preferred format for the transcription output (e.g., `.docx`, `.txt`).

4. **User Selects Transcription Language**:
   - The user selects the language in which the transcription will be provided (e.g., English, Spanish, French).

5. **User Clicks Confirm**:
   - After all fields are filled out, the user clicks the "Confirm" button to submit the form.
   - A POST request is sent to the backend to start the transcription process.


## **4. Backend API Requirements**

### **4.1 File Upload API**

- **Endpoint**: `/api/upload`
- **Method**: `POST`
- **Description**: Handles the file upload. The uploaded file(s) and the user's email are passed to the backend for transcription.
- **Parameters**:
  - **email** (string): The email address where transcription results will be sent.
  - **file** (file): One or more audio files (or video files in future iterations).
  - **outputFormat** (string): The selected output format (`docx`, `txt`).
  - **language** (string): The selected transcription language.
- **Response**:
  - **Success**: Returns a success message and initiates the transcription process.
  - **Error**: Returns an error if file format is unsupported or email validation fails.

### **4.2 Transcription Status API**

- **Endpoint**: `/api/transcription-status`
- **Method**: `GET`
- **Description**: Checks the current status of the transcription process.
- **Parameters**:
  - **fileId** (string): The unique ID of the uploaded file.
- **Response**:
  - **Success**: Returns the status (e.g., "Processing", "Completed", "Failed").
  - **Error**: Returns an error if the file ID is invalid.


## **5. Error Handling**

### **5.1 Email Input Validation Error**
- **Scenario**: If the user inputs an invalid email address, a red error message appears below the input field.
- **Error Message**: "Please enter a valid email address."

### **5.2 Unsupported File Format Error**
- **Scenario**: If the user uploads a file that is not in the supported formats, an error message is displayed.
- **Error Message**: "Unsupported file format. Please upload a valid audio file."

### **5.3 Missing Required Fields**
- **Scenario**: If any required fields (e.g., email, file, output format) are not filled out, an error is shown when the user clicks "Confirm".
- **Error Message**: "Please fill out all required fields."



## **6. UI Considerations**

- **Accessibility**: Ensure all form elements (input fields, dropdowns, and buttons) are accessible to users with disabilities (e.g., using screen readers).
- **Responsiveness**: The interface should be responsive and adapt to different screen sizes, ensuring optimal user experience on both desktop and mobile devices.
- **Visual Feedback**: Provide visual feedback (e.g., checkmarks, progress indicators) to inform users that their input has been received and processed.

