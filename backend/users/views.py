from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from canvasapi import Canvas
from .services import save_user_token
from .utils import encrypt_token
from .models import EncryptedToken
import json

# Create your views here.
@csrf_exempt
def validate_token(req):
    if req.method == 'POST':
        try:
            data = json.loads(req.body)
            token = data.get('token')
            if not token:
                return JsonResponse({'valid': False, 'error': '토큰이 없습니다.'}, status=400)
            
            API_URL = "https://knulms.kongju.ac.kr/"
            canvas = Canvas(API_URL, token)
            user = canvas.get_current_user() # 유효성 검사

            save_user_token(token)

            # 정상적인 user 정보일 경우
            return JsonResponse({'userName': user.name})
        except Exception as e:
            print(f"Exception: {e}")
            return JsonResponse({'valid': False, 'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'POST 요청만 허용됩니다.'}, status=405)
    
@csrf_exempt
def logout(req):
    if req.method == "POST":
        try:
            data = json.loads(req.body)
            token = data.get('token')
            if not token:
                print(token)
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