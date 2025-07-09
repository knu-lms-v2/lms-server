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
    
    # json 반환 리스트
    lecture_data = []

    # 강의 목록 조회
    courses_list = list(courses)
    filtered_courses = [course for course in courses_list if not getattr(course, "access_restricted_by_date", False)]

    for course in filtered_courses:
        course_name = getattr(course, "name", "이름없음")
        
        # 과제 정보
        try:
            assignments = list(course.get_assignments())
            for a in course.get_assignments():
                if not hasattr(a, "due_at") or not a.due_at:
                    continue
                lecture_data.append({
                    'type': 'assignment',
                    'course_name': course_name,
                    'title': a.name,
                    'due_at': a.due_at
                })
        except Exception as e:
            continue

        # 모듈(영상) 정보
        # try:
        #     modules = list(course.get_modules())
        #     for m in modules:
        #         lecture_data.append({
        #             'type': 'module',
        #             'course_name': course_name,
        #             'title': m.name,
        #             'completed_at': getattr(m, "completed_at", None)
        #         })
        # except Exception as e:
        #     continue
    return JsonResponse({'success': True, 'lecture_data': lecture_data})