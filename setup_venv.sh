#!/bin/bash

# 가상환경을 만들고 패키지를 설치하는 스크립트

echo "가상환경을 생성합니다..."
python -m venv venv

echo "가상환경을 활성화합니다..."
source venv/bin/activate

echo "pip를 업그레이드합니다..."
pip install --upgrade pip

echo "필요한 패키지를 설치합니다 (requirements.txt)..."
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

echo ""
echo "설치가 완료되었습니다!"
echo ""
echo "가상환경을 활성화하려면 다음 명령어를 실행하세요:"
echo "  source venv/bin/activate"
echo ""
echo "그 다음 AI 에이전트 서버를 실행하세요:"
echo "  python -m src.server"
