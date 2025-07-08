from datetime import timedelta, timezone
from django.http import JsonResponse

# Create your views here.
def upcoming(req):
    if req.method == 'GET':
        now = timezone.now()
        end = now + timedelta(days=7)

        # DB 필터링 부분

        
    else:
        return JsonResponse()