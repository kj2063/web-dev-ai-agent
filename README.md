# AI Agent 개발 프로젝트

FastAPI와 LangChain 기반 AI 에이전트 서버입니다.

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
