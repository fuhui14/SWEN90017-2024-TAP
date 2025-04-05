import json
from datetime import timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from transcription.models import Transcription

# 导入 Fernet 相关模块以及 Django 配置
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings

@csrf_exempt
def admin_history(request):
    """
    管理后台查看转录历史记录接口
    前端通过 POST 方式传入 JSON 数据 { "enc": "加密数据" }
    这里的加密数据经过解密后得到用户邮箱，然后根据该邮箱查询对应的转录记录。
    """
    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "请求体必须为合法的 JSON 格式"}, status=400)

        encrypted = body.get("enc")
        if not encrypted:
            return JsonResponse({"error": "缺少加密数据"}, status=400)

        # 使用 Fernet 对称加密解密前端传来的数据
        try:
            f = Fernet(settings.FERNET_KEY)
            decrypted_bytes = f.decrypt(encrypted.encode())
            email = decrypted_bytes.decode("utf-8")
        except InvalidToken:
            return JsonResponse({"error": "无效的加密数据"}, status=403)

        # 根据解密后的邮箱查找对应的转录记录
        # 注意这里使用 file__email 过滤 Transcription 的外键关联的 File 模型中的 email 字段
        transcriptions = Transcription.objects.select_related('file').filter(file__email=email)
        history_data = []

        for transcription in transcriptions:
            # 使用 File 模型中的 upload_timestamp 作为创建日期
            creation_date = (
                transcription.file.upload_timestamp
                if transcription.file.upload_timestamp
                else timezone.now()
            )
            # 记录保存 30 天，计算剩余天数
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

        return JsonResponse(history_data, safe=False)
    else:
        return JsonResponse({"error": "仅支持 POST 方法"}, status=405)
