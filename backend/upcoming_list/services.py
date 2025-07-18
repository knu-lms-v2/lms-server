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

def is_video_file(filename):
    video_extensions = ('.mp4', '.mov', '.avi', '.wmv', '.mkv', '.flv', '.webm')
    return filename.lower().endswith(video_extensions)

def is_video_page(content):
    return (
        "<video" in content.lower() or
        "<iframe" in content.lower() or
        re.search(r'(youtube\.com|vimeo\.com|kaltura\.com|panopto\.com)', content, re.IGNORECASE)
    )

def save_lecture_data(lecture_data, user_name, upcoming_type, course_name, week_clean, due_at):
    data = {
        'type': upcoming_type,
        'course_name': course_name,
        'week': week_clean,
        'due_date': due_at
    }
    lecture_data.append(data)
    UpcomingData.objects.update_or_create(
        user_name=user_name,
        type=upcoming_type,
        course_name=course_name,
        week=week_clean,
        defaults={'due_date': due_at}
    )

def update_user_upcoming_list(user_name):
    lecture_data = []
    week_map = {}
    item_info = {}  # (type, content_id): (upcoming_type, due_at)

    courses = convert_user_name_to_token(user_name)
    if not courses:
        print("It is not courses...")
        return lecture_data

    filtered_courses = [course for course in courses if not getattr(course, "access_restricted_by_date", False)]

    for course in filtered_courses:
        course_name = getattr(course, "name", "이름없음")
        try:
            for m in course.get_modules():
                week_name = m.name
                for item in m.get_module_items():
                    key = (item.type, item.content_id)
                    week_map[key] = week_name

                    # 타입별로 upcoming_type, due_at 추출
                    if item.type == "Assignment":
                        upcoming_type = "과제"
                        due_at = getattr(item, "due_at", None)
                    elif item.type == "Quiz":
                        upcoming_type = "시험"
                        due_at = getattr(item, "due_at", None)
                    elif item.type == "ExternalTool":
                        upcoming_type = "영상"
                        due_at = getattr(item, "due_at", None)
                    elif item.type == "File":
                        filename = getattr(item, 'title', '')
                        if is_video_file(filename):
                            upcoming_type = "영상"
                            due_at = getattr(item, "due_at", None)
                        else:
                            continue
                    elif item.type == "Page":
                        content = getattr(item, "body", "")
                        if is_video_page(content):
                            upcoming_type = "영상"
                            due_at = getattr(item, "due_at", None)
                        else:
                            continue
                    else:
                        continue

                    item_info[key] = (upcoming_type, due_at)
        except Exception as e:
            print(f'error: {e}')
            continue

        # 한 번에 처리
        for key, (upcoming_type, due_at) in item_info.items():
            if not due_at or not is_due_within_7_days(due_at):
                continue
            week_clean = extract_week_number(week_map.get(key, ""))
            save_lecture_data(lecture_data, user_name, upcoming_type, course_name, week_clean, due_at)

    return lecture_data