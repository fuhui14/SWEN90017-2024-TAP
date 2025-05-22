# Development Guide

## Overview
The purpose of this guide is to help you set up this project and start the server.

## Preperation
- Install **python 3.12.3** and **node.js**.

- Go to **code/backend** folder, enter:
    ```
    pip install -r requirements.txt
    ```
    to install all required library for backend.

- Modify the **config/settings.py**:
    - HuggingFace setting: Modify the "HF_TOKEN" to your own HuggingFace token, this token is used to download the AI model when you first time start the server.

- Check the **Email Configuration Guideline.md** and modify your SMTP info.

- Open the folder of this project in terminal and run the following command to install required packages and models for translation service.

```
python ./code/backend/translation/set_env.py
```

## Start service
Go to **code/backend** folder, enter:
```
./start.sh
```
to run the start server script. Both frontend and backend server will start.

## Notices:
- When you start the server for the first time on a new computer, it will take some time to download the model. You can use the model offline without downloading it later.
- If the start server fail with "no module" alert, download the python model with **pip install abc** (where abc is the module missing).

## Usage Guidline:

- Transcribe:
  - Click "Transcribe" to new page.
  - Upload your audio or video files (recommand max 3), enter your email address.
  - Choose your result type and language.
  - Click "Transcribe" button.
  - Wait for your result.
  - Click download button to download your result or download from email.

- History record:
  - Click "History" to new page.
  - Enter your email address and click "Send Email".
  - Open your email and open the access link.
  - View your history record.
