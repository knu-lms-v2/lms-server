from datetime import datetime, timezone
from django.test import TestCase
from canvasapi import Canvas
from pprint import pprint

class CanvasApiTest(TestCase):
    def test_canvasapi_structure(self):
        API_URL = "https://knulms.kongju.ac.kr/"
        API_KEY = "uvvHRNOilQjXYsk7buRNhKZBkmuzfYciiKsaL4YNq5tif97vioWwEUnZXrQ5AWmf"

        canvas = Canvas(API_URL, API_KEY)
        user = canvas.get_current_user()
        print("유저 정보:", user)

        dt = datetime(2025, 7, 15, 10, 30, tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)

        print(dt-now)
        # courses = user.get_courses()
        # for course in courses:
        #     name = getattr(course, "name", None)
        #     if name:
        #         assignments = course.get_assignments()
        #         assignments_list = list(assignments)
        #         for a in assignments_list:
        #             print(f"a.due_at_date: {a.due_at_date}")
        #             now = datetime.now(timezone.utc)
        #             print(a.due_at_date - now)

            # print("과목명:", course.name)
            # modules = course.get_modules()
            # for module in modules:
            #     print("  모듈명:", module.name)