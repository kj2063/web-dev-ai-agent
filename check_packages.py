#!/usr/bin/env python
import sys

packages_to_check = {
    'uvicorn': 'uvicorn',
    'langchain_openai': 'langchain-openai',
    'langchain_community': 'langchain-community',
}

missing = []
for module, package in packages_to_check.items():
    try:
        __import__(module)
        print(f"✓ {package} 설치됨")
    except ImportError as e:
        print(f"✗ {package} 누락됨")
        missing.append(package)

if missing:
    print(f"\n누락된 패키지: {', '.join(missing)}")
    sys.exit(1)
else:
    print("\n모든 패키지가 설치되어 있습니다!")
