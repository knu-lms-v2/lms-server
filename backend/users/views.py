from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

# Create your views here.
@csrf_exempt
def validate_token(req):
    if req.method == 'POST':
        try:
            pass
        except Exception as e:
            return JsonResponse({'valid': False, 'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'POST 요청만 허용됩니다.'}, status=405)