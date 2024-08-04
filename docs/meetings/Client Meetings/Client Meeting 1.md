# TAP Client Meeting 1

**Date & Time:** xx/Aug/2024, 16:00-17:00

**Participant & Role:**
|Client|Supervisor|Product Owner|Scrum Master|Frontend Development Lead|Backend Development Lead|Quality Assurance Lead|Architecture Lead|User Experience Lead|Member|Member|
|---|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
|Diego Munoz Saez|Mingye Li|Tianyi Zhong|Fuhui Yang|Lecheng Chen|Zixuan Zhang|Yongjie Ba|Claire Shou|Yingrong Chen|Jiangyu Chen|Pengyuan Yu|

## Agenda


### 1. **Welcome and Introductions (5 minutes)**
   - Brief introductions by each participant.
   - Outline of the meeting's objectives.

### 2. **Project Overview (15 minutes)**
   - High-level overview of project goals and expected outcomes.
   - Client to describe their business needs and what they aim to achieve with the project.

### 3. **Project Requirements Discussion (30 minutes)**
   - Detailed discussion on specific project requirements.
   - Clarification of technical and business requirements.
   - Discussion of initial questions prepared by the team (see Question & Answer section).

### 4. **Closing Remarks (5 minutes)**
   - Thank the client and all participants for their time and input.
   - Express enthusiasm for the project’s commencement.
   - Scheduling of the next meeting.



## Decisions


## Action Items





## Question & Answer


#### Q: As mentioned in the slides, it takes Raspberry Pi 5 around 9 hours to transcribe a 1-hour audio file. So how much time do you expect our system to process the same file? (Pengyuan Yu)

A: 

#### Q: Do we need to store the result in the local database or in another format. If so, should they be kept indefinitely, or is there a retention policy? (Pengyuan Yu)

A: 

#### Q: Which core features do you expect the platform to have? For example, are file upload, transcription status monitoring, transcription result download or email delivery, and speaker identification sufficient? Additionally, when you mentioned a "simple web interface," do you mean having a simple color design and minimal interactive buttons (like only buttons for uploading files, downloading transcripts, and sending transcripts via email)? (Yingrong Chen)

A:

#### Q: What security measures do you expect us to implement for the platform, especially considering it will be used within a secure LAN? Are there any specific security protocols we should follow? (Claire Shou)

A: 

#### Q: Are there any specific performance requirements for the application? For example, do you expect it to handle a certain number of concurrent users or process a certain amount of data within a given time frame? (Claire Shou)

A:

#### Q: What are the expected input file formats for the application? Should it support audio files only, or are other formats like video or text files also required? (Claire Shou)

A:


#### Q: For the frontend design, can we use frameworks? Do you recommend us to use any specific framework? (Lecheng Chen)

A:

#### Q: do you have any requirements for the web interface's interactivity? For example, should we implement drag-and-drop functionality for file uploads? Do we need to make this project accessible on mobile platforms, or should it only be implemented for desktop use? (Lecheng Chen)

A:

#### Q: Whisper currently outputs the transcription as a single line of text. Do you need the text to be formatted into more readable paragraphs or sentences? (Fuhui Yang)

A:

#### Q: Do you have specific expectations regarding the accuracy of speaker identification(in terms of Whisper's confidence level)? (Fuhui Yang)

A:

#### Q: Do you need the speaker's timestamps to be marked in the transcription results? (Fuhui Yang)

A:

#### Q: Noticing that you mentioned in the introduction slides, does the platform need regular backups? If so, do you have any preferred frequency or method for the backups? (Fuhui Yang)

A:

#### Q: For the function of identifying different speaker, can we use other open source library on GitHub base on OpenAI Whisper? (Zixuan Zhang)

A:

#### Q: Considering future project updates, are there any requirements for the language used in backend server development? (Zixuan Zhang)

A:

#### Q: For the output results, what other file formats do you expect, such as pdf, jpg? (Zixuan Zhang)

A:

#### Q: If other open source libraries can provide both translation and voiceprint recognition, do we still need to use Whisper for the implementation? (Jiangyu Chen)

A:

#### Q: Does this project have any special performance requirements, such as the need to address high concurrency or handle large files, etc.? (Jiangyu Chen)

A:

#### Q: When identifying speakers, how specific do the details need to be? Is noting their gender sufficient, or is it also necessary to include a description of their voice type? (Yongjie Ba)

A:

#### Q: Could you provide us with some user cases in various scenarios? (Yongjie Ba)

A:

#### Q: Should the system include automated alerts or notifications for users when transcriptions are complete or if there are issues during processing? （Tianyi Zhong)

A:

### Meeting Recording

[The video recording of the meeting is on OneDrive](https://unimelbcloud-my.sharepoint.com/:v:/g/personal/xxxxxx)
