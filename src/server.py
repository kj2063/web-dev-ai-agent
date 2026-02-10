import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# 프로젝트 루트에서 .env 로드
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_PROJECT_ROOT / ".env")

# 로그는 stdout/stderr로만 출력. 파일 저장은 start_server.sh 리다이렉트로 처리
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("server")

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# .env에서 서버·클라이언트 주소 로드
SERVER_HOST = os.getenv("SERVER_HOST", "localhost")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))
CLIENT_ORIGIN = os.getenv("CLIENT_ORIGIN", "http://localhost:3000")

# LangChain 관련 임포트
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# 우리가 만든 도구 임포트
from .tools import agent_tools

app = FastAPI()

# 1. CORS 설정 (요청 하는 클라이언트 출처 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[CLIENT_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. 데이터 모델 정의 (Next.js의 ChatRequest 타입과 일치)
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    conversationHistory: List[Message]

# 3. LangChain 에이전트 초기화
llm = ChatOpenAI(model="gpt-5.2", temperature=0) # gpt-5.2 사용

system_prompt = (
    "당신은 유능한 풀스택 개발자 AI 에이전트입니다. "
    "주어진 도구(파일시스템, DB, 터미널)를 사용하여 사용자의 요청을 해결하세요. "
    "코드를 수정할 때는 먼저 파일을 읽어서 내용을 확인한 뒤 수정하세요. "
    "DB 질문이 들어오면 스키마를 먼저 확인하세요."
)

# 에이전트 생성 (최신 LangChain API 사용)
agent = create_agent(llm, tools=agent_tools, system_prompt=system_prompt)

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # Next.js의 대화 기록을 LangChain 포맷으로 변환
        history_messages = []
        for msg in request.conversationHistory:
            if msg.role == 'user':
                history_messages.append(HumanMessage(content=msg.content))
            elif msg.role == 'assistant':
                history_messages.append(AIMessage(content=msg.content))
        
        # 에이전트 실행 (최신 LangChain API)
        # create_agent는 LangGraph를 반환하므로 invoke 메서드를 사용
        config = {"configurable": {"thread_id": "1"}}
        
        # 대화 기록을 포함하여 실행
        if history_messages:
            # 대화 기록을 컨텍스트로 전달
            result = await agent.ainvoke(
                {"messages": history_messages + [HumanMessage(content=request.message)]},
                config=config
            )
        else:
            result = await agent.ainvoke(
                {"messages": [HumanMessage(content=request.message)]},
                config=config
            )
        
        # 응답에서 마지막 메시지 추출
        if isinstance(result, dict) and "messages" in result:
            last_message = result["messages"][-1]
            if hasattr(last_message, "content"):
                return {"response": last_message.content}
            else:
                return {"response": str(last_message)}
        else:
            return {"response": str(result)}

    except Exception as e:
        logger.exception("Error processing request: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.middleware("http")
async def log_requests(request: Request, call_next):
    body = await request.body()
    if body:
        logger.debug("Request Body: %s", body.decode("utf-8"))
    response = await call_next(request)
    logger.debug("Response Status: %s", response.status_code)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.server:app", host=SERVER_HOST, port=SERVER_PORT, reload=False, log_level="debug")
