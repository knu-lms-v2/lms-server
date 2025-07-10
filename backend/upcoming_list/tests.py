from datetime import datetime, timedelta, timezone
from django.test import TestCase
from canvasapi import Canvas
from pprint import pprint

import pytz

class CanvasApiTest(TestCase):
    def test_canvasapi_structure(self):
        API_URL = "https://knulms.kongju.ac.kr/"
        API_KEY = "uvvHRNOilQjXYsk7buRNhKZBkmuzfYciiKsaL4YNq5tif97vioWwEUnZXrQ5AWmf"

        canvas = Canvas(API_URL, API_KEY)
        user = canvas.get_current_user()
        print("유저 정보:", user)

        # json 반환 리스트
        lecture_data = []
        module_week_map = {}

        # 강의 목록 조회
        courses = user.get_courses()
        courses_list = list(courses)
        filtered_courses = [course for course in courses_list if not getattr(course, "access_restricted_by_date", False)]
        for course in filtered_courses:
            course_name = getattr(course, "name", "이름없음")
            print(course_name)
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