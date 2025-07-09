from datetime import datetime, timedelta
import json
import re
from canvasapi import Canvas
from users.services import get_token_by_username
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

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

    # 최대 7일까지의 날짜 필터링 설정
    now = timezone.now()
    end = now + timedelta(days=7)
    
    lecture_data = []
    """
    {
        'course_name': course.name,
        'title': assignment.name,
        'remaining_days': assignment.due_at, 남은 D-day (D-0이면 HH시간 출력)
    }
    """

    # 강의 목록 조회
    courses_list = list(courses)
    filtered_courses = [course for course in courses_list if not getattr(course, "access_restricted_by_date", False)]

    for course in filtered_courses:
        print(vars(course))
        course_name = getattr(course, "name", "이름없음")
        
        # 과제 정보
        for a in course.get_assignments():
            title = a.name
            if not a.due_at:
                print(f"title: {title}")
                continue
            try:
                due_dt = datetime.strptime(a.due_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            except Exception:
                continue

            start_date = datetime(2025, 6, 1, 0, 0, 0, tzinfo=timezone.utc)
            end_date = datetime(2025, 6, 30, 23, 59, 59, tzinfo=timezone.utc)

            if start_date <= due_dt <= end_date:
                delta = due_dt - now
                if delta.days > 0:
                    remaining_days = f"D-{delta.days}"
                elif delta.days == 0:
                    hours = delta.seconds // 3600
                    remaining_days = f"D-0 ({hours}시간)"
                else:
                    continue
            


            lecture_data.append({
                'course_name': course_name,
                'title': title,
                'remaining_days': remaining_days
            })

    return JsonResponse({'success': True, 'lecture_data': lecture_data})