from datetime import datetime, timedelta
import json
import re
from canvasapi import Canvas
from users.services import get_token_by_username
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import timezone

def get_d_day_str(due_dt) -> str:
    """
    D-Day 형식으로 반환한다. D-0일 경우 "D-0 (HH시간)"을 포함하여 반환한다.
    """
    try:
        now = datetime.now(timezone.utc)
        delta = due_dt - now
        if delta.days > 0:
            return f"D-{delta.days}"
        elif delta.days == 0:
            hours = delta.seconds // 3600
            return f"D-0 ({hours}시간)"
        else:
            return "마감됨"
    except Exception as e:
        print("파싱 실패: ", due_at, e)
        return "날짜 오류"

def extract_week_number(week_str) -> str:
    """
    "00주차" 형식으로 반환한다.
    """
    match = re.search(r'(\d+)\s*주차', week_str)
    if match:
        return f"{match.group(1)}주차"
    return None

# Create your views here.
@csrf_exempt
def upcoming(req):
    """
    주어진 user_name에 해당하는 토큰을 조회 및 활용하여 강의/과제/영상 정보를 추출
    """
    if req.method != 'POST':
        return JsonResponse({'error': 'POST 요청이 아닙니다.'}, status=405)
    
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
    
    # json 반환 리스트
    lecture_data = []
    module_week_map = {}

    # 강의 목록 조회
    courses_list = list(courses)
    filtered_courses = [course for course in courses_list if not getattr(course, "access_restricted_by_date", False)]

    # 수강 중인 과목 대상 반복
    for course in filtered_courses:
        course_name = getattr(course, "name", "이름없음")
        
        # 1. 모듈 정보 수집
        try:
            modules = list(course.get_modules())
            for m in modules:
                week_name = m.name
                try:
                    items = list(m.get_module_items())
                    for item in items:
                        if item.type == "Assignment":
                            module_week_map[item.content_id] = week_name
                except Exception:
                    continue
        except Exception:
            pass

        # 2. 과제 정보에 week 추가
        try:
            assignments = list(course.get_assignments())
            for a in assignments:
                if not hasattr(a, "due_at") or not a.due_at:
                    continue
                d_day_str = get_d_day_str(a.due_at_date)
                # 1. 모듈에서 주차 추출
                week_raw = module_week_map.get(a.id, None)
                week_clean = extract_week_number(week_raw) if week_raw else None
                # 2. 모듈에서 못 찾으면 과제명에서 주차 추출
                if not week_clean:
                    week_clean = extract_week_number(a.name)
                # 3. 둘 다 없으면 None
                lecture_data.append({
                    'type': '과제',
                    'course_name': course_name,
                    'week': week_clean,
                    'remaining_days': d_day_str
                })
        except Exception as e:
            continue
    return JsonResponse({'success': True, 'lecture_data': lecture_data})