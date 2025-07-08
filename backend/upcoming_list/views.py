from datetime import timedelta
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

    now = timezone.now()
    end = now + timedelta(days=7)
    deadlines = []

    for course in courses:
        print(dir(course))
        # 과제 목록
        for assignment in course.get_assignments():
            print("  - Assignment:", assignment.name, assignment.due_at)
        # 퀴즈 목록
        for quiz in course.get_quizzes():
            print("  - Quiz:", quiz.title, quiz.due_at)
        # 모듈(강의자료) 목록
        for module in course.get_modules():
            print("  - Module:", module.name)