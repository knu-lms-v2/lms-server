from datetime import datetime, timedelta, timezone
import re
from canvasapi import Canvas
from users.services import get_token_by_username
from .models import UpcomingData

def convert_user_name_to_token(user_name):
    """
        user_name을 토큰으로 반환하여 데이터 추출하는 함수
    """
    # 토큰 조회
    try:
        token = get_token_by_username(user_name)
        if not token:
            print("It is not token...")
            return None
    except Exception as e:
        print(f"error: {e}")
        return None
       
    # Canvas API 연결
    try:
        API_URL = "https://knulms.kongju.ac.kr/"
        canvas = Canvas(API_URL, token)
        user = canvas.get_current_user()
        courses = user.get_courses()
    except Exception as e:
        print(f"error: {e}")
        return None
    
    return courses
    
def is_due_within_7_days(due_at) -> bool:
    """
        정해진 날짜 이내에 포함되어 있는 강의/과제/영상만 출력
    """
    now = datetime.now(timezone.utc)
    end = now + timedelta(days=7)
    return now <= due_at <= end

def extract_week_number(week_str) -> str:
    """
        "00주차" 형식으로 반환한다.
    """
    match = re.search(r'(\d+)\s*주', week_str)
    if match:
        return f"{match.group(1)}주차"
    return None

def get_week_from_maps(a, assignment_week_map):
    """
        딕셔너리의 값을 "00주차" 형식으로 바꾸기 위한 함수
    """
    week_raw = assignment_week_map.get(a.id)
    week_clean = extract_week_number(week_raw) if week_raw else None
    if not week_clean:
        week_clean = extract_week_number(a.name)
    return week_clean

def update_user_upcoming_list(user_name):
    """
        사용자의 강의/과제/영상의 마감일이 7일 이내에
        존재하면 DB에 저장하고 반환하는 함수
    """
    lecture_data = []
    assignment_week_map = {}
    exam_week_map = {}
    video_week_map = {}
    upcoming_type = ""

    courses = convert_user_name_to_token(user_name)
    if not courses:
        print("It is not courses...")
        return lecture_data
    
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
                due_at = getattr(a, "due_at_date", None)
                if not due_at:
                    continue

                if not is_due_within_7_days(due_at):
                    print("not exists due_date...")
                    # continue

                week_clean = get_week_from_maps(a, assignment_week_map)
                data = {
                    'type': upcoming_type,
                    'course_name': course_name,
                    'week': week_clean,
                    'due_date': due_at
                }
                lecture_data.append(data)

                # DB에 저장
                UpcomingData.objects.update_or_create(
                    user_name=user_name,
                    type=upcoming_type,
                    course_name=course_name,
                    week=week_clean,
                    defaults={
                        'due_date': due_at
                    }
                )
        except Exception as e:
            print(f"error: {e}")
            continue
    return lecture_data
    