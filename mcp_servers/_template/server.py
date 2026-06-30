from mcp.server import Server
from mcp.server.stdio import stdio_server
import asyncio


app = Server("{tool_name}-mcp")


@app.tool()
async def primary_function(input_text: str) -> str:
    """ツールの主要機能の説明。"""
    raise NotImplementedError("Implement this MCP tool.")


if __name__ == "__main__":
    asyncio.run(stdio_server(app))
