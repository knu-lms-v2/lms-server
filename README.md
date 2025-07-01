## server
기존 LMS 플랫폼을 리뉴얼하기 위한 Django 기반 백엔드입니다.

OAuth 인증 플로우
1. 사용자가 로그인 클릭
2. Canvas LMS 로그인 및 권한 허용
3. Django가 access token을 받아 저장
4. 사용자는 로그인된 상태가 됨.