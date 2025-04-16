## Bug Report Introduction
During the development process, systematically recording and tracking bugs is essential for ensuring software quality and maintaining project progress. This document is intended to provide a structured format for reporting bugs encountered throughout the project lifecycle.

|Field | Description|
|-------|-----------|
|Bug ID | A unique identifier for each bug (e.g., BUG-20250415-01)|
|Description | A clear explanation of the bug and its symptoms|
|Reproduction Steps | Step-by-step guide to consistently reproduce the issue|
|Reporter | The team member who discovered the bug|
|Assignee | The person responsible for investigating/fixing the bug|
|Status | The current state of the bug (e.g., Open, In Progress, Fixed, Closed)|
|Fix / PR Link | Related pull request or commit resolving the issue|
|Final Notes | Any additional context, remarks, or links|

Using a consistent reporting template helps the team collaborate more efficiently when identifying issues, confirming fixes, and referencing past problems.

All team members are encouraged to log bugs as soon as they are discovered and to keep the status updated, ensuring transparency throughout the bug's lifecycle.

## Bug ID: BUG-20250324-01

**Description**: A typo found during the unit test

**Reproduction Steps**:
1. Navigate to `/code/frontend/src/about/about.js`
2. There is a typo: "Transcription Aid Plaltform"

```javascript
<section className="hero-section">
    <h3> Transcription Aid Plaltform</h3>
    <p>Everything you need to transcribe audio filesat your fingertips.0ur platform is 100% free and easy to use!Upload, process, and receive your transcriptions with justa few clicks -no login reguired. Identify different speakershandle multiple files, and receive results directly via email.</p>
</section >
```

**Reporter**: @Eclipsezty

**Assignee**: @Eclipsezty 

**Status**: Closed 

**Fix / PR Link**: [Commit 5a9baa7](https://github.com/fuhui14/SWEN90017-2024-TAP/commit/5a9baa7faa462f89be1942dae213b3d3ab4ad9bf) 

**Final Notes**: Adjust typo on About.js and finish unit test

## Bug ID: BUG-20250402-01

**Description**: Backend error - Can not find the file under given path when using winddows system to transcribe the audio file

**Reproduction Steps**:
1. Run the backend server, with following command, under code/backend path
```
python manage.py run server
``` 
2. Run the React frontend with following command:
```
cd code/frontend
npm run start
```
3. Go to Transcription page
4. Input correct Email address
5. Select desired format for the output file
    - txt for example
6. Select transcription language
    - English for example
7. Upload an auido file
8. Click Upload Button
9. Transcription error happens


**Reporter**: @Baye0110

**Assignee**: @Baye0110

**Status**: Closed 

**Fix / PR Link**: [Commit 9ebbde8](https://github.com/fuhui14/SWEN90017-2024-TAP/commit/9ebbde852291db6c91831ea3ba378828e9729e61) 

**Final Notes**: fix the windows bug

## Bug ID: BUG-20250319-01

**Description**: On project startup, when uploading a file for transcription, a "connection refused" error is displayed. The issue occurs because Celery is not running.

**Reproduction Steps**:
1. Start the backend server.
2. Start the React frontend.
3. Navigate to the Transcription page.
4. Enter a valid email address and select the desired output format and transcription language.
5. Upload an audio file.
6. Click the Upload Button.
7. The system displays a "connection refused" error.
8. Investigation reveals that Celery is not running.
9. To resolve the issue, execute the following commands in the backend environment:
    ```
    celery -A config beat -I info
    celery -A config worker -I info
    ```
10. Restart the file upload process to confirm the issue is resolved.

**Reporter**: @Joey-Chen-259

**Assignee**: @Joey-Chen-259

**Status**: Closed

**Fix / PR Link**: N/A

**Final Notes**: Ensure that the Celery commands are run in the backend environment to properly initialize the task queue and avoid connection errors during the transcription process.
