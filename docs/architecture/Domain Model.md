# Transcription Aide Platform - Domain Model

The Domain Model is used to describe the key concepts, objects and their relationships in the business domain. It helps the development team better understand business requirements and ensure that technical implementation is consistent with business requirements.

## Domain Model

![domain_model](../imgs/Architecture%20diagram/domain_model.png)

## Domain Model Explanation

The domain model contains six objects which shows the main business requirements of this project.

- **User:**
  - Attribute:
    - Email address: User use an email address to upload file and check history record.
  - An User can upload file to the transcription queue and access history record.
- **File:**

  - Attribute:
    - File name: Name of the file.
    - File type: Type of the file, for example, .doc, .txt.
    - Language: The language in which the document is transcribed.
    - Creator email: Email address of the user who upload the file.
    - Status: Status of the file, such as "Waiting", "Processing", "Completed".
    - Translated Date: The date when the file complete transcription.
    - Upload Date: The date when the file is uploaded.
    - Processing Progress: The current processing progress of the file, expressed as a percentage, such as "50%".
    - Speaker Number: The number of speaker being identified.
    - Transcription text: The content of the transcription, store in a conversation form.

- **History Record**
  - Attribute:
    - File: History record include a temporary transcription file store in local.
    - Expire Time: Shows the expire time for the transcription file.
    - Email Address: Used to identify the creator of the history record.
  - History Record is used to record the transcription file and can be checked by user.
- **File Manager**
  - Attribute:
    - History Record: File manager has many history record.
  - File Manager will manage all history records and check if they are expired.
- **Transcription Queue**
  - Attribute:
    - Waiting Files: The transcription queue will keep track of files waiting to be transcribed and files currently being transcribed.
    - Estimated Waiting Time: Shows the estimated waiting time for each file.
    - Error reports: When there is a error occur when processing transcription, an error report will be created and sent to the user.
  - The transcription queue will manage the transcription of all files and create the error report.
- **Error Report**
  - Attribute:
    - Report time: The time when the report is created.
    - Files name: The name of the file which occur error when processing.
    - Error info: Detailed error info which helps the user to understand what had happened.
    - Report email: User's email address to received the error report.
  - The Error report is created by the transcription queue when error occur and will be sent to the user. The report contains info to help the user understand what happened.
