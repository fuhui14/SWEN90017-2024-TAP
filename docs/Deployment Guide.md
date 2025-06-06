# Deployment Guide

## Overview

The purpose of this guide is to help you set up this project and start the server.

## Recommended devices:
- System: Mac OS 15.5
- Chips: Apple M2
- Memory: 24GB

## Preperation

* Install **python 3.12.3** and **node.js**.

* Install **Redis** (>= 7.0) and make sure the Redis server is running *before* you start the project.

  **macOS (Homebrew):**

  ```bash
  brew install redis
  redis-server
  ```

  **Ubuntu / Debian:**

  ```bash
  sudo apt-get update
  sudo apt-get install redis-server
  sudo systemctl enable --now redis-server
  ```

  **Windows (Chocolatey):**

  ```powershell
  choco install redis-64
  redis-server
  ```

  Verify the installation:

  ```bash
  redis-cli ping    # should reply: PONG
  ```

* Go to **code/backend** folder, enter:

  ```bash
  pip install -r requirements.txt
  ```

  to install all required library for backend.

* Modify the **config/settings.py**:

  * HuggingFace setting: Modify the "HF\_TOKEN" to your own HuggingFace token, this token is used to download the AI model when you first time start the server.

  * **Database setting**: Update the “DATABASES” configuration.  
      For quick testing, you can switch to SQLite with the following setting:

      ```python
      DATABASES = {
          'default': {
              'ENGINE': 'django.db.backends.sqlite3',
              'NAME': BASE_DIR / 'db.sqlite3',
          }
      }
      ```

      If you prefer using PostgreSQL locally, make sure to install it and update the credentials (NAME, USER, PASSWORD, HOST, PORT) accordingly.


* Check the **Email Configuration Guideline.md** and modify your SMTP info.

* Open the folder of this project in terminal and run the following command to install required packages and models for translation service.

  ```bash
  python ./code/backend/translation/set_env.py
  ```

## Start service

Go to **code/backend** folder, enter:

```bash
./start.sh
```

to run the start server script. Both frontend and backend server will start.

## Notices:

* When you start the server for the first time on a new computer, it will take some time to download the model. You can use the model offline without downloading it later.
* If the start server fail with "no module" alert, download the python model with **pip install abc** (where abc is the module missing).
* Estimated transcription time:

  * Approximately **1 hour** is needed to transcribe **30 minutes** of audio.
  * Approximately **2+ hours** is needed to transcribe **1 hour** of audio.

  The actual time may vary depending on your device performance and system load.


## Usage Guidline:

* Transcribe:

  * Click "Transcribe" to new page.
  * Upload your audio or video files (recommand max 3), enter your email address.
  * Choose your result type and language.
  * Click "Transcribe" button.
  * Wait for your result.
  * Click download button to download your result or download from email.

* History record:

  * Click "History" to new page.
  * Enter your email address and click "Send Email".
  * Open your email and open the access link.
  * View your history record.
