from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from canvasapi import Canvas
from .services import save_user_token
from .utils import encrypt_token
from .models import EncryptedToken
import json

@csrf_exempt
def validate_token(req):
    """토큰의 유효성을 검사하고, 유효하면 저장 후 사용자 이름 반환"""
    if req.method == 'POST':
        try:
            data = json.loads(req.body)
            token = data.get('token')
            if not token:
                return JsonResponse({'valid': False, 'error': '토큰이 없습니다.'}, status=400)
            API_URL = "https://knulms.kongju.ac.kr/"
            canvas = Canvas(API_URL, token)
            user = canvas.get_current_user()  # 유효성 검사
            save_user_token(token)
            return JsonResponse({'user_name': user.name})
        except Exception as e:
            return JsonResponse({'valid': False, 'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'POST 요청만 허용됩니다.'}, status=405)

@csrf_exempt
def logout(req):
    """토큰을 받아 DB에서 삭제 (로그아웃)"""
    if req.method == "POST":
        try:
            data = json.loads(req.body)
            token = data.get('token')
            if not token:
                return JsonResponse({'success': False, 'error': '토큰이 없습니다.'}, status=400)
            encrypted = encrypt_token(token)
            deleted, _ = EncryptedToken.objects.filter(token=encrypted).delete()
            if deleted:
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': '토큰이 DB에 없습니다.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'POST 요청만 가능합니다.'}, status=405)