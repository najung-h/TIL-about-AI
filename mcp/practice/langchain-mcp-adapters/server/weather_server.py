from typing import List
from mcp.server.fastmcp import FastMCP

# "Weather"라는 이름으로 MCP 서버 생성
mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get weather for location."""
    return f"It's sunny in New York!"  # 여기에 실제 날씨 API 호출 로직을 넣을 수 있음 # 현재는 더미데이터

if __name__ == "__main__":
    # HTTP 방식으로 실행 (기본 포트 8000 사용)
    # 공식 문서에는 http 로 나와있었지만, 이제는 sse로 해야 langchain-mcp-adapters와 호환됨.
    mcp.run(transport="sse")

# `python weather_server.py` 입력해서 서버 실행