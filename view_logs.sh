#!/usr/bin/env bash
# 서버 로그를 실시간으로 확인합니다. (Ctrl+C 로 종료)

cd "$(dirname "$0")"
LOG_FILE="logs/server.log"

if [ ! -f "$LOG_FILE" ]; then
  echo "로그 파일이 없습니다: $LOG_FILE"
  echo "먼저 ./start_server.sh 로 서버를 실행하세요."
  exit 1
fi

echo "로그 실시간 보기 (종료: Ctrl+C)"
echo "---"
tail -f "$LOG_FILE"
