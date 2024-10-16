import os
import uuid
import platform
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pathlib import Path
import shutil
import whisper

from speaker_identify.assign_speaker_service import assign_speakers_to_transcription
from .forms import UploadFileForm
from .models import File, Transcription  # 确保 File 和 Transcription 模型已定义

# 在应用启动时加载 Whisper 模型
model = whisper.load_model("base")

@csrf_exempt
def transcribe(request):
    print("Received a request to transcribe")
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid")

            # 提取用户的邮箱
            email = form.cleaned_data.get('email')
            print(f"User email: {email}")

            # 保存上传的文件
            file = request.FILES['file']
            upload_id = uuid.uuid4()  # 生成唯一标识符
            original_filename = file.name
            print(f"Original filename: {original_filename}, Upload ID: {upload_id}")

            # 根据结构化存储策略定义文件路径
            sanitized_email = email.replace('@', '_at_').replace('.', '_dot_')  # 确保路径不包含非法字符
            storage_dir = os.path.join(settings.MEDIA_ROOT, 'uploads', sanitized_email, upload_id.hex)
            try:
                os.makedirs(storage_dir, exist_ok=True)
            except OSError as e:
                print(f"Error creating directory: {e}")
                return JsonResponse({'error': f'Unable to create storage directory: {str(e)}'}, status=500)

            file_path = os.path.join(storage_dir, original_filename)
            print(f"Storage directory: {storage_dir}, File path: {file_path}")

            try:
                with open(file_path, 'wb') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                print("File saved successfully")
            except Exception as e:
                print(f"Error saving file: {e}")
                return JsonResponse({'error': f'Error saving file: {str(e)}'}, status=500)

            # 检查文件是否成功保存
            if not os.path.exists(file_path):
                print(f"File does not exist after saving: {file_path}")
                return JsonResponse({'error': f'File not found after saving: {file_path}'}, status=500)

            # 将文件元数据存储到数据库
            try:
                db_file = File.objects.create(
                    email=email,
                    upload_id=upload_id,
                    original_filename=original_filename,
                    storage_path=file_path,
                    file_size=file.size,
                    status='uploaded'
                )
                print(f"File metadata saved in database with ID: {db_file.id}")
            except Exception as e:
                print("Error saving file metadata to the database:", e)
                return JsonResponse({'error': f'Database error: Unable to save file metadata: {str(e)}'}, status=500)

            # 转录音频文件并存储转录文本
            try:
                print(f"Starting transcription for file: {file_path}")
                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"The file at {file_path} does not exist")
                transcription = transcribe_audio(file_path)  # 根据操作系统调整路径格式
                transcription_with_speaker = assign_speakers_to_transcription(transcription, file_path)
                Transcription.objects.create(
                    file=db_file,
                    transcribed_text=transcription_with_speaker
                )
                print("Transcription saved in database")
            except FileNotFoundError as fnf_error:
                print(f"File not found during transcription: {fnf_error}")
                return JsonResponse({'error': f'Transcription error: File not found {str(fnf_error)}'}, status=500)
            except Exception as e:
                print(f"Error during transcription or saving transcription for file {file_path}: {e}")
                return JsonResponse({'error': f'Transcription error: {str(e)}'}, status=500)

            # 返回转录结果
            print("Returning transcription result")
            return JsonResponse({"transcription": transcription_with_speaker}, safe=False)

        else:
            print("Form is not valid")
            errors = form.errors.as_json()
            print(f"Form errors: {errors}")
            return JsonResponse({'error': f'Invalid form submission: {errors}'}, status=400)

    else:
        print("GET request received; rendering form")
        form = UploadFileForm()
    return render(request, 'index.html', {'form': form})

def transcribe_audio(audio_path):
    """
    使用 Whisper 模型转录给定的音频文件。
    """
    print('Transcribing audio file at path: ' + audio_path)  # 更详细的调试信息
    try:
        system_platform = platform.system()
        if system_platform == 'Windows':
            # 在 Windows 上，将路径转换为原始字符串格式
            audio_path = r'{}'.format(audio_path)
            print('Path:::' + audio_path)
        # 在非 Windows 系统上，保持原始的路径格式

        result = model.transcribe(audio_path)
        return result
    except FileNotFoundError as fnf_error:
        print(f"File not found error during transcription: {fnf_error}")
        raise
    except Exception as e:
        print(f"General error during transcription: {e}")
        raise