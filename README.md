# AI Agent 개발 프로젝트

FastAPI와 LangChain 기반 AI 에이전트 서버입니다.  
채팅으로 요청을 보내면 에이전트가 파일 읽기/쓰기, 디렉터리 탐색, 테스트 실행, DB 조회 등 도구를 사용해 작업을 수행합니다.

---

## 파일 구성

```
web-dev-ai-agent/
├── src/
│   ├── __init__.py    # 패키지 초기화
│   ├── server.py      # FastAPI 앱, CORS, /api/chat 엔드포인트, LangChain 에이전트 연동
│   ├── tools.py       # 에이전트용 도구: 파일 읽기/쓰기, 목록·검색, 테스트 실행, DB 스키마·쿼리
│   └── utils.py       # 경로 검증(get_safe_path), TARGET_PROJECT_ROOT·.env 로드
├── check_packages.py  # 필수 패키지 확인 스크립트 (실행 전 의존성 검사)
├── requirements.txt  # Python 의존성 목록
├── setup_venv.sh     # 가상환경 생성 및 패키지 설치
├── start_server.sh   # 서버 백그라운드 실행 (로그: logs/server.log)
├── stop_server.sh    # 백그라운드 서버 중지
├── view_logs.sh      # 서버 로그 실시간 조회
└── README.md         # 이 문서
```

- **logs/** — 서버 실행 시 생성되는 로그·PID 파일 (`.gitignore` 대상)
- **venv/** — 가상환경 디렉터리 (`.gitignore` 대상)

---

## 프로젝트 기능 설명

| 구분 | 설명 |
|------|------|
| **서버** | FastAPI 앱, CORS 허용(CLIENT_ORIGIN), `POST /api/chat`로 대화 요청 처리. Next.js 등 클라이언트와 연동 가능. |
| **에이전트** | LangChain(GPT) 기반 풀스택 개발 에이전트. 대화 기록을 유지한 채 도구를 호출해 작업 수행. |
| **파일 도구** | `read_file`(파일 읽기), `write_file`(파일 생성/덮어쓰기), `list_files`(디렉터리 목록·재귀 탐색), `find_files_by_name`(패턴으로 파일 검색). 프로젝트 루트 밖 접근은 차단. |
| **실행 도구** | `run_test`: 프로젝트 루트에서 `npm test` 등 셸 명령 실행. (TARGET_PROJECT_ROOT 기준) |
| **DB 도구** | `DATABASE_URL` 설정 시 `get_db_schema`(테이블·스키마 조회), `run_sql_query`(SQL 실행). |
| **보안** | `utils.get_safe_path`로 경로가 TARGET_PROJECT_ROOT 내부인지 검사해 경로 조작 방지. |

환경 변수: `SERVER_HOST`, `SERVER_PORT`, `CLIENT_ORIGIN`, `TARGET_PROJECT_ROOT`, `DATABASE_URL`(선택), `.env` 로드.

---

## 설치

### 문제 해결

패키지 설치 시 권한 오류가 발생하는 경우, 아래 방법 중 하나를 사용하세요.

### 가상환경 사용 (권장)

```bash
# 스크립트 사용
bash setup_venv.sh
```

가상환경 활성화 후:

```bash
source venv/bin/activate   # macOS/Linux
```

### 설치 확인

```bash
python check_packages.py
```

모든 패키지가 설치되면 다음 명령어로 서버를 실행하세요:

```bash
python -m src.server
```

---

## 서버 실행

### 일반 실행

```bash
python -m src.server
```

### 백그라운드 실행 (콘솔 없이)

서버를 백그라운드에서 돌리고 로그만 따로 보려면:

```bash
./start_server.sh    # 백그라운드로 서버 시작 (로그: logs/server.log)
./view_logs.sh       # 로그 실시간 보기 (Ctrl+C 로 종료)
./stop_server.sh     # 서버 중지
```

---

## 환경 설정

`.env.example`을 참고하여 프로젝트 루트에 `.env` 파일을 만들고 필요한 환경 변수를 설정하세요.

---
