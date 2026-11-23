from pathlib import Path
from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import (
    StdioConnectionParams,
    StreamableHTTPConnectionParams,
)
from mcp import StdioServerParameters
from dotenv import load_dotenv
import os

load_dotenv()

# load github token
github_token = os.getenv("GITHUB_TOKEN")
if not github_token:
    raise ValueError("Add GITHUB_TOKEN to your .env file")

folder = Path(__file__).parent.joinpath("files").resolve()
folder.mkdir(exist_ok=True)

root_agent = Agent(
    model="gemini-3.6-flash",
    name="filesystem_and_github_agent",
    description="A helpful assistant that manages local files and github.",
    instruction=f"""You have access to filesystem and Github MCP Servers.
Use their tools to manage local files and handle Github workflows.
Local files are located in {folder}. Always use absolute paths for filesystem operations.""",
    tools=[
        # Read files from the local machine.
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx",
                    args=[
                        "-y",
                        "@modelcontextprotocol/server-filesystem",
                        str(folder),
                    ],
                ),
                timeout=30,
            ),
        ),
        # Github MCP Server
        McpToolset(
            connection_params=StreamableHTTPConnectionParams(
                url="https://api.githubcopilot.com/mcp/",
                headers={"Authorization": f"Bearer {github_token}"},
            )
        ),
    ],
)
