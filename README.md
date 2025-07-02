## server
기존 LMS 플랫폼을 리뉴얼하기 위한 Django 기반 백엔드입니다.

## 해결해야할 문제
1. 사용자 토큰을 어떻게 가져오느냐
    - OAuth 연동으로 로그인 (Developer API Key 발급 필요, 학교 IT 팀에 요청해야함)
    - 사용자가 직접 API 토큰을 발급받아 입력하는 방식 (토큰 생성 창을 띄워주면 됨)

OAuth 인증 플로우
1. 사용자가 로그인 클릭
2. Canvas LMS 로그인 및 권한 허용
3. Django가 access token을 받아 저장
4. 사용자는 로그인된 상태가 됨.