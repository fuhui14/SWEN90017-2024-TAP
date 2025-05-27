
# Acceptance Criteria

## Epic 1: File Upload

| US ID | AC ID | User Story | Given | When | Then |
|-------|-------|------------|-------|------|------|
| 1.1   | 1.1.1 | As a User, I want to upload audio files so that I can transcribe audio files. | I have an audio file that I want to transcribe and an upload interface on the platform | I select the audio file and click the "Upload" button | The file is successfully uploaded, and a progress bar appears showing the transcription process starting |
| 1.2   | 1.2.1 | As a User, I want to upload video files so that I can transcribe video files. | I have a video file that I want to transcribe and an upload interface on the platform | I select the video file and click the "Upload" button | The file is successfully uploaded, and a progress bar appears showing the transcription process starting |
| 1.3   | 1.3.1 | As a User, I want to drag and drop files for upload so that I can quickly and easily upload files. | I have a file I want to upload and a drag-and-drop area on the platform | I drag the file to the drag-and-drop area | The file is successfully uploaded, and a progress bar appears showing the transcription process starting |
| 1.4   | 1.4.1 | As a User, I want to input my email address to receive the transcription result so that I can get the results directly sent to my inbox. | I have completed uploading my file and there is an email input field on the platform | I input my email address and click the "Submit" button | A confirmation message appears stating that the transcription result will be sent to the provided email |
| 1.5   | 1.5.1 | As a User, I want to select a format for the output file so that I can receive the transcription in my preferred format. | I have uploaded my file and an option to select the output format is available | I select the desired output format from the dropdown menu and click "Save" | A confirmation message appears stating that the transcription will be delivered in the selected format |

## Epic 2: Transcription Processing

| US ID | AC ID | User Story | Given | When | Then |
|-------|-------|------------|-------|------|------|
| 2.1   | 2.1.1 | As a User, I want the system to handle multiple file transcriptions using a queue so that multiple requests are processed eventually. | Multiple files are queued for transcription in the system | The system processes each file in the queue | The files are processed one by one, and their progress is displayed until all files are transcribed |
| 2.2   | 2.2.1 | As a User, I want to use the OpenAI Fast Whisper model so that I can receive the most accurate transcription result. | The Fast Whisper model is integrated into the system | A transcription request is made | The transcription result is provided using the fast Whisper model with improved accuracy |
| 2.3   | 2.3.1 | As a User, I want to watch transcribed results in a conversation form so that I can easily follow and understand the dialogue structure. | A transcription result is ready to be viewed | I open the transcription result page | The result is displayed in a conversation format with clear dialogue structure |
| 2.4   | 2.4.1 | As a User, I want to differentiate speakers labeled as "Speaker 1, 2, 3, etc." so that I can easily identify who said what in the transcript. | A transcription result includes multiple speakers | I view the transcription result | Each speaker is labeled distinctly as "Speaker 1," "Speaker 2," etc., making it clear who said what |
| 2.5   | 2.5.1 | As a user, I want the system to automatically detect the language of my audio so I receive an accurate transcript without having to choose a language manually, no matter where I’m located or what language my research team uses. | The system identifies the spoken language of the uploaded or recorded audio with a predefined accuracy threshold (e.g., ≥ 95%), eliminating the need for a manual dropdown. | I upload or record an audio clip and click “Transcribe.” | The system detects the language, transcribes the audio in that language, and displays the transcript. If detection fails, a fallback option allows me to select the language manually. |
| 2.6   | 2.6.1 | As a User, I want to receive transcriptions in my preferred language (e.g. Chinese) so that I can receive transcription services in my preferred language, enhancing accessibility and usability for a global audience. | I have set my preferred language in the system settings | I submit an audio file for transcription | The transcription result is provided in the selected language |
| 2.7   | 2.7.1 | As a User, I want to see a progress bar on the web page while my file is being processed so that I can understand the process’s status and estimate how long the processing will take. | A file is being processed | The system displays a progress bar on the processing page | The progress bar updates in real-time, reflecting the current status of the transcription process |

## Epic 3: Transcription Result Forwarding

| US ID | AC ID | User Story | Given | When | Then |
|-------|-------|------------|-------|------|------|
| 3.1   | 3.1.1 | As a User, I want to receive transcription results through email so that I can get the results conveniently. | A transcription is complete and my email is registered | The system sends the transcription result to my email | I receive an email with the transcription result attached or linked |
| 3.2   | 3.2.1 | As a User, I want to receive system error reports through email so that I am informed if my transcription request fails. | A transcription request fails during processing | The system generates an error report | The error report is sent to my registered email address, detailing the issue |
| 3.3   | 3.3.1 | As a User, I want to receive transcription in 'txt' format so that I can use it with most text processing tools. | The transcription is complete | I select 'txt' as the output format and click "Download" | The transcription is downloaded in 'txt' format with proper line breaks and character encoding |
| 3.4   | 3.4.1 | As a User, I want to receive transcription in 'docx' format so that I can use it in a professional document format. | The transcription is complete | I select 'docx' as the output format and click "Download" | The transcription is downloaded in 'docx' format with professional document styling |

## Epic 4: File Management

| US ID | AC ID | User Story | Given | When | Then |
|-------|-------|------------|-------|------|------|
| 4.1   | 4.1.1 | As a User, I want to save transcription result files in the local database automatically so that I can access them later if needed. | A transcription is complete and the system is connected to the local database | The transcription result is saved automatically | The transcription result is stored in the local database and accessible from the history page |
| 4.2   | 4.2.1 | As a User, I want to have my old files automatically cleaned up after 30 days so that storage is efficiently managed, and outdated files are removed. | Files have aged 30 days | The system's cleanup process runs automatically | Outdated files are deleted, and storage is freed up |
| 4.3   | 4.3.1 | As a User, I want to access an admin portal to see the history record so that I can manage and review past transcriptions. | The admin portal is accessible, and I have the correct permissions | I log in to the admin portal and navigate to the history section | The system displays the history of all transcription records with options to sort, filter, and review |
| 4.4   | 4.4.1 | As a User, I want to receive a link through email to enter the admin portal so that I can securely access the portal. | I have requested access to the admin portal | The system sends a secure link to my email | The link grants secure access to the admin portal, and I can log in |
| 4.5   | 4.5.1 | As a User, I want to download history transcription result files from the portal so that I can access previous transcriptions if needed. | I have accessed the admin portal and navigated to the history section | I select a transcription file and click "Download" | The selected transcription file is downloaded to my device |
| 4.6   | 4.6.1 | As a User, I want to see the expiration date of my transcription files in the admin portal so that I can know when my files will be automatically deleted. | I have accessed the admin portal and viewed the transcription history | I view the file expiration dates displayed next to each transcription file | The system accurately displays the expiration dates for all stored files, allowing me to take necessary actions before deletion |
