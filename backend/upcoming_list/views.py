import json
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UpcomingData
from .services import update_user_upcoming_list


# Create your views here.
@csrf_exempt
def set_upcoming_data(req):
    """
    - 장기 미접속자(7일 이상)의 로그인 시, 띄울 데이터 정보 갱신
    - 주어진 user_name에 해당하는 토큰을 조회 및 활용하여 강의/과제/영상 정보를 추출
    """
    if req.method == 'POST':
        try:
            json_data = json.loads(req.body)
            user_name = json_data.get('user_name', '')
            lecture_data = update_user_upcoming_list(user_name)
            return JsonResponse({'success': True, 'lecture_data': lecture_data})
        except Exception as e:
            print(f'error: {e}')
    else:
        return JsonResponse({'error': 'POST 요청이 아닙니다.'}, status=405)

@require_GET
def get_upcoming_data(req):
    """
    - 최근 접속자(7일 이내)의 경우, 바로 DB에서 정보를 긁어와 프론트로 전달
    """
    if req.method == "GET":
        try:
            json_data = json.loads(req.body)
            user_name = json_data.get('user_name', '')
            data = UpcomingData.objects.filter(user_name=user_name).order_by('-created_at')
            result = [
                {
                    'type': d.type,
                    'course_name': d.course_name,
                    'week': d.week,
                    'remaining_days': d.remaining_days
                }
                for d in data
            ]
        except Exception as e:
            print(f"error: {e}")
    return JsonResponse({'success': True, 'lecture_data': result})