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
1. Navigate to `/about.js`
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
