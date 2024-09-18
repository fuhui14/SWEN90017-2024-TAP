
# Transcription and Speaker Identification Backend Project

This is a project that provides API endpoints for speech transcription and speaker identification using Django and Django Rest Framework (DRF). The project supports asynchronous task processing using Celery and Redis for background job handling.

## Table of Contents
- [Project Structure](#project-structure)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [API Endpoints](#api-endpoints)
- [Technologies Used](#technologies-used)
- [Database Setup](#database-setup)
- [Asynchronous Tasks](#asynchronous-tasks)
- [Testing](#testing)

---

## Project Structure

```bash
transcription_project/
│
├── manage.py                    # Django management command
├── requirements.txt             # Backend dependencies
├── .env                         # Environment variables file
├── .gitignore                   # Git ignore file
│
├── config/                      # Project settings and configuration
│   ├── __init__.py
│   ├── settings.py              # Django global settings (includes database settings)
│   ├── urls.py                  # Main entry for routing API endpoints
│   ├── asgi.py                  # ASGI for asynchronous support
│   └── wsgi.py                  # WSGI for deployment
│
├── core/                        # Core application (generic logic and shared utilities)
│   ├── __init__.py
│   ├── models.py                # Generic models, if needed
│   ├── views.py                 # Core API views logic (if necessary)
│   ├── urls.py                  # Core app API routes
│   └── serializers.py           # Data serialization for generic core responses
│
├── transcription/               # Transcription app (handles transcription processes)
│   ├── __init__.py
│   ├── models.py                # Transcription-related data models
│   ├── views.py                 # Transcription API views logic
│   ├── urls.py                  # Transcription app API routes
│   ├── tasks.py                 # Asynchronous tasks (e.g., calling external speech recognition APIs)
│   ├── transcribe_service.py    # Logic for integrating external transcription services
│   └── serializers.py           # Transcription data serialization
│
├── speaker_identify/            # Speaker identification app
│   ├── __init__.py
│   ├── models.py                # Speaker identification-related data models
│   ├── views.py                 # Speaker identification API views logic
│   ├── urls.py                  # Speaker identification API routes
│   ├── identify_service.py      # Logic for identifying speakers in audio files
│   └── serializers.py           # Speaker identification data serialization
│
├── api/                         # General API (for non-specific or cross-app APIs)
│   ├── __init__.py
│   ├── urls.py                  # API global routes (including versioning if needed)
│   └── views.py                 # General API views
│
└── tests/                       # Unit and integration tests
    ├── test_core.py             # Core app tests
    ├── test_transcription.py    # Transcription app tests
    └── test_speaker_identify.py # Speaker identification app tests
```

---

## Installation

### 1. Clone the Repository
First, clone the project to your local machine:
```bash
git clone https://github.com/yourusername/transcription_project.git
cd transcription_project
```

### 2. Set up a Python Virtual Environment
Create a Python virtual environment to install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

### 3. Install Dependencies
Use \`pip\` to install the project dependencies listed in \`requirements.txt\`:
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Create a \`.env\` file in the root of your project and add the following environment variables:
```
SECRET_KEY=your_secret_key_here
DEBUG=True
DATABASE_URL=your_database_url_here  # or use settings from 'settings.py'
CELERY_BROKER_URL=redis://localhost:6379/0  # For Redis
```

---

## How to Run

### 1. Database Setup

Before running the application, you need to configure the database and apply migrations.

#### PostgreSQL (Recommended)
Make sure you have PostgreSQL installed and running. Create a database named \`transcription_db\` or configure your database settings in \`config/settings.py\`.

Then, run the following commands:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Run Redis for Celery (Asynchronous Tasks)
For background tasks, you need to have Redis running:
```bash
redis-server
```

### 3. Run Celery Worker
In a separate terminal, run the Celery worker to handle asynchronous tasks:
```bash
celery -A config worker --loglevel=info
```

### 4. Run the Django Server
You can now run the Django development server:
```bash
python manage.py runserver
```

Access the server at \`http://127.0.0.1:8000/\`.

---

## API Endpoints

### Transcription API
- **POST** \`/api/transcription/\`: Upload an audio file and receive transcription text.
- **GET** \`/api/transcription/<id>/\`: Get the transcription result for a specific transcription.

### Speaker Identification API
- **POST** \`/api/speaker-identify/\`: Upload an audio file and identify the speaker.
- **GET** \`/api/speaker-identify/<id>/\`: Get the speaker identification result.

---

## Technologies Used

- **Django**: Web framework for building the backend API.
- **Django REST Framework (DRF)**: For creating RESTful APIs.
- **Celery**: For asynchronous task management (e.g., speech transcription, speaker identification).
- **Redis**: As a message broker for Celery.
- **PostgreSQL**: For database management.
- **Google Speech-to-Text** (or other services): For handling transcription (if using an external service).
- **pyAudioAnalysis**: For speaker identification (optional, if integrated).

---

## Database Setup

### Database Configuration

The project uses Django's ORM (Object-Relational Mapping) for managing the database. By default, it is configured to use **PostgreSQL**, but you can change this in \`config/settings.py\` if needed.

Example for PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'transcription_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

If you are using another database, such as SQLite, you can update the configuration accordingly.

### Running Migrations

After setting up your database connection, apply migrations to create the required tables:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Asynchronous Tasks

To handle long-running tasks such as speech transcription and speaker identification, we use **Celery**.

### Steps to Set Up Celery:
1. Make sure **Redis** is installed and running as the message broker.
2. Configure **Celery** in \`config/celery.py\`.
3. Start the **Celery worker**:
   ```bash
   celery -A config worker --loglevel=info
   ```

Celery tasks are defined in the \`tasks.py\` file of each app (e.g., \`transcription/tasks.py\`).

---

## Testing

To run the project's test cases, use the following command:
```bash
python manage.py test
```

Test cases are located in the \`tests/\` directory, with separate tests for transcription and speaker identification functionalities.

---

