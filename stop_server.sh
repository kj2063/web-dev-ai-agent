#!/usr/bin/env bash
# start_server.sh 로 띄운 서버를 중지합니다.

cd "$(dirname "$0")"
PID_FILE="logs/server.pid"

if [ ! -f "$PID_FILE" ]; then
  echo "실행 중인 서버 정보가 없습니다. (logs/server.pid 없음)"
  exit 0
fi

PID=$(cat "$PID_FILE")
if kill -0 "$PID" 2>/dev/null; then
  kill "$PID"
  echo "서버를 중지했습니다 (PID: $PID)"
else
  echo "해당 PID($PID) 프로세스가 이미 없습니다."
fi
rm -f "$PID_FILE"
