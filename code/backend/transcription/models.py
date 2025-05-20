from django.db import models
import uuid

class File(models.Model):
    email = models.EmailField(max_length=255)  # User's email address, used for identification
    upload_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)  # Unique identifier for the uploaded file
    original_filename = models.CharField(max_length=255)  # Original name of the file
    storage_path = models.CharField(max_length=1024)  # Path where the file is stored on the server
    file_size = models.BigIntegerField()  # File size in bytes
    status = models.CharField(max_length=50, default='uploaded')  # File status, e.g., 'uploaded', 'processing', 'completed'
    upload_timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of when the file was uploaded
    processing_start_time = models.DateTimeField(null=True, blank=True)  # Processing start time
    processing_end_time = models.DateTimeField(null=True, blank=True)  # Processing end time
    portal_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)  # secure access link

    class Meta:
        db_table = 'file'  # Specify exact table name in the database

    def __str__(self):
        return f"File {self.original_filename} ({self.upload_id})"

class Transcription(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)  # Foreign key linking to the File model
    transcribed_text = models.TextField()  # The transcribed text content
    created_at = models.DateTimeField(auto_now_add=True)# Timestamp when the transcription was created

    class Meta:
        db_table = 'transcription'  # Specify exact table name in the database

    def __str__(self):
        return f"Transcription for {self.file.original_filename}"