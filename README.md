# SWEN90017 - 2024 - Transcription Aide Platform (TAP)

## Project Overview

### Introduction
This project aims to develop a transcription platform that operates in a local environment using OpenAI's Whisper software. The platform is designed for a team working within a secure local area network (LAN), allowing team members to upload audio files for transcription without the need for user login.

### Key Components
#### 1. Web Interface
- **File Upload**: A simple web interface enables users to upload audio files directly to the local machine.
- **User Simplicity**: No login is required, making the process straightforward for team members.
- **Email Input**: Users can provide an email address to receive the transcription once it's completed.

#### 2. Local Machine Execution
- **Transcription Software**: The local machine runs OpenAI's Whisper software to transcribe the uploaded audio files.
- **Speaker Identification**: The transcription process includes diarisation to identify different speakers within the audio.
- **Output Format**: The primary output is a readable text file (.txt) that captures the transcription with identified speakers and timing.

### Deployment & Performance
- **Secure LAN**: The platform is deployed within a secure local area network to ensure data privacy.
- **Scalability**: The platform can handle the transcription of multiple files concurrently.

### About the Project Team

The project is a Transcription Aide Platform by Team002 as a part of SWEN90017(Masters Advanced Software Project Part 1) at the University of Melbourne. The project comes from the client's needs and is supervised by the mentor -- **Mingye Li**. All team members are Masters of Software Engineering from the University of Melbourne.

#### Client
Diego Munoz Saez. Email Address: [dmunoz@swin.edu.au]().

#### Mentor
Mingye Li. Email Address: [ming.li1@unimelb.edu.au]()

#### Team Members
| Product Owner, Front-end Team Member | Scrum Master, Back-end Team Member |Development Lead (Back-end)|
|:-------:|:-------:|:-------:|
|Defining the product vision and prioritizing the backlog to align with stakeholder requirements and business value. Gather and parse the opinions of multiple stakeholders, acting as the middleman between the development team and clients. | Facilitating Scrum ceremonies, removing impediments, and coaching the team on Agile practices to ensure continuous improvement. | Providing technical leadership and guidance, ensuring code quality, and designing the back-end architecture.|
| <img src="docs/imgs/README/Tianyi.jpg" width="240" /> | <img src="docs/imgs/README/Fuhui.jpg" width="240" /> | <img src="docs/imgs/README/Zixuan.jpg" width="240" /> |
|Tianyi Zhong<br>*zhong17@student.unimelb.edu.au*|Fuhui Yang<br>*fuhui.yang@student.unimelb.edu.au*|Zixuan Zhang<br>*zixuzhang2@student.unimelb.edu.au*|
|**Development Lead (Front-end)**| **Architecture Lead, Back-end Team Member** | **User Experience Lead, Front-end Team Member** |
|  Providing technical leadership and guidance, ensuring code quality, and designing the front-end architecture. | Designing the overall system architecture, selecting appropriate technologies, and ensuring alignment with business goals. |  Conducting user research and designing intuitive, user-friendly interfaces. |
| <img src="docs/imgs/README/Lecheng.jpg" width="240" /> | <img src="docs/imgs/README/Claire.jpg" width="240" /> | <img src="docs/imgs/README/Yingrong.jpg" width="240" /> |
|Lecheng Chen<br>*lechengc@student.unimelb.edu.au*|Jiacheng(Claire) Shou<br>*jssho@student.unimelb.edu.au*|Yingrong Chen<br>*yingrong@student.unimelb.edu.au*|
|**Quality Assurance Lead, Front-end Team Member** | **Back-end Team Member** | **Back-end Team Member** |
| Planning and executing tests to ensure product quality and reliability. | Developing and maintaining server-side logic and APIs, optimizing performance, and ensuring data security. | Developing and maintaining server-side logic and APIs, optimizing performance, and ensuring data security. |
| <img src="docs/imgs/README/Yongjie.jpg" width="240" /> | <img src="docs/imgs/README/Pengyuan.jpg" width="240" /> | <img src="docs/imgs/README/Jiangyu.jpg" width="240" /> |
|Yongjie Ba<br>*yongjieb@student.unimelb.edu.au*|Pengyuan Yu<br>*pengyuany@student.unimelb.edu.au*|Jiangyu Chen<br>*jiangyuc2@student.unimelb.edu.au*|


### Directory Structure

```
├── code
│   ├── backend
│   ├── frontend
├── data samples
├── docs
│   ├── Architecture
│   ├── imgs
│   ├── meetings
│   │   ├── Agile Ceremony
│   │   ├── Client Meetings
│   │   ├── Team Meetings
│   │   └── Meeting Template
│   └── requirement
│   │   └── Personas
├── prototypes
│   ├── High Fidelity Prototype
│   ├── Low Fidelity Prototype
├── tests
└── README.md
```

## Changelog (Release Notes)

### Sprint 1

- Initialized the file structure
- Added meetings minutes during sprint 1 
- Create persona with explanation documentation
- Implement user stories
- Design the motivation model
- Add Acceptance Criteria
- Build low-fidelity & high-fidelity prototype with explanation documentations
- Make technology selection

### Sprint 2

- Create system architecture diagrams
  - Class diagram
  - Use case diagram
  - Sequence diagram
  - Component diagram
  - Domain diagram
  - Deployment diagram
  - Activity diagram
  - ER diagram
- Acknowledge speaker library
- Build development environment configuration
  - Front End
  - Back End
- Add risk management document
- Create communication plan
- Add mood board for high fidelity prototype

### Sprint 3

- Develop user stories for the priority of *Must Have*
- Separate development of front end and back end
- Relevant tests
- Integrate back end and front end

### Sprint 4

- Complete remaining *Must Have* user stories.
- Start development on *Should Have* & *Could Have* user stories.
- Ensure early front-end and back-end integration to prevent last-minute issues.
- Improve performance of identifying different speakers.
- Begin testing for completed features.

### Sprint 5

- Complete all remaining *Should Have* and *Could Have* user stories.
- Finalize admin portal and history features.
- Complete testing framework and ensure full integration.
- Optimize database, API, and file management system.
- Deliver feature-complete system for Sprint 6 validation.

### Sprint 6

- Complete regression and acceptance testing
- Finalize technical documentation, user manual, and test report
- Conduct client acceptance testing and address final feedback
- Prepare materials for Endeavor Exhibition (poster, demo script, risk assessment)
- Perform system handover and final delivery

## Important Links
- Github: https://github.com/Eclipsezty/SWEN90017-2024-TAP
- Kanban: https://github.com/users/Eclipsezty/projects/1/views/1
- Backlog(issues): https://github.com/Eclipsezty/SWEN90017-2024-TAP/issues
- Low Fidelity Prototype: https://www.figma.com/design/dUKziZzm2oo8kCkefUN3vS/TAP-Low-Fidelity?node-id=8-2349&t=vUWVQPpejumNpbcV-1
- High Fidelity Prototype: https://www.figma.com/design/zgg9tm6Nl6iH9f8ilOzibW/TAP-High-Fidelity?node-id=0-1&t=kjIHFZw31TVJB1zR-1
