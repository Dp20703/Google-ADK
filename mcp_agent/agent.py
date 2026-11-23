from pathlib import Path
from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

folder = Path(__file__).parent.joinpath("files").resolve()
folder.mkdir(exist_ok=True)

root_agent = Agent(
    model="gemini-3.6-flash",
    name="filesystem_agent",
    description="A helpful assistant that manages local files.",
    instruction=f"Help users manage files in {folder}. Always use absolute paths.",
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx",
                    args=["-y", "@modelcontextprotocol/server-filesystem", str(folder)],
                ),
                timeout=30,
            ),
        )
    ],
)
