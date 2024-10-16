

# **Frontend-Backend Integration - Epic 1 (File Upload)**

## **Overview**

This document outlines the necessary steps and considerations for integrating the frontend with the backend for the Transcription Aide Platform (TAP). The goal is to ensure that the frontend can correctly communicate with the backend API, particularly for file uploads and transcription requests, ensuring smooth interaction between both teams. Below is the current frontend interface.

![image](https://github.com/user-attachments/assets/7955c88a-79a0-4a88-a471-693a4292f960)



## **1. API Interaction Details**

### **1.1 API Endpoint for File Upload**
- **Endpoint**: `/api/upload`
- **Method**: `POST`
- **Description**: Handles file uploads (audio files) along with email, output format, and language preferences.
- **Content Type**: `multipart/form-data`

### **1.2 Request Parameters**
The following parameters are sent from the frontend via a `POST` request:

| **Parameter**  | **Type**    | **Description**                                       | **Required** |
|----------------|-------------|-------------------------------------------------------|--------------|
| `email`        | `string`    | The user's email address to receive transcription.    | Yes          |
| `file`         | `file`      | Audio file(s) to be transcribed.                      | Yes          |
| `outputFormat` | `string`    | The preferred output format (`docx`, `pdf`, `txt`).   | Yes          |
| `language`     | `string`    | The transcription language (`english`, `spanish`).    | Yes          |

### **1.3 Response Structure**

#### **1.3.1 Success Response**
- **HTTP Status Code**: `200 OK`
- **Response Body**:
  ```json
  {
    "message": "Files uploaded successfully!",
    "fileId": "abc123",
    "estimatedProcessingTime": "10 minutes"
  }
  ```
  - `message`: Confirmation of a successful upload.
  - `fileId`: Unique identifier for tracking the uploaded file.
  - `estimatedProcessingTime`: Estimated time for transcription completion.

#### **1.3.2 Error Response**
- **HTTP Status Codes**:
  - `400 Bad Request`: Invalid request parameters.
  - `500 Internal Server Error`: Server-side issue during file upload or processing.

- **Response Body Example**:
  ```json
  {
    "error": "Invalid file format."
  }
  ```


## **2. Frontend-Backend Integration Steps**

### **2.1 Confirm API Availability**
- The frontend will use the API endpoint `/api/upload` to upload files and form data.
- Backend team needs to confirm the following:
  - The API endpoint is live and accessible.
  - API base URL has been correctly set up as `REACT_APP_API_URL` in the environment configuration.

### **2.2 Define Data Format and Validation**
- **Email**: Ensure that the backend validates email addresses.
- **File**: The frontend sends multiple files through `FormData`. Ensure the backend accepts multiple file uploads in the required format (`.wav`, `.mp3`, etc.).
- **Output Format** and **Language**: Ensure backend accepts and processes these parameters. The options should match those in the frontend (`docx`, `pdf`, `txt` for output format; `english`, `spanish`, `french` for language).

### **2.3 Error Handling**
- **Network Errors**: In case of a network failure or an unavailable API, the frontend will alert the user with a message like: `"An error occurred while uploading files."`
- **API Errors**: If the backend returns an error response (e.g., invalid file format), the frontend will alert the user with the message from the `error` field in the response.


## **3. Key Points for Backend Team**

### **3.1 File Size and Format**
- Confirm any file size limitations and accepted formats.
- If a file exceeds the size limit or is in an unsupported format, the backend should return an appropriate error with a clear message (e.g., `"File too large"` or `"Invalid file format"`).

### **3.2 API Authentication (If Applicable)**
- Confirm whether authentication is required for the `/api/upload` endpoint.
- If authentication is required, provide the necessary details (e.g., tokens) that the frontend should include in the request headers.

### **3.3 Rate Limiting or Queue Handling**
- If there is any rate limiting or queuing on the backend, confirm how this should be communicated to the frontend (e.g., by providing estimated wait times in the response).

### **3.4 Mock Data for Testing**
- If the backend API is not fully ready, it is helpful to set up mock endpoints or provide example responses so the frontend team can proceed with development and testing.


## **4. Frontend Responsibilities**

### **4.1 FormData Submission**
- The frontend uses `FormData` to handle file uploads and related form data (email, output format, language). The following code snippet illustrates the request:
  ```js
  const handleConfirm = async () => {
    const formData = new FormData();
    formData.append('email', email);
    files.forEach(file => formData.append('file', file));
    formData.append('outputFormat', outputFormat);
    formData.append('language', language);

    try {
      const API_BASE_URL = process.env.REACT_APP_API_URL;
      const response = await fetch(`${API_BASE_URL}/api/upload`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        alert("Files uploaded successfully!");
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.message}`);
      }
    } catch (error) {
      alert("An error occurred while uploading files.");
    }
  };
  ```

### **4.2 Progress Feedback to Users**
- The frontend simulates upload progress for visual feedback. Once the backend is fully integrated, this can be extended to reflect the actual progress as reported by the backend (e.g., using WebSockets or long polling).

### **4.3 Post-Upload Navigation**
- After a successful upload, the frontend can automatically navigate the user to a status page or queue where they can track the progress of the transcription.


## **5. Communication with Backend Team**

### **5.1 Next Steps**
- **Backend Team**: 
  - Confirm the API endpoint paths and ensure that the parameters (email, file, outputFormat, language) are handled correctly.
  - Provide detailed error messages for invalid input (e.g., invalid file type, large files).
  - Share any additional requirements such as authentication, rate limiting, or file size constraints.
  
- **Frontend Team**:
  - Ensure the form data is sent correctly via `POST` request.
  - Handle various response codes from the backend, including success and error cases.
  - Provide feedback to the user about the upload status and navigate them to the appropriate page after the upload.
