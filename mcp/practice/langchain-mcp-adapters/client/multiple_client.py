# 루트 폴더에서 python client/multiple_client.py 으로 실행

# Multiple MCP Servers
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

# env 파일에서 OPENAI_API_KEY 읽기
from dotenv import load_dotenv
load_dotenv()

async def main():
    # 1. MultiServerMCPClient 설정
    client = MultiServerMCPClient(
        {
            "Math": {
                "command" : "python",
                # 경로 주의
                "args": ["server/math_server.py"],
                "transport": "stdio",
            },
            "Weather": {
                # 8000번 포트에서 HTTP MCP 서버에 실행한 후 연결해야함.
                # `weather_server.py`
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            },
        }
    )

    # 2. 도구 로드 및 에이전트 실행
    
    print("connecting to MCP servers...")
    tools = await client.get_tools()

    # LLM 설정 (예: OpenAI GPT-5.2)
    llm = ChatOpenAI(model="gpt-5.2", temperature=0)

    # Langraph 에이전트 생성
    agent = create_agent(llm, tools)

    # math 도구 테스트
    print("\n--- Testing Math Tool ---")
    math_response = await agent.ainvoke({"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]})
    # 응답 파싱용
    print(f"Agent: {math_response['messages'][-1].content}")
    # mcp 도구 호출 관찰용
    print(math_response['messages'])

    # weather 도구 테스트
    print("\n--- Testing Weather Tool ---")
    weather_response = await agent.ainvoke({"messages": [{"role": "user", "content": "what is the weather in nyc?"}]})
    # 응답 파싱용
    print(f"Agent: {weather_response['messages'][-1].content}")
    # 관찰용
    # print(weather_response['messages'][-1])

if __name__ == "__main__":
    asyncio.run(main())