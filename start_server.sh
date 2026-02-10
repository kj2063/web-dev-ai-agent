#!/usr/bin/env bash
# server.py(src)를 백그라운드에서 실행하고 로그를 남깁니다.
# 중지: ./stop_server.sh

set -e
cd "$(dirname "$0")"

LOG_DIR="logs"
LOG_FILE="$LOG_DIR/server.log"
PID_FILE="$LOG_DIR/server.pid"

# 이미 실행 중이면 종료
if [ -f "$PID_FILE" ]; then
  OLD_PID=$(cat "$PID_FILE")
  if kill -0 "$OLD_PID" 2>/dev/null; then
    echo "이미 서버가 실행 중입니다 (PID: $OLD_PID). 중지하려면 ./stop_server.sh"
    exit 1
  fi
  rm -f "$PID_FILE"
fi

mkdir -p "$LOG_DIR"

# 가상환경이 있으면 활성화
if [ -d "venv/bin" ]; then
  source venv/bin/activate
fi

# 서버 실행에 필요한 패키지 설치 여부 확인
if ! python check_packages.py; then
  echo "패키지 검사 실패. 위 메시지를 확인한 뒤 패키지를 설치한 후 다시 시도하세요."
  exit 1
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 서버 시작" >> "$LOG_FILE"
nohup python -m src.server >> "$LOG_FILE" 2>&1 &
SERVER_PID=$!
echo $SERVER_PID > "$PID_FILE"

# 서버가 정상 기동했는지 잠시 후 확인 (실패 시 에러 로그 출력)
sleep 2
if ! kill -0 "$SERVER_PID" 2>/dev/null; then
  rm -f "$PID_FILE"
  echo "서버 실행에 실패했습니다. 로그 마지막 내용:" >&2
  echo "---" >&2
  tail -n 50 "$LOG_FILE" >&2
  exit 1
fi

echo "서버를 백그라운드에서 시작했습니다 (PID: $SERVER_PID). 로그: $LOG_FILE"
