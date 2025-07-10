from datetime import datetime, timedelta, timezone
import json
import re
from canvasapi import Canvas
from django.http import JsonResponse
from users.services import get_token_by_username

def convert_user_name_to_token(req):
    # user_name 가져오기
    try:
        data = json.loads(req.body)
        user_name = data.get('user_name')
        if not user_name:
            return JsonResponse({'success': False, 'error': 'user_name이 없습니다.'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'요청 파싱 오류: {str(e)}'}, status=400)

    # 토큰 조회
    try:
        token = get_token_by_username(user_name)
        if not token:
            return JsonResponse({'success': False, 'error': '토큰이 없습니다.'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'토큰 조회 오류: {str(e)}'}, status=400)
       
    # Canvas API 연결
    try:
        API_URL = "https://knulms.kongju.ac.kr/"
        canvas = Canvas(API_URL, token)
        user = canvas.get_current_user()
        courses = user.get_courses()
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Canvas API 오류: {str(e)}'}, status=400)
    
    return courses
    
def get_d_day_str(due_dt) -> str:
    """
    D-Day 형식으로 반환한다. D-0일 경우 "D-0 (HH시간)"을 포함하여 반환한다.
    """
    now = datetime.now(timezone.utc)
    end = now + timedelta(days=7)

    if now <= due_dt <= end:
        try:
            delta = due_dt - now
            hours = delta.seconds // 3600
            minutes = (delta.seconds % 3600) // 60
            if delta.days > 0:
                return f"D-{delta.day}"
            elif delta.days == 0:
                return f"D-0 ({hours}시간 {minutes}분전)"
            elif hours == 0:
                return f"D-0 ({minutes}분전)"
            else:
                return "마감됨"
        except Exception as e:
            print(f"오류: {e}")

def extract_week_number(week_str) -> str:
    """
    "00주차" 형식으로 반환한다.
    """
    match = re.search(r'(\d+)\s*주', week_str)
    if match:
        return f"{match.group(1)}주차"
    return None