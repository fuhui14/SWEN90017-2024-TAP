
# **Usability Test Result**

## **1. Introduction**

The usability test for the Transcription Aide Platform (TAP) was conducted to assess the ease of use, intuitiveness, and overall user experience. Participants were tasked with uploading audio files, configuring transcription settings, and managing transcription history. The test revealed several areas for improvement, particularly in file management, UI adjustments, and navigation.  

The key objectives and detailed procedures from the test are outlined in the **Usability Test Plan.md**.  

The results are outlined **here**, which will help identify usability issues and provide feedback for further improvements.

### **1.2 Scope**
The usability test will cover:
- The overall user interface (UI) and its ease of navigation.
- The functionality of core features: audio file upload, process management, result delivery and history management.

### **1.3 Objectives**
- Determine if users can upload audio files and configure transcription settings (file format, language, and email) easily.
- Assess how effectively users can monitor the progress of their transcription tasks during the processing phase.
- Identify issues with navigation and management in the history section, such as downloading results and understanding task statuses.

### **1.4 Participants**
The test will include participants with varied technical skill levels (Team members) and the Client.


## **2. Test Tasks and Results**

### **2.1 Task Scenario 1: Transcribe**

- **Objective**: Evaluate the ease with which users can upload audio files and configure transcription settings.
  

- **Instruction**: You are using the Transcription Aide Platform to transcribe an important meeting recording that includes multiple speakers. You need the transcription to be emailed to you in txt format and to be transcribed into Spanish.
  

- **Steps**:
    1. Navigate to the **Transcription** page on the Figma prototype.  
    2. Input an email address to receive the transcription results.
    3. Choose the desired file format for the transcription output (e.g., `.txt` or `.docx` or `.pdf`).
    4. Select the language for transcription (e.g., English, Spanish, Chinese).
    5. Select one audio files for upload (via drag-and-drop or file selection).
    6. Click the "Confirm" button to start the transcription process.
  

- **Expected Outcome**:
    - Files are successfully uploaded, and the system provides immediate feedback (e.g., upload progress).
    - All fields are correctly filled out before the user is able to proceed (valid email format, file format selected).
    - Users clearly understand the settings they need to configure before transcription.
  

- **Potential Challenges**:
    - Difficulty in locating the file upload section.
    - Confusion about the email input field (e.g., incorrect format, unclear instructions).
    - Uncertainty about which file format or language to choose for transcription.
 

- **Results**:
  - Task Completion Rate: 100%, successfully uploaded audio files and submitted them for transcription.
  - Feedback: Participant mentioned that the font size was too small on certain parts of the page, making it difficult to read instructions and options.
  - Issue: After uploading one file, participants were unable to find a button to add another file without reloading the page.
  - Improvement: Add a clear option for uploading multiple files simultaneously or sequentially.

---

### **2.2 Task Scenario 2: Processing**

- **Objective**: Assess users' ability to monitor the progress of the transcription process and handle multiple tasks.


- **Instruction**: After uploading the audio files for transcription, you want to monitor the progress and ensure that the file is being processed correctly. You also want to know if there’s a way to start new transcription tasks while others are still being processed.


- **Steps**:
    1. After submitting a transcription task, users are taken to the **Processing** page.
    2. View the progress bar or status indicator for each file being transcribed.
    3. If multiple files are uploaded, monitor the progress of each file.
    4. Observe the option to either transcribe another file or wait for the current tasks to finish.
    5. Note any system messages that indicate completion, errors, or warnings.


- **Expected Outcome**:
    - Users can easily track the progress of each file with clear status indicators (e.g., progress bars, “Completed,” “In Progress”).
    - The system allows users to start a new transcription task without waiting for the previous ones to finish.
    - Errors are clearly indicated if any files fail to process.


- **Potential Challenges**:
    - Confusion about the meaning of progress indicators.
    - Difficulty managing multiple tasks at once.
    - Unclear error messages if a task fails.


- **Results**:
  - Task Completion Rate: 100% Understood the transcription progress bars and managed multiple tasks.
  - Feedback: Participants requested that the system remembers previous transcription settings, such as language and file format, to avoid reselecting the same options for each new transcription.
  - Improvement: Implement default settings to speed up repetitive tasks.
---

### **2.3 Task Scenario 3: History**

- **Objective**: Test users' ability to access past transcription tasks, download results, and manage files.
  

- **Instruction**: You have previously submitted several transcription tasks and now need to access the history of completed transcriptions to download a file and review it.
  

- **Steps**:
    1. Navigate to the **History** section of the platform.
    2. Input the email address used for previous transcriptions to access past results.
    3. Review the table of past transcription tasks, which includes file name, file type, creation date, expiry date, output type, and status (completed, failed, etc.).
    4. Click on the “Download” button to retrieve the transcription results.
    5. Check the file’s expiration date or remaining time for storage (e.g., “Expires in 30 days”).
    6. Handle any failed tasks, reviewing system messages for errors.


- **Expected Outcome**:
    - Users can easily locate and download completed transcriptions from the history section.
    - The system clearly displays the status of each task (e.g., completed, failed).


- **Potential Challenges**:
    - Difficulty finding the correct transcription task in the history.
    - Misunderstanding the file expiration warning.
    - Unclear instructions for handling failed transcriptions.


- **Results**:
  - Task Completion Rate: 100% Successfully accessed and downloaded their transcription history.
  - Issue: Participants suggested that if a file fails to transcribe, the download button should be grayed out, indicating that the file cannot be downloaded.
  - Pagination Feedback: The “Last Page” button at the bottom of the history page was unclear. Participants recommended switching to numeric page numbers and renaming “Page” to “Previous Page” for consistency with “Next Page.”
  - Improvement: Modify the download button color for failed files and adjust pagination labels for better navigation clarity.


## **3. Key Findings**

1. **Font Size Adjustment**: Some of the font sizes are too small and hard to read. It would be helpful to adjust the font size for better visibility.

2. **File Addition Issue**: When transcribing, after adding one file, there’s no way to add another file — there’s no button to allow for additional file uploads (a minor issue).

3. **Default Transcription Settings**: It would be useful to add a default state for the transcription options. This way, when a new file with identical settings needs to be transcribed, users don’t have to select the same options again.

4. **Failed File Download in History Page**: On the history page, if a file fails to process, its download button should be grayed out to indicate that it cannot be downloaded.

5. **Pagination in History Page**: The "Last Page" button at the bottom of the history page could be replaced with page numbers. Additionally, the "Page" button on the left could be renamed "Previous Page" to match the "Next Page" button on the right.

6. **About Page Links**: The About page could include hyperlinks to allow users to navigate directly to relevant sections or external resources.

## **4. Next Steps**

1. The development team should prioritize these usability issues and implement the recommended changes. 
2. Once changes are made, conduct a follow-up usability test to confirm improvements. 
3. Continue gathering user feedback for future iterations to ensure the platform remains intuitive and user-friendly.
