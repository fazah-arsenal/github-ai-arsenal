# ⚡ FAZAH AI Arsenal v4.0 — Quickstart Examples for AI Agents
> Official Repository: [github.com/fazah-arsenal/github-ai-arsenal](https://github.com/fazah-arsenal/github-ai-arsenal)  
> Developer: **FAZAH** | Telegram: [@testtttttttt11222](https://t.me/testtttttttt11222)

## 1. Find the Best Tool Before Writing Code (Arabic & English)
```bash
python scripts/gh_arsenal.py recommend "بوت تليجرام ذكي مع كشط مواقع"
python scripts/gh_arsenal.py recommend "security audit and reverse engineering"
```

## 2. Instant Offline BM25 Search Across 20,078+ Real GitHub Tools
```bash
python scripts/gh_arsenal.py mega --category security-pentest --query "scanner" --limit 10
python scripts/gh_arsenal.py mega --category mcp-servers --query "postgres" --limit 10
```

## 3. Audit Security & Compare Competing Repos Side-by-Side
```bash
python scripts/gh_arsenal.py audit-repo unclecode/crawl4ai
python scripts/gh_arsenal.py compare unclecode/crawl4ai mendableai/firecrawl
```

## 4. Scaffold a Complete Turnkey Project Stack in 1 Command
```bash
python scripts/gh_arsenal.py stack list
python scripts/gh_arsenal.py stack saas-ai --scaffold ./my-saas-app
```

## 5. Auto-Detect Install Commands (`quickstart`) & Inject MCP Server
```bash
python scripts/gh_arsenal.py quickstart unclecode/crawl4ai
python scripts/gh_arsenal.py mcp-inject github-ai-arsenal
```

## 6. Pull Any GitHub Repo Without `git` or Install as Agent Skill
```bash
python scripts/gh_arsenal.py inspect D4Vinci/Scrapling
python scripts/gh_arsenal.py pull D4Vinci/Scrapling --dest ./github_tools
python scripts/gh_arsenal.py install-skill anthropics/skills
```
