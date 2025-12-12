# multiple and langgraph stategraph client.py
# 루트 폴더에서 python client/multiple_langgraph_stategraph_client.py 으로 실행

# create_agent 는 내부 로직 관찰이나 중간 통제가 용이하지 않다.
# 반면 stategraph client 를 사용하면 에이전트가 도구를 호출하기 전에 사람의 승인을 받게 하거나, 
# 특정 조건에서만 도구를 실행하도록 흐름을 직접 설계할 수 있다.
# 해보자.
# 일단은, 기존 코드랑 동일한 기능을 수행하는 그래프를 만들고, 새로운 파이썬 파일에서 더 고도화해볼 예정이다!!

import asyncio
from dotenv import load_dotenv

# --- 1. 필수 라이브러리 임포트 ---
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
# LangGraph의 핵심 요소들:
# StateGraph: 그래프 정의, MessagesState: 대화 기록 관리, START: 시작점
from langgraph.graph import StateGraph, MessagesState, START
# Prebuilt: 미리 만들어진 도구 노드와 조건문 (이게 없으면 직접 다 짜야 함)
from langgraph.prebuilt import ToolNode, tools_condition


# 환경 변수(.env)에서 API KEY 로드
load_dotenv()

async def main():
    # --- 2. MCP 클라이언트 설정 (서버 연결 정보) ---
    # 여러 서버(Math, Weather)를 한꺼번에 관리하는 클라이언트입니다.
    client = MultiServerMCPClient(
        {
            "Math": {
                "command" : "python",
                # 경로 주의
                "args": ["server/math_server.py"],
                "transport": "stdio", # 로컬 프로세스로 실행하겠다. 보안이 중요하거나, 로직이 중요할 때.
            },
            "Weather": {
                # 8000번 포트에서 HTTP MCP 서버에 실행한 후 연결해야함.
                # `python weather_server.py` 등으로 미리 실행 필요
                "url": "http://localhost:8000/sse",
                "transport": "sse", # http sse 방식으로 연결
            },
        }
    )

    print("connecting to MCP servers...")

    # --- 3. 도구(Tools) 불러오기 ---
    # 각 서버에 접속해 "무슨 함수 쓸 수 있어?"라고 물어보고 가져오기    
    tools = await client.get_tools()

    # --- 4. LLM 모델 설정 ---
    model= ChatOpenAI(model="gpt-5.2", temperature=0)

    # --- 5. 노드(Node) 함수 정의 ---
    # 그래프의 각 정점(Node)에서 실행될 로직을 함수로 만들어야함.

    # [챗봇 노드]: 현재 대화 상태(state)를 받아 모델을 실행합니다.
    def call_model(state: MessagesState):
        # model.bind_tools(tools): 모델에게 "이 도구들을 사용할 수 있어"라고 알려줍니다.
        # invoke: 모델이 대화 기록을 보고 답변하거나, 도구 호출을 결정합니다.
        response = model.bind_tools(tools).invoke(state['messages'])
        # 결과를 다시 'messages' 상태에 추가하여 반환합니다.
        return {'messages': response}

    # --- 6. 그래프(Graph) 조립 ---
    # 여기서부터 에이전트의 워크플로우를 직접 설계할 수 있음.!!

    # 대화 기록(Messages)을 상태로 가지는 그래프 생성
    builder = StateGraph(MessagesState)

    # (1) 노드 등록: 'call_model'과 'tools' 노드를 그래프에 추가
    builder.add_node("call_model", call_model)
    builder.add_node("tools", ToolNode(tools))

    # (2) 시작점 연결: 그래프가 시작되면 무조건 'call_model'부터 실행해라.
    # 가장 중요한 시작점(Entrypoint) 정의!!
    # 그래프가 시작되면 무조건 'call_model' 노드로 가라고 지정.
    builder.add_edge(START, "call_model")

    # (3) 조건부 엣지(Conditional Edge) 
    # 모델이 도구를 호출하면 'tools'로, 아니면 종료(END)로 가라.
    builder.add_conditional_edges(
        "call_model",       # 출발 노드
        tools_condition,    # 조건 판단 함수
    )

    # (4) 순환 엣지:
    # 도구 실행 후 다시 모델 호출로 돌아가서 결과를 보고해라.
    builder.add_edge("tools", "call_model")

    # (5) 컴파일: 설계도를 실제 실행 가능한 객체로 변환
    graph = builder.compile()

    # --- 7. 실행 및 테스트 ---
    print("\n--- Math Query (Graph) ---")
    # ainvoke: 비동기로 그래프 실행
    math_response = await graph.ainvoke({"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]})
    print(f"Agent: {math_response['messages'][-1].content}")

    print("\n--- Weather Query (Graph) ---")
    weather_response = await graph.ainvoke({"messages": [{"role": "user", "content": "what is the weather in nyc?"}]})
    print(f"Agent: {weather_response['messages'][-1].content}")

if __name__ == "__main__":
    asyncio.run(main())