### LangChain MCP 어댑터란, 
MCP가 랭체인 및 랭그래프와 호환되도록 하는 경량 wrapper이다.
즉, mcp 도구를 langchain 도구로 변환함으로써, 
랭체인 및 렝그레프 에이전트에서 도구로서 로드할 수 있도록 구현해주는 도구이다.

### 소감
앞서, mcp와 관련하여 공부할 때, 한컴의 자료를 읽은 적이 있다.
그때, mcp 와 ai agent가 상호 소통하기 위해서, auth관련 문제나 데이터 형식 규약, 파라미터에 대한 준비를 해주는 mcp wrapper가 있다는 개념을 학습한 바가 있는데, 그것과 연관이 있을까 싶다.

### 기반 개념 정리
mcp 어댑터에 대해서 이해하기 위해서는 우선, mcp 계층에 대한 이해를 함양할 필요가 있다.

mcp는 다음 세 가지 원소들로 이루어져있다.
- mcp servers : They provide context, tools, and prompts to clients 
- mcp clients : They maintain 1:1 connections with servers, inside the host app
- app : such as claude desktop app, langgraph agent

### FastMCP 간단 정리
- mcp 서버를 간단하게 만들 수 있도록 도와주는 high-level의 래퍼이다.
- 거의 MCP계의 FastAPI



