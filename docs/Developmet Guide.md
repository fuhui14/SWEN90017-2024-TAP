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
    - Email settings: Modify the "SMTP_SERVER" and "SMTP_USER" and "SMTP_PASSWORD" to your own SMTP Infomation.
    - HuggingFace setting: Modify the "HF_TOKEN" to your own HuggingFace token, this token is used to download the AI model when you first time start the server.

## Start service
Go to **code/backend** folder, enter:
```
./start.sh
```
to run the start server script. Both frontend and backend server will start.

## Notices:
- When you start the server for the first time on a new computer, it will take some time to download the model. You can use the model offline without downloading it later.
- If the start server fail with "no module" alert, download the python model with **pip install abc** (where abc is the module missing).
