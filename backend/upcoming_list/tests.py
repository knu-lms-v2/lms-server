from canvasapi import Canvas
import pprint

API_URL = "https://knulms.kongju.ac.kr/"
API_KEY = "uvvHRNOilQjXYsk7buRNhKZBkmuzfYciiKsaL4YNq5tif97vioWwEUnZXrQ5AWmf"

canvas = Canvas(API_URL, API_KEY)

# 1. 내 강의 전체 목록 가져오기
user = canvas.get_current_user()
courses = user.get_courses()

# 2. 강의명 "소프트웨어공학"인 강의 찾기
target_course = None
# for course in courses:
course = courses[0]
for i in course.get_assignments():
    print(dir(i))
    # if course.name == "소프트웨어공학 03분반":
    #     target_course = course
    #     break

if target_course:
    # 3. 강의의 모든 정보 출력
    print(target_course.__dict__)
else:
    print("소프트웨어공학 강의를 찾을 수 없습니다.")