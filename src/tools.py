import fnmatch
import logging
import os
import subprocess
from langchain.tools import tool
from langchain_community.utilities import SQLDatabase
from .utils import get_safe_path, TARGET_ROOT

logger = logging.getLogger(__name__)

# 파일 읽기 도구
@tool
def read_file(file_path: str):
    """프로젝트 내의 파일 내용을 읽습니다. 파일 경로는 프로젝트 루트 상대 경로여야 합니다."""
    logger.info("read_file 호출됨: file_path=%s", file_path)
    try:
        safe_path = get_safe_path(file_path)
        with open(safe_path, "r", encoding="utf-8") as f:
            content = f.read()
        logger.info("read_file 성공: file_path=%s", file_path)
        return content
    except Exception as e:
        logger.warning("read_file 실패: file_path=%s, error=%s", file_path, e)
        return f"Error reading file: {str(e)}"

# 파일 쓰기/생성 도구
@tool
def write_file(file_path: str, content: str):
    """파일을 생성하거나 덮어씁니다. 코드를 작성할 때 사용하세요."""
    logger.info("write_file 호출됨: file_path=%s, content_length=%d", file_path, len(content))
    try:
        safe_path = get_safe_path(file_path)
        # 디렉토리가 있는 경우에만 생성
        dir_path = os.path.dirname(safe_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        with open(safe_path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info("write_file 성공: file_path=%s", file_path)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        logger.warning("write_file 실패: file_path=%s, error=%s", file_path, e)
        return f"Error writing file: {str(e)}"

# 파일 목록 조회 (탐색용)
@tool
def list_files(directory_path: str = ".", recursive: bool = False):
    """
    특정 디렉토리 내의 파일 목록을 조회합니다. 
    recursive=True로 설정하면 하위 디렉토리까지 모두 조회하지만, 
    node_modules나 .git 같은 거대 폴더는 자동으로 제외합니다.
    """
    logger.info("list_files 호출됨: directory_path=%s, recursive=%s", directory_path, recursive)
    try:
        safe_path = get_safe_path(directory_path)
        files = []
        
        # 무시할 디렉토리 목록
        IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', 'dist', 'build', '.idea', '.vscode'}
        
        if recursive:
            for root, dirs, filenames in os.walk(safe_path):
                # 무시할 디렉토리는 탐색에서 제외
                dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
                
                for filename in filenames:
                    rel_dir = os.path.relpath(root, safe_path)
                    if rel_dir == ".":
                        files.append(filename)
                    else:
                        files.append(os.path.join(rel_dir, filename))
        else:
            # 기존처럼 현재 디렉토리만 조회
            for root, dirs, filenames in os.walk(safe_path):
                for filename in filenames:
                    files.append(filename)
                break 

        # 결과가 너무 길면 잘라서 반환 (토큰 제한 방지)
        if len(files) > 100:
            return "\n".join(files[:100]) + f"\n... (Total {len(files)} files, truncated)"
            
        logger.info("list_files 성공: count=%d", len(files))
        return "\n".join(files)
    except Exception as e:
        logger.warning("list_files 실패: %s", e)
        return f"Error listing files: {str(e)}"

# 파일 검색 도구 (파일명 패턴 검색)
@tool
def find_files_by_name(pattern: str):
    """
    프로젝트 전체에서 특정 패턴(예: '*.tsx', '*Chat*', '*.css')을 가진 파일의 경로를 찾습니다.
    UI 파일이나 특정 로직이 담긴 파일을 찾을 때 유용합니다.
    """
    logger.info("find_files_by_name 호출됨: pattern=%s", pattern)
    try:
        found_files = []
        safe_root = get_safe_path(".")
        IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', 'dist', 'build'}

        for root, dirs, filenames in os.walk(safe_root):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            for filename in filenames:
                if fnmatch.fnmatch(filename, pattern):
                    full_path = os.path.join(root, filename)
                    rel_path = os.path.relpath(full_path, safe_root)
                    found_files.append(rel_path)
        
        logger.info("find_files_by_name 성공: count=%d", len(found_files))
        if not found_files:
            return "No files found matching the pattern."
        return "\n".join(found_files)
    except Exception as e:
        return f"Error finding files: {str(e)}"

# 테스트 실행 도구
@tool
def run_test(command: str):
    """npm test 또는 python 테스트 명령어를 실행합니다. 프로젝트 루트에서 실행됩니다."""
    logger.info("run_test 호출됨: command=%s", command)
    if not TARGET_ROOT:
        logger.warning("run_test 실패: TARGET_PROJECT_ROOT 미설정")
        return "Error: TARGET_PROJECT_ROOT 환경 변수가 설정되지 않았습니다."
    try:
        # 보안을 위해 rm 등의 위험한 명령어 필터링 로직 추가 권장
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=TARGET_ROOT, 
            capture_output=True, 
            text=True
        )
        logger.info("run_test 성공: command=%s, returncode=%d", command, result.returncode)
        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    except Exception as e:
        logger.warning("run_test 실패: command=%s, error=%s", command, e)
        return f"Error running test: {str(e)}"

# 데이터베이스 조회 도구
# DB 연결 설정 (환경 변수가 있을 때만 초기화)
db = None
database_url = os.getenv("DATABASE_URL")
if database_url:
    try:
        db = SQLDatabase.from_uri(database_url)
    except Exception as e:
        import sys
        print(f"Warning: Could not initialize database connection: {e}", file=sys.stderr)

@tool
def get_db_schema():
    """데이터베이스의 테이블 목록과 스키마 정보를 가져옵니다."""
    logger.info("get_db_schema 호출됨")
    if not db:
        logger.warning("get_db_schema 실패: DB 연결 없음")
        return "Error: DATABASE_URL 환경 변수가 설정되지 않았거나 데이터베이스 연결에 실패했습니다."
    try:
        schema = db.get_table_info()
        logger.info("get_db_schema 성공")
        return schema
    except Exception as e:
        logger.warning("get_db_schema 실패: error=%s", e)
        return f"Error getting schema: {str(e)}"

@tool
def run_sql_query(query: str):
    """SQL 쿼리를 실행하여 데이터를 조회합니다. SELECT 문만 허용하는 것을 권장합니다."""
    logger.info("run_sql_query 호출됨: query=%s", query)
    if not db:
        logger.warning("run_sql_query 실패: DB 연결 없음")
        return "Error: DATABASE_URL 환경 변수가 설정되지 않았거나 데이터베이스 연결에 실패했습니다."
    try:
        result = db.run(query)
        logger.info("run_sql_query 성공")
        return result
    except Exception as e:
        logger.warning("run_sql_query 실패: query=%s, error=%s", query, e)
        return f"SQL Error: {str(e)}"

# AI에게 전달할 도구 리스트
agent_tools = [read_file, write_file, list_files, run_test, get_db_schema, run_sql_query]
