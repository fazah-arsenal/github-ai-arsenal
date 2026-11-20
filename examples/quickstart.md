# Quickstart Examples for AI Agents

## Example 1: Find the Best Tool Before Writing Code
Prompt your AI (DeepSeek Harness / Claude / Cursor / Antigravity):
> "استخدم مهارة `github-ai-arsenal` عشان تلاقيلي أفضل مكتبة بايثون لعمل بوت تليجرام مع كشط مواقع، واعرضلي أوامر التثبيت."

The AI runs:
```bash
python scripts/gh_arsenal.py recommend "بوت تليجرام وكشط مواقع"
```

## Example 2: Search 18,000+ Tools Offline Without GitHub Rate Limits
```bash
python scripts/gh_arsenal.py mega --category security-pentest --query "scanner" --limit 10
python scripts/gh_arsenal.py mega --category mcp-servers --query "database" --limit 10
```

## Example 3: Generate Instant MCP Server Config
```bash
python scripts/gh_arsenal.py mcp-config playwright
python scripts/gh_arsenal.py mcp-config context7
```

## Example 4: Pull Any GitHub Tool Into Your Project Without `git`
```bash
python scripts/gh_arsenal.py inspect D4Vinci/Scrapling
python scripts/gh_arsenal.py pull D4Vinci/Scrapling --dest ./github_tools
```
