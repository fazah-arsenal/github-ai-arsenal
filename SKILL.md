---
name: github-ai-arsenal
description: Master GitHub AI Toolbox Skill v6.5 (by FAZAH | @testtttttttt11222) equipping any AI agent with 20,078+ real, curated GitHub tools across 37 domains, a 17-tool zero-dependency Native MCP Server (+ 4 Resources & 3 Prompts), 1-Call Autonomous Tool Broker (`fazah g`), Deep Supply-Chain Security Scanner (`fazah scan`), Local Web UI (`fazah ui`), Project Advisor (`fazah az`), Isolated Sandbox (`fazah try`), Self-Updater (`fazah up`), and instant offline BM25 search.
metadata:
  version: "6.5.0"
  author: "FAZAH"
  telegram: "@testtttttttt11222"
  email: "mhamadabdalla150150@gmail.com"
  indexed_tools: "20,078+"
  mcp_server: "scripts/mcp_server.py"
  compatible_with: "DeepSeek Harness, Antigravity, Claude Code, Codex, Cursor, Windsurf"
---

# GitHub AI Arsenal v6.5 (`github-ai-arsenal`)

**Developed by FAZAH** (`@testtttttttt11222` | `mhamadabdalla150150@gmail.com`)

The ultimate AI Agent Toolbox: gives any AI agent instant access to **20,078+ real GitHub tools**, a **12-tool Native MCP Server**, **1-command project scaffolding**, **side-by-side repo comparisons**, and **repository security audits** with zero external dependencies.

---

## 1. Native MCP Server (`scripts/mcp_server.py` — 18 Tools)

Inject automatically into `.mcp.json`:
```bash
python scripts/gh_arsenal.py mcp-inject arsenal
```

Exposed MCP Tools:
1. `arsenal_give_tool`: 1-Call Autonomous Tool Broker with security scan, code snippet, and auto-pull.
2. `arsenal_learn`: Adaptive mistake-learning reflex (penalize broken tools, route to working alternatives).
3. `arsenal_mistakes`: List all recorded tool mistakes and learned fixes.
4. `arsenal_recommend`: Arabic/English intelligent tool recommender.
5. `arsenal_search_offline`: Instant BM25 offline search across 20,078+ repositories.
6. `arsenal_deep_scan`: Deep supply-chain security scan of install/build scripts.
7. `arsenal_get_snippet`: Extract runnable code snippets from README without full downloads.
8. `arsenal_memory`: Agent experience memory (list, clear, log tool outcomes).
9. `arsenal_analyze_project`: Detect missing tools/MCP servers for current project folder.
10. `arsenal_stack`: Browse 8 turnkey project stacks.
11. `arsenal_scaffold_stack`: Generate a full starter project folder (`README.md`, `setup_stack.ps1`, `.env.example`, `.mcp.json`).
12. `arsenal_quickstart`: Auto-detect ecosystem and output ready install/run commands for any repo.
13. `arsenal_compare`: Compare 2+ repositories side-by-side (Trust Score, Stars, License, Recency).
14. `arsenal_audit_repo`: Trust Score (0-100) and security risk audit before pulling code.
15. `arsenal_bookmark`: Save, list, or remove favorite GitHub tools with notes.
16. `arsenal_mcp_inject`: Safely inject any MCP server into `.mcp.json` with backup.
17. `arsenal_inspect_repo`: Inspect metadata, files, and README/SKILL.md without cloning.
18. `arsenal_pull_repo`: Download and unpack repo ZIP without git.

---

## 2. Short CLI Commands (`fazah` or `python scripts/gh_arsenal.py`)

```bash
fazah g "scrape dynamic javascript websites"   # 1-call tool delivery with security scan
fazah mem mistakes                             # Show all learned tool failures & fixes
fazah ui                                       # Launch local interactive Web dashboard
fazah doc                                      # Check local runtimes & index health
fazah info                                     # Breakdown of 20,078+ tools across 37 domains
fazah r "telegram bot and web scraping"        # Smart Arabic/English recommender
fazah m -q "postgres vector" -n 10             # Instant offline BM25 search
fazah q unclecode/crawl4ai                     # Auto-detect install & run commands
fazah cmp unclecode/crawl4ai mendableai/firecrawl # Side-by-side repo comparison
fazah a modelcontextprotocol/servers           # Security & Trust Score (0-100) audit
fazah scan unclecode/crawl4ai                  # Deep supply-chain security scan
fazah st saas-ai -s ./my-saas-app              # Scaffold turnkey project stack
fazah bm add unclecode/crawl4ai -m "Best"      # Bookmark favorite tools
fazah mi arsenal                               # Inject MCP config into .mcp.json
fazah i danielmiessler/fabric                  # Inspect repo without cloning
fazah p unclecode/crawl4ai -d ./tools          # Pull repo ZIP without git
fazah is anthropics/skills                     # Install repo as local Agent Skill
```
