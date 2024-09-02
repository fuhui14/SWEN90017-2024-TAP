# Transcription Aide Platform - Domain Model

The Domain Model is used to describe the key concepts, objects and their relationships in the business domain. It helps the development team better understand business requirements and ensure that technical implementation is consistent with business requirements.

## Domain Model

![domain_model](../imgs/Architecture%20diagram/domain_model.png)

## Domain Model Explanation

The domain model contains three objects which shows the main business requirements of this project.

- **User:**
  - User use an email address to upload file and check history record.
  - An User can upload many files and has many histories.
- **File:**
  - File has it's own file name and file type(audio or video).
  - File also contains an uploaded date, which will be used to check if the file is expired.
  - An status of file is used to shown whether the file has completed transcription or not.
- **History**
  - Each history record includes a file and an expire time.
