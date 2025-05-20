# Email Configuration Guideline

This document provides step-by-step instructions to configure the email sending functionality of the delivered system. It uses environment variables to keep sensitive information secure and allows flexible configuration without modifying the source code.

---

## Requirements

- A working email account that supports SMTP (e.g., Gmail, Outlook, company email)
- Access to the server or hosting environment

---

## Step 1: Create a `.env` file

Navigate to the root directory of your deployed project (where the executable or service entry point is located) and create a file named `.env`.

```bash
touch .env
```

## Step 2: Add the following content to `.env`

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_specific_password
```

> 💡 For Gmail users: It is strongly recommended to use an **App Password** instead of your main account password. You can generate this in your Google Account under "Security > App Passwords."

## Step 3: Restart the Application

Once the `.env` file is saved, restart your application or service. The environment variables will be automatically loaded at runtime.

---
