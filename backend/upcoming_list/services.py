from datetime import datetime, timedelta
from django.utils import timezone
import json
import re
from canvasapi import Canvas
from users.services import get_token_by_username
from .models import UpcomingData

def convert_user_name_to_token(user_name):
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
                return f"D-{delta.days}"
            elif delta.days == 0 and hours == 0:
                return f"{minutes}분전"
            elif delta.days == 0:
                return f"{hours}시간전"

        except Exception as e:
            print(f"error: {e}")
    else:
        return "마감됨"

def extract_week_number(week_str) -> str:
    """
    "00주차" 형식으로 반환한다.
    """
    match = re.search(r'(\d+)\s*주', week_str)
    if match:
        return f"{match.group(1)}주차"
    return None

def get_week_from_maps(a, assignment_week_map):
    week_raw = assignment_week_map.get(a.id)
    week_clean = extract_week_number(week_raw) if week_raw else None
    if not week_clean:
        week_clean = extract_week_number(a.name)
    return week_clean

def update_user_upcoming_list(user_name):
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
                UpcomingData.objects.update_or_create(
                    user_name=user_name,
                    type=upcoming_type,
                    course_name=course_name,
                    week=week_clean,
                    defaults={
                        'remaining_days':d_day_str
                    }
                )
        except Exception:
            continue
    return lecture_data
    