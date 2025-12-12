# math_server.py
from mcp.server.fastmcp import FastMCP

# 이 MCP 서버의 이름 규정
# 클라이언트(LLM)가 여러 MCP 서버 중에서 이 서버를 식별할 때 사용함
mcp = FastMCP("Math")

# MCP 서버에 제공할 도구(tool) 정의
# 이 데코레이터는 1. 이 함수를 mcp tool로 등록하고, 2. LLM이 JSON Schema 기반으로 호출할 수 있도록 도와줌.
# how? 내부적으로 메타정보를 자동으로 생성하걸랑.
# { 
#   "name": "add",
#   "description": "Add two numbers",
#   "input_schema": {
#     "a": "int",
#     "b": "int"
#   },
#   "output": "int"
# }
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a+b

@mcp.tool()
def multiply(a:int, b:int) -> int:
    """Multiply two numbers"""
    return a*b 

if __name__ =="__main__":
    # `stdio`는 mcp 서버가 표준 입력/출력으로 통신한다는 의미.
    # http 서버 아니고, 웹 브라우저 아니고, LLM 프로세스와 파이프 기반 통신하겠다!!!
    mcp.run(transport="stdio")