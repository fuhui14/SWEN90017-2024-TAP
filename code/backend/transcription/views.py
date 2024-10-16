import os
import uuid
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from speaker_identify.assign_speaker_service import assign_speakers_to_transcription
from .forms import UploadFileForm
from .transcribe_service import transcribe_audio
from .models import File, Transcription  # 确保File和Transcription模型已定义

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
            storage_dir = os.path.join(settings.MEDIA_ROOT, 'uploads', email, upload_id.hex)
            os.makedirs(storage_dir, exist_ok=True)
            file_path = os.path.join(storage_dir, original_filename)
            print(f"Storage directory: {storage_dir}, File path: {file_path}")

            with open(file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            print("File saved successfully")

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
                return JsonResponse({'error': 'Database error: Unable to save file metadata'}, status=500)

            # 转录音频文件并存储转录文本
            try:
                transcription = transcribe_audio(file_path)
                transcription_with_speaker = assign_speakers_to_transcription(transcription, file_path)
                Transcription.objects.create(
                    file=db_file,
                    transcribed_text=transcription_with_speaker
                )
                print("Transcription saved in database")
            except Exception as e:
                print("Error during transcription or saving transcription:", e)
                return JsonResponse({'error': 'Transcription error'}, status=500)

            # 返回转录结果
            print("Returning transcription result")
            return JsonResponse({"transcription": transcription_with_speaker}, safe=False)

        else:
            print("Form is not valid")
            return JsonResponse({'error': 'Invalid form submission'}, status=400)

    else:
        print("GET request received; rendering form")
        form = UploadFileForm()
    return render(request, 'index.html', {'form': form})