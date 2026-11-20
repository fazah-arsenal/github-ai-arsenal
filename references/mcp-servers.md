# Top GitHub MCP Servers Quick Reference

Use these Model Context Protocol (MCP) server configurations whenever the user wants to connect their AI agent (DeepSeek Harness, Claude Code, Cursor, Antigravity, Codex) to external GitHub tools.

## 1. GitHub Official MCP (`github/github-mcp-server`)
```json
{
  "mcpServers": {
    "github": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR_GH_TOKEN>"
      }
    }
  }
}
```

## 2. Context7 Up-to-Date Library Docs (`upstash/context7`)
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

## 3. Playwright Browser Automation (`microsoft/playwright-mcp`)
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"]
    }
  }
}
```

## 4. Sequential Thinking & Memory (`modelcontextprotocol/servers`)
```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"]
    }
  }
}
```

## 5. Build a Custom Python MCP Server (`jlowin/fastmcp`)
```python
from fastmcp import FastMCP

mcp = FastMCP("custom-toolkit")

@mcp.tool()
def ping(host: str) -> str:
    """Example custom tool exposed over MCP."""
    return f"Checked {host}"

if __name__ == "__main__":
    mcp.run()
```
