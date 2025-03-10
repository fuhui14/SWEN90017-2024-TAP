from django.db import models
import uuid

class File(models.Model):
    email = models.EmailField(max_length=255)  # 用户的邮箱，用于识别用户
    upload_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)  # 文件上传的唯一标识符
    original_filename = models.CharField(max_length=255)  # 文件的原始名称
    storage_path = models.CharField(max_length=1024)  # 文件在服务器上的存储路径
    file_size = models.BigIntegerField()  # 文件大小，以字节为单位
    status = models.CharField(max_length=50, default='uploaded')  # 文件状态，如 'uploaded', 'processing', 'completed'
    upload_timestamp = models.DateTimeField(auto_now_add=True)  # 文件上传的时间戳
    processing_start_time = models.DateTimeField(null=True, blank=True)  # 处理开始时间
    processing_end_time = models.DateTimeField(null=True, blank=True)  # 处理结束时间

    class Meta:
        db_table = 'file'  # Specify exact table name in the database

    def __str__(self):
        return f"File {self.original_filename} ({self.upload_id})"

class Transcription(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)  # 外键关联到File模型
    transcribed_text = models.TextField()  # 转录后的文本
    created_at = models.DateTimeField(auto_now_add=True)  # 转录创建时间

    class Meta:
        db_table = 'transcription'  # Specify exact table name in the database

    def __str__(self):
        return f"Transcription for {self.file.original_filename}"