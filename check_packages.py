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

if missing_packages:
    print()
    print("=" * 60)
    print("오류: 필요한 패키지가 설치되지 않았습니다!")
    print("=" * 60)
    print(f"누락된 패키지: {', '.join(missing_packages)}")
    print("\n[권장] 가상환경 사용 (권한 문제 해결):")
    print("  bash setup_venv.sh")
    print("  source venv/bin/activate")
    print("  ./start_server.sh")
    print("\n[대안 1] 직접 설치:")
    print(f"  pip install {' '.join(missing_packages)}")
    print("\n[대안 2] Conda 사용:")
    print("  conda install -c conda-forge uvicorn")
    print("  pip install langchain-openai langchain-community")
    print("\n자세한 내용은 README_SETUP.md를 참조하세요.")
    print("=" * 60)
    sys.exit(1)

print("\n모든 패키지가 설치되어 있습니다.")
sys.exit(0)
