---
name: github-ai-arsenal
description: Master GitHub AI Toolbox Skill v4.0 (by FAZAH | @testtttttttt11222) equipping any AI agent with 20,078+ real, curated GitHub tools across 37 domains, a 12-tool zero-dependency Native MCP Server (`scripts/mcp_server.py`), Turnkey Project Scaffolder (`stack --scaffold`), Repository Security & Trust Auditor (`audit-repo` & `compare`), Smart Quickstart (`quickstart`), Bookmarks (`bookmark`), Auto MCP Injector (`mcp-inject`), and instant offline BM25 search (`mega` & `recommend`).
metadata:
  version: "4.0.0"
  author: "FAZAH"
  telegram: "@testtttttttt11222"
  email: "mhamadabdalla150150@gmail.com"
  indexed_tools: "20,078+"
  mcp_server: "scripts/mcp_server.py"
  compatible_with: "DeepSeek Harness, Antigravity, Claude Code, Codex, Cursor, Windsurf"
---

# GitHub AI Arsenal v4.0 (`github-ai-arsenal`)

**Developed by FAZAH** (`@testtttttttt11222` | `mhamadabdalla150150@gmail.com`)

The ultimate AI Agent Toolbox: gives any AI agent instant access to **20,078+ real GitHub tools**, a **12-tool Native MCP Server**, **1-command project scaffolding**, **side-by-side repo comparisons**, and **repository security audits** with zero external dependencies.

---

## 1. Native MCP Server (`scripts/mcp_server.py` — 12 Tools)

Inject automatically into `.mcp.json`:
```bash
python scripts/gh_arsenal.py mcp-inject github-ai-arsenal
```

Exposed MCP Tools:
1. `arsenal_recommend`: Arabic/English intelligent tool recommender.
2. `arsenal_search_offline`: Instant BM25 offline search across 20,078+ repositories.
3. `arsenal_stack`: Browse 8 turnkey project stacks.
4. `arsenal_scaffold_stack`: Generate a full starter project folder (`README.md`, `setup_stack.ps1`, `.env.example`, `.mcp.json`).
5. `arsenal_quickstart`: Auto-detect ecosystem and output ready install/run commands for any repo.
6. `arsenal_compare`: Compare 2+ repositories side-by-side (Trust Score, Stars, License, Recency).
7. `arsenal_audit_repo`: Trust Score (0-100) and security risk audit before pulling code.
8. `arsenal_bookmark`: Save, list, or remove favorite GitHub tools with notes.
9. `arsenal_mcp_inject`: Safely inject any MCP server into `.mcp.json` with backup.
10. `arsenal_inspect_repo`: Inspect metadata, files, and README/SKILL.md without cloning.
11. `arsenal_pull_repo`: Download and unpack repo ZIP without git.
12. `arsenal_install_skill`: Automatically install any repo as a local agent skill.

---

## 2. Short CLI Commands (`fazah` or `python scripts/gh_arsenal.py`)

```bash
fazah doc                                  # Check local runtimes & index health
fazah info                                 # Breakdown of 20,078+ tools across 37 domains
fazah r "telegram bot and web scraping"    # Smart Arabic/English recommender
fazah m -q "postgres vector" -n 10         # Instant offline BM25 search
fazah q unclecode/crawl4ai                 # Auto-detect install & run commands
fazah cmp unclecode/crawl4ai mendableai/firecrawl   # Side-by-side repo comparison
fazah a modelcontextprotocol/servers       # Security & Trust Score (0-100) audit
fazah st saas-ai -s ./my-saas-app          # Scaffold turnkey project stack
fazah bm add unclecode/crawl4ai -m "Best"  # Bookmark favorite tools
fazah mi github-ai-arsenal                 # Inject MCP config into .mcp.json
fazah i danielmiessler/fabric              # Inspect repo without cloning
fazah p unclecode/crawl4ai -d ./tools      # Pull repo ZIP without git
fazah is anthropics/skills                 # Install repo as local Agent Skill
```
