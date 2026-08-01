from langchain.agents import create_agent
from langchain_core.tools import tool
from fastapi import FastAPI
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="强尼银手")

model = ChatOpenAI(
    model=os.getenv("MODEL_NAME"),
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    temperature=0.3,
    profile={"max_input_tokens":128000}
)


@tool
async def get_weather(city: str) -> str:
    """查询指定城市的天气。当用户询问某城市天气、气温、是否下雨时调用。"""
    return f"夜之城{city}是晴天"


tools = [get_weather]

graph = create_agent(
    model=model,
    tools=tools,
    system_prompt="你是一个智能聊天助手，你需要以赛博朋克2077里强尼银手的语气与用户说话",
    checkpointer=InMemorySaver(),
    middleware=[
        SummarizationMiddleware(
            model=model,
            trigger=("tokens", 3000),
            keep=("messages", 2),
            summary_prompt="对历史消息摘要，消息列表如下\n{messages}"
        )
    ],
)


class ChatRequest(BaseModel):
    question: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    answer: str
    status: str


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    config = {"configurable": {"thread_id": request.session_id}}
    try:
        result = await graph.ainvoke(
            {"messages": [{"role": "user", "content": request.question}]},
            config=config,
        )
        answer = result["messages"][-1].content
        return ChatResponse(answer=answer, status="success")
    except Exception as e:
        return ChatResponse(answer=str(e), status="error")


@app.get("/health")
async def health():
    return {"status": "healthy"}


# uvicorn chief:app --reload
