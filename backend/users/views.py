from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from canvasapi import Canvas
from .services import save_user_token, get_token_by_username
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
            user_name = user.name
            now = save_user_token(token, user_name)
            return JsonResponse({'user_name': user_name, 'last_login': now})
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
            user_name = data.get('user_name')
            if not user_name:
                return JsonResponse({'success': False, 'error': 'user_name이 없습니다.'}, status=400)
            token = get_token_by_username(user_name)
            if not token:
                return JsonResponse({'success': False, 'error': '토큰이 없습니다.'}, status=400)
            deleted, _ = EncryptedToken.objects.filter(username=user_name).delete()
            if deleted:
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': '토큰이 DB에 없습니다.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'POST 요청만 가능합니다.'}, status=405)