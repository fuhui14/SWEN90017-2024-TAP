
# **Usability Test Plan**

## **1. Introduction**

### **1.1 Purpose**
The purpose of this usability test is to evaluate the ease of use, intuitiveness, and overall user experience of the **Transcription Aide Platform (TAP)**. The test will focus on key tasks such as file upload, transcription result retrieval, and interaction with the user interface. The results will help identify usability issues and provide feedback for further improvements.

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


## **2. Test Methodology**

### **2.1 Test Environment**
- The test will be conducted remotely or in person using the Figma platform to interact with the high-fidelity prototype of the Transcription Aide Platform (TAP). The prototype will be shared with participants via a Figma link, allowing them to explore and interact with the design. 
- Participants will use their own devices/our laptops to complete the test, ensuring a more realistic simulation of the actual user environment.
- Mobile recording and Screen recording software will be used to capture user interactions with the Figma prototype, focusing on their navigation, task completion, and overall interaction with the interface.
- Observers and facilitators will use online communication tools (such as Zoom or Google Meet) to provide instructions and guide the participants through the test if necessary.

### **2.2 Test Scenario Overview**
Participants will be asked to complete a series of tasks representing typical user actions, including:
- **Scenario 1: Transcribe**  
Participants will input email, select transcription settings, upload one or more audio files and initiate the transcription process.
  

- **Scenario 2: Processing**  
Participants will monitor the transcription progress, observe system feedback, and manage multiple transcription tasks.
  

- **Scenario 3: History**  
Participants will navigate to the history section, view past transcriptions, download completed files.


## **3. Test Objectives and Tasks**

### **3.1 Overview**

| **Test Objective**                                                                                     | **Task Description**                                                                                          |
|--------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| Evaluate the ease with which users can upload audio files and configure transcription settings         | **Task 1 (Transcribe)**: Input email, select format and language, upload audio files and start transcription. |
| Assess users' ability to monitor the progress of the transcription process and handle multiple tasks.  | **Task 2 (Processing)**: Monitor transcription progress, review progress bars, and manage multiple tasks.     |
| Test the navigation and management functionality of the history section                                | **Task 3 (History)**: Access history, download completed transcriptions.                                      |

### **3.2 Details**

#### **Task Scenario 1: Transcribe**

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

---

### **Task Scenario 2: Processing**

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

---

### **Task Scenario 3: History**

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



## **4. Test Procedure**

### **4.1 Briefing**
- Participants will be briefed on the purpose of the test. They will be informed that the test evaluates the platform's usability, not their performance.
- Instructions on each task will be provided, and participants will be encouraged to vocalize their thoughts and challenges during the process.

### **4.2 Execution**
- **Observation**: The test facilitator will observe and take notes on participants' behavior, any difficulties encountered, and overall reactions.
- **Recording**: The session will be recorded using screen capture software to review participant interactions in detail.
  
### **4.3 Post-Test Feedback**
- After completing all tasks, participants will be asked to share their feedback on their experience using the platform.
- Follow-up questions may be asked to understand their preferences, confusion points, or suggestions for improvement.


## **5. Test Metrics and Data Collection**

### **5.1 Success Criteria**
- **Task Completion Rate**: The percentage of tasks completed without errors.
- **Error Rate**: The number of mistakes participants make while trying to complete each task.
- **Time on Task**: The amount of time participants spend on each task, compared to the expected completion time.
- **User Satisfaction**: Measured via a post-test survey, where participants rate their satisfaction with the platform's ease of use and interface.

### **5.2 Data Collection Tools**
- **Screen Recording**: To capture participant actions during the test.
- **Observation Notes**: Facilitators will take notes on user behavior and challenges.
- **Survey and Follow-up Questions**: Participants will answer questions about their experience and rate their satisfaction with the system.


## **6. Roles and Responsibilities**

| **Role**                            | **Team Member**                            | **Responsibilities**                                                                                           |
|-------------------------------------|--------------------------------------------|----------------------------------------------------------------------------------------------------------------|
| **Test Designer and Facilitator**   | Yingrong Chen                              | Design the usability test plan, create tasks, brief participants, and guide them through the testing process.   |
| **Participant Recruitment**         | Tianyi Zhong                               | Recruit participants with various technical backgrounds for the usability test.                                |
| **Observer and Recorder**           | Fuhui Yang, and any available team members | Observe user interactions, take notes, and ensure screen recordings capture all interactions.                  |
| **Test Data Analysis**              | Yingrong Chen, Fuhui Yang                  | Analyze the data collected during the test, categorize issues, and prepare the final report.                    |
| **Reporting and Improvements**      | Entire Development Team                    | Review the usability report and implement improvements based on the findings.                                   |


## **7. Analysis and Reporting**

### **7.1 Analysis**
- The results will be analyzed based on the success criteria mentioned earlier (task completion rate, error rate, time on task, and user satisfaction).
- Usability issues will be categorized based on severity (high, medium, low) and prioritized for action.

### **7.2 Reporting**
- A detailed usability test report will be generated, outlining the findings, key issues, and suggestions for improvement.
- The report will be shared with the development team to help guide the next phase of improvements.


## **8. Follow-up and Iteration**

### **8.1 Discussion**
- A discussion will be held with the development team to review the usability test findings and prioritize the issues that need to be addressed.

### **8.2 Re-testing**
- Once improvements have been made, a second round of usability testing will be conducted to ensure the issues have been resolved and the platform's usability has improved.



## **9. Deliverables**
- Usability Test Plan (this document)
- Screen recordings of user interactions
- Usability Test Report with prioritized issues
- Recommendations for platform improvements
