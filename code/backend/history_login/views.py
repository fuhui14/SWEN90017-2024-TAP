import json
import urllib.parse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from cryptography.fernet import Fernet
from django.conf import settings

# 假设发送邮件的函数已经写好，可以直接导入使用
# 根据你的项目结构，调整导入路径，例如：
# from emails.send_email import send_email
from emails.send_email import send_email

@csrf_exempt
def send_history_link(request):
    """
    接收前端传递的邮箱地址，将邮箱加密后生成查看历史记录的链接，
    并调用邮件发送函数将该链接发送到用户邮箱。
    前端传入 JSON 数据示例： { "email": "user@example.com" }
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")  # 打印解析 JSON 异常信息
            return JsonResponse({"message": "请求体必须为合法的 JSON 格式"}, status=400)

        email = data.get("email")
        if not email:
            print("Email is missing from request data")  # 打印缺少邮箱信息
            return JsonResponse({"message": "缺少邮箱信息"}, status=400)

        # 使用 Fernet 对称加密对邮箱信息进行加密
        try:
            f = Fernet(settings.FERNET_KEY)
            encrypted_bytes = f.encrypt(email.encode('utf-8'))
            encrypted_email = encrypted_bytes.decode('utf-8')
        except Exception as e:
            print(f"Encryption error: {e}")  # 打印加密异常信息
            return JsonResponse({"message": "加密邮箱信息失败"}, status=500)

        # 生成历史记录查看链接
        frontend_url = getattr(settings, "FRONTEND_URL", "http://127.0.0.1:3000")
        history_link = f"{frontend_url}/history?enc={urllib.parse.quote(encrypted_email)}"

        # 构造邮件内容
        subject = "您的历史记录访问链接"
        content = (
            f"您好，\n\n请点击以下链接以查看您的转录历史记录：\n"
            f"{history_link}\n\n该链接有效期为 30 天。"
        )

        # 调用邮件发送函数，file_content 为空字符串，不需要附件
        try:
            send_email(receiver=email, subject=subject, content=content, file_content="")
        except Exception as e:
            print(f"Send email error: {e}")  # 打印发送邮件异常信息
            return JsonResponse({"message": "发送邮件失败"}, status=500)

        return JsonResponse({"message": "登录链接已发送至您的邮箱，请检查收件箱。"})
    else:
        print("Unsupported HTTP method")  # 打印不支持的 HTTP 方法信息
        return JsonResponse({"message": "仅支持 POST 方法"}, status=405)
