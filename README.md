# 사용 방법
1. `example.env` 파일명 `.env`로 변경
2. `.env` 파일 빈칸 기입
   1. `OPEN_API_KEY` : 공공 데이터포털 API KEY 입력
   2. `EXTERNAL_PORT` : 사용할 포트 번호 입력
3. FastAPI 서버 실행
   1. ❗처음 실행 시 `venv` 를 통해 가상 환경에서 `requirements.txt` 읽어서 외부 라이브러리 설치하기
   2. Window의 경우 start.ps1 실행
   3. Linux 환경(MacOS)의 경우 start.sh 실행
4. http://localhost:{EXTERNAL_PORT}/docs 에서 API 실행 가능

# 수집 정보
## 박물관 정보
### 활용 API

**1. 한국관광공사_국문 관광정보 서비스_GW**
- 국문 관광 정보 동기화 목록 조회
- 공통 정보 조회
- 소개 정보 조회회


### 필요 데이터
- [x] 명칭
- [x] 소개글
- [x] 대표 이미지
- [x] 운영 시간
- [x] 주소
## 유적지 정보


## 민속촌 정보