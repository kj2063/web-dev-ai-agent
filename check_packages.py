#!/usr/bin/env python
"""start_server.sh 실행 시 필요한 모든 라이브러리 설치 여부를 확인합니다."""
import sys

# server.py / requirements.txt 와 동기화된 필수 패키지
required_packages = {
    'fastapi': 'fastapi',
    'uvicorn': 'uvicorn',
    'pydantic': 'pydantic',
    'langchain_openai': 'langchain-openai',
    'langchain': 'langchain',
    'langchain_community': 'langchain-community',
    'dotenv': 'python-dotenv',
    'psycopg2': 'psycopg2-binary',
}

missing_packages = []
for module_name, package_name in required_packages.items():
    try:
        __import__(module_name)
        print(f"✓ {package_name} 설치됨")
    except ImportError:
        print(f"✗ {package_name} 누락됨")
        missing_packages.append(package_name)

print("\n모든 패키지가 설치되어 있습니다.")
sys.exit(0)
