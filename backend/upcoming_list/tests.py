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

        dt = datetime(2025, 7, 10, 14, 55, tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        end = now + timedelta(days=7)

        print(now)
        if now <= dt <= end:
            try:
                delta = dt - now
                hours = delta.seconds // 3600
                minutes = (delta.seconds % 3600) // 60
                if delta.days > 0:
                    print(f"D-{delta.day}")
                elif delta.days == 0:
                    print(f"D-0 ({hours}시간 {minutes}분전)")
                elif hours == 0:
                    print(f"D-0 ({minutes}분전)")
                else:
                    print("마감됨")
            except Exception as e:
                print(f"오류: {e}")

        # courses = user.get_courses()
        # for course in courses:
        #     name = getattr(course, "name", None)
        #     if name:
        #         assignments = course.get_assignments()
        #         assignments_list = list(assignments)
        #         for a in assignments_list:
        #             print(type(a.due_at_date))

            # print("과목명:", name)
            # modules = course.get_modules()
            # for module in modules:
            #     pass
            #     # print("  모듈명:", module.name)