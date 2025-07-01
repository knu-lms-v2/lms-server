# 현재 lms에 접속된 계정의 강의 정보를 가져오는 코드

import canvasapi

API_URL = "https://knulms.kongju.ac.kr/"
TOKEN = ""

canvas = canvasapi.Canvas(API_URL, TOKEN)

for course in canvas.get_courses():
    try:
        print(course)
    except AttributeError:
        pass
