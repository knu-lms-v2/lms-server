from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from upcoming_list.services import convert_user_name_to_token, get_d_day_str, extract_week_number

# Create your views here.
@csrf_exempt
def upcoming(req):
    """
    주어진 user_name에 해당하는 토큰을 조회 및 활용하여 강의/과제/영상 정보를 추출
    """
    if req.method != 'POST':
        return JsonResponse({'error': 'POST 요청이 아닙니다.'}, status=405)
    
    # 토큰 반환
    courses = convert_user_name_to_token(req)

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
                week_clean = extract_week_number(week_raw)
                
                # 2. 모듈에서 못 찾으면 과제명에서 주차 추출
                if not week_clean:
                    print(a.name)
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