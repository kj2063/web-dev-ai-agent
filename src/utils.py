import os
from pathlib import Path
from dotenv import load_dotenv

# 프로젝트 루트에서 .env 로드 (src 폴더 기준 상위 디렉터리)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_PROJECT_ROOT / ".env")

TARGET_ROOT = os.getenv("TARGET_PROJECT_ROOT")
if not TARGET_ROOT:
    # 기본값: 이 패키지가 있는 프로젝트 루트
    TARGET_ROOT = str(_PROJECT_ROOT)

def get_safe_path(rel_path: str) -> str:
    """
    입력된 경로가 목표 프로젝트 루트 내부인지 확인하고 절대 경로를 반환합니다.
    경로 조작(../../etc/passwd) 공격을 방지합니다.
    """
    if not TARGET_ROOT:
        raise ValueError("TARGET_PROJECT_ROOT 환경 변수가 설정되지 않았습니다.")
    
    base = Path(TARGET_ROOT).resolve()
    target = (base / rel_path).resolve()
    
    # target 경로가 base 경로로 시작하지 않으면 에러 발생
    if not str(target).startswith(str(base)):
        raise ValueError(f"Access denied: Path {rel_path} is outside the project root.")
    
    return str(target)
