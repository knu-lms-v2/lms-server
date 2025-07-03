from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from canvasapi import Canvas
from .services import get_user_token, save_user_token
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

            # 정상적인 user 정보일 경우
            return JsonResponse({'valid': True, 'user': {'id': user.id, 'name': user.name}})
        except Exception as e:
            return JsonResponse({'valid': False, 'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'POST 요청만 허용됩니다.'}, status=405)
    
def save_token_view(req):
    if req.method == 'POST':
        token = req.POST.get('token')
        save_user_token(req.user, token)
        return JsonResponse({'status': 'ok'})

def get_token_view(req):
    token = get_user_token(req.user)
    return JsonResponse({'token': token})