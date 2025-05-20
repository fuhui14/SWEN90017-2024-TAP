import json
from datetime import timedelta
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from transcription.models import Transcription

# 导入 Fernet 相关模块以及 Django 配置
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings


@csrf_exempt
def admin_history(request):
    print(f"Received request with method: {request.method}")

    if request.method == "POST":
        try:
            body = json.loads(request.body)
            print(f"Request JSON parsed successfully: {body}")
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            return JsonResponse({"error": "请求体必须为合法的 JSON 格式"}, status=400)

        encrypted = body.get("enc")
        print(f"Extracted encrypted value: {encrypted}")
        if not encrypted:
            print("No encrypted data provided in the request.")
            return JsonResponse({"error": "缺少加密数据"}, status=400)

        # 使用 Fernet 对称加密解密前端传来的数据
        try:
            f = Fernet(settings.FERNET_KEY)
            print(f"Fernet instance created using key: {settings.FERNET_KEY}")
            decrypted_bytes = f.decrypt(encrypted.encode(), ttl=2592000)
            email = decrypted_bytes.decode("utf-8")
            print(f"Decrypted email: {email}")
        except InvalidToken as e:
            print(f"InvalidToken error during decryption: {e}")
            return JsonResponse({"error": "无效的加密数据"}, status=403)
        except Exception as e:
            print(f"Exception during decryption: {e}")
            return JsonResponse({"error": "解密过程出错"}, status=500)

        # 根据解密后的邮箱查找对应的转录记录
        try:
            transcriptions = Transcription.objects.select_related('file').filter(file__email=email)
            count = transcriptions.count()
            print(f"Found {count} transcription record(s) for email: {email}")
        except Exception as e:
            print(f"Database query error: {e}")
            return JsonResponse({"error": "查询数据库出错"}, status=500)

        history_data = []
        for transcription in transcriptions:
            # 使用 File 模型中的 upload_timestamp 作为创建日期
            creation_date = (
                transcription.file.upload_timestamp
                if transcription.file.upload_timestamp
                else timezone.now()
            )
            expiry_date = creation_date + timedelta(days=30)
            days_left = (expiry_date - timezone.now()).days
            if days_left < 0:
                days_left = 0

            record = {
                "id": transcription.id,
                "taskName": transcription.file.original_filename if transcription.file else "",
                "taskType": "Transcription",
                "creationDate": creation_date.isoformat(),
                "daysLeft": days_left,
                "outputType": "text",
                "status": "Completed" if transcription.transcribed_text else "Failed",
            }
            history_data.append(record)
            print(f"Processed transcription record: {record}")

        print("Returning history data to client.")
        return JsonResponse(history_data, safe=False)
    else:
        print("Unsupported HTTP method encountered.")
        return JsonResponse({"error": "仅支持 POST 方法"}, status=405)


@csrf_exempt
def download_history(request):
    print(f"Download request received with method: {request.method}")
    if request.method != "POST":
        return JsonResponse({"error": "仅支持 POST 方法"}, status=405)

    try:
        body = json.loads(request.body)
        record_id = body.get("id")
        if not record_id:
            return JsonResponse({"error": "缺少记录ID"}, status=400)
        print(f"Download request for record ID: {record_id}")
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        return JsonResponse({"error": "请求体必须为合法的 JSON 格式"}, status=400)

    try:
        transcription = Transcription.objects.select_related('file').get(id=record_id)
    except Transcription.DoesNotExist:
        print("Transcription record does not exist.")
        return JsonResponse({"error": "记录不存在"}, status=404)
    except Exception as e:
        print(f"Database query error: {e}")
        return JsonResponse({"error": "查询数据库出错"}, status=500)

    # 获取转录后的文本内容
    text_content = transcription.transcribed_text
    if not text_content:
        return JsonResponse({"error": "无转录内容可供下载"}, status=404)

    # 返回纯文本文件下载
    response = HttpResponse(text_content, content_type="text/plain")
    # 如果 File 模型中提供了原始文件名，则使用之，否则使用默认文件名
    filename = transcription.file.original_filename if transcription.file and transcription.file.original_filename else "transcription"
    response['Content-Disposition'] = f'attachment; filename="{filename}.txt"'
    print("Download response prepared, returning file to client.")
    return response
