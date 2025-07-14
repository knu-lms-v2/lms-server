from datetime import timezone
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from upcoming_list.services import convert_user_name_to_token, get_d_day_str, get_week_from_maps
from .models import UpcomingData

# Create your views here.
@csrf_exempt
def upcoming(req):
    """
    주어진 user_name에 해당하는 토큰을 조회 및 활용하여 강의/과제/영상 정보를 추출
    """
    if req.method != 'POST':
        return JsonResponse({'error': 'POST 요청이 아닙니다.'}, status=405)
    
    # user_name -> token -> canvas api 연결하여 courses 반환
    courses = convert_user_name_to_token(req)
    if not courses:
        return JsonResponse({'success': False, 'error': '토큰 또는 강의 정보 없음'}, status=400)
    
    # json 반환 리스트
    lecture_data = []

    # 강의, 영상, 시험의 "id: week" 값
    assignment_week_map = {}
    exam_week_map = {}
    video_week_map = {}

    upcoming_type = ""

    # 강의 목록 조회
    courses_list = list(courses)
    filtered_courses = [course for course in courses_list if not getattr(course, "access_restricted_by_date", False)]

    # 수강 중인 과목 대상 반복
    for course in filtered_courses:
        course_name = getattr(course, "name", "이름없음")
        
        # 1. 모듈 정보 수집
        try:
            for m in course.get_modules():
                week_name = m.name # 주차학습의 1주차, 2주차, ...
                for item in m.get_module_items(): # 주차학습 1주차의 내용들...
                    if item.type == "Assignment":
                        upcoming_type = "과제"
                        assignment_week_map[item.content_id] = week_name
                    elif item.type == "Quiz":
                        upcoming_type = "시험"
                        exam_week_map[item.content_id] = week_name
                    elif item.type == "File":
                        upcoming_type = "영상"
                        video_week_map[item.content_id] = week_name
        except Exception:
            continue

        # 2. 과제 정보에 week 추가
        try:
            for a in course.get_assignments():
                if not getattr(a, "due_at", None):
                    continue

                # D-day 반환
                d_day_str = get_d_day_str(a.due_at_date)
                if d_day_str == "마감됨":
                    continue

                week_clean = get_week_from_maps(a, assignment_week_map)
                data = {
                    'type': upcoming_type,
                    'course_name': course_name,
                    'week': week_clean,
                    'remaining_days': d_day_str
                }
                lecture_data.append(data)

                # DB에 저장
                UpcomingData.objects.create(
                    user_name=req.POST.get('user_name', ''),
                    type=upcoming_type,
                    course_name=course_name,
                    week=week_clean,
                    remaining_days=d_day_str
                )

        except Exception as e:
            print(f"error: {e}")
            continue
    return JsonResponse({'success': True, 'lecture_data': lecture_data})

@require_GET
def get_upcoming_data(req):
    user_name = req.GET.get('user_name', '')
    data = UpcomingData.objects.filter(user_name=user_name).order_by('-created_at')
    data.update(last_accessed=timezone.now())
    result = [
        {
            'type': d.type,
            'course_name': d.course_name,
            'week': d.week,
            'remaining_days': d.remaining_days,
            'last_accessed': d.last_accessed
        }
        for d in data
    ]
    return JsonResponse({'succress': True, 'lecture_data': result})