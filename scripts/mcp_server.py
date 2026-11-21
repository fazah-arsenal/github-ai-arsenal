#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub AI Arsenal — Zero-Dependency Native MCP Server (stdio JSON-RPC 2.0)
==========================================================================
Exposes 7 native MCP tools over stdin/stdout so any MCP client
(DeepSeek Harness, Antigravity, Claude Code, Cursor, Windsurf) can call
the 20,000+ GitHub AI Arsenal directly without needing shell commands:

  1. arsenal_recommend       - Smart Arabic/English tool recommender (Core + 20k Mega Index)
  2. arsenal_search_offline  - Instant offline BM25/synonym search across 20,000+ GitHub repos
  3. arsenal_stack           - Complete cohesive project stacks (saas-ai, telegram-ai-bot, etc.)
  4. arsenal_audit_repo      - Security & Trust Score (0-100) audit before pulling any repo
  5. arsenal_inspect_repo    - Inspect repo metadata, files & README/SKILL.md without cloning
  6. arsenal_pull_repo       - Safely download & extract any GitHub repo ZIP without git
  7. arsenal_install_skill   - Install any GitHub repo as a local SKILL.md into ~/.agents/skills/
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import gh_arsenal as arsenal

SERVER_INFO = {"name": "github-ai-arsenal", "version": "6.5.0"}
PROTOCOL_VERSION = "2024-11-05"

MCP_TOOLS: List[Dict[str, Any]] = [
    {
        "name": "arsenal_recommend",
        "description": "Recommend the best GitHub AI tools, MCP servers, or libraries for a task (supports English & Arabic) from the 60 Core Elite picks + 20,000+ Mega Index.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "task": {"type": "string", "description": "Task description in Arabic or English"},
                "limit": {"type": "integer", "default": 5},
            },
            "required": ["task"],
        },
    },
    {
        "name": "arsenal_search_offline",
        "description": "Instant offline BM25/synonym search across 20,000+ curated real GitHub repositories across 30+ domains with zero API rate limits.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "default": ""},
                "category": {"type": "string", "default": ""},
                "limit": {"type": "integer", "default": 12},
            },
        },
    },
    {
        "name": "arsenal_stack",
        "description": "Return a complete, cohesive GitHub project tech stack with install commands (pass 'list' to see all 8 stacks: saas-ai, telegram-ai-bot, scraping-rag, security-pentest-lab, reverse-engineering-lab, desktop-app, voice-ai-agent, mcp-builder).",
        "inputSchema": {
            "type": "object",
            "properties": {"name": {"type": "string", "default": "list"}},
        },
    },
    {
        "name": "arsenal_audit_repo",
        "description": "Audit any GitHub repository before downloading or running it. Returns a Trust Score (0-100), verdict (TRUSTED/CAUTION/HIGH_RISK), stars, license, maintenance recency, and warnings.",
        "inputSchema": {
            "type": "object",
            "properties": {"repo": {"type": "string", "description": "owner/repo or GitHub URL"}},
            "required": ["repo"],
        },
    },
    {
        "name": "arsenal_inspect_repo",
        "description": "Inspect a GitHub repository's metadata, top-level files, and README/SKILL.md excerpt without cloning.",
        "inputSchema": {
            "type": "object",
            "properties": {"repo": {"type": "string"}},
            "required": ["repo"],
        },
    },
    {
        "name": "arsenal_pull_repo",
        "description": "Safely download and extract any GitHub repository ZIP into a destination directory without requiring git.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "repo": {"type": "string"},
                "dest": {"type": "string", "default": "./github_tools"},
                "branch": {"type": "string", "default": ""},
            },
            "required": ["repo"],
        },
    },
    {
        "name": "arsenal_install_skill",
        "description": "Auto-discover SKILL.md (or synthesize one from README.md) and install a GitHub repo as a local Agent Skill in ~/.agents/skills/.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "repo": {"type": "string"},
                "target": {"type": "string", "default": ""},
            },
            "required": ["repo"],
        },
    },
    {
        "name": "arsenal_quickstart",
        "description": "Auto-detect ecosystem (Python/Node/Rust/Go/Docker) and return ready-to-run install & start commands for any GitHub repo.",
        "inputSchema": {
            "type": "object",
            "properties": {"repo": {"type": "string"}},
            "required": ["repo"],
        },
    },
    {
        "name": "arsenal_compare",
        "description": "Side-by-side comparison of 2 or more GitHub repositories (Trust Score, Stars, License, Maintenance) and recommend the winner.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "repos": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["repos"],
        },
    },
    {
        "name": "arsenal_scaffold_stack",
        "description": "Scaffold a complete starter project directory (README, setup_stack.ps1/sh, .env.example, .mcp.json) from any of the 8 project stacks.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "dest": {"type": "string"},
            },
            "required": ["name", "dest"],
        },
    },
    {
        "name": "arsenal_bookmark",
        "description": "Save, list, or remove bookmarked favorite GitHub tools with notes.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "default": "list"},
                "repo": {"type": "string", "default": ""},
                "note": {"type": "string", "default": ""},
            },
        },
    },
    {
        "name": "arsenal_mcp_inject",
        "description": "Safely inject an MCP server (e.g., github-ai-arsenal, github, playwright, context7) into a .mcp.json configuration file with backup.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "server": {"type": "string"},
                "target": {"type": "string", "default": ""},
            },
            "required": ["server"],
        },
    },
    {
        "name": "arsenal_deep_scan",
        "description": "Deep supply-chain security scan of a GitHub repo's install/build files (setup.py, package.json, install.sh, Dockerfile) for malicious patterns (curl|sh, eval, webhooks, postinstall hooks).",
        "inputSchema": {
            "type": "object",
            "properties": {"repo": {"type": "string"}},
            "required": ["repo"],
        },
    },
    {
        "name": "arsenal_analyze_project",
        "description": "Analyze a local project directory (package.json, requirements.txt, Cargo.toml, etc.) and recommend the best missing GitHub tools & MCP servers from the 20,078+ index.",
        "inputSchema": {
            "type": "object",
            "properties": {"path": {"type": "string", "default": "."}},
        },
    },
    {
        "name": "arsenal_give_tool",
        "description": "1-Call Autonomous Tool Broker: give me any task in English or Arabic and I will return the #1 GitHub tool from 20,078+ repos, its supply-chain security scan, install command, extracted code snippet, and optionally auto-pull it.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "task": {"type": "string", "description": "What you need the tool to do (English or Arabic)"},
                "auto_pull": {"type": "boolean", "default": False},
                "dest": {"type": "string", "default": "./github_tools"},
            },
            "required": ["task"],
        },
    },
    {
        "name": "arsenal_get_snippet",
        "description": "Extract clean, runnable code snippets directly from any GitHub repo README without downloading the whole README (saves 85% tokens).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "repo": {"type": "string"},
                "max_blocks": {"type": "integer", "default": 4},
            },
            "required": ["repo"],
        },
    },
    {
        "name": "arsenal_memory",
        "description": "Agent experience memory: list, inspect mistakes, clear, or log working/failed GitHub tools on this machine.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "default": "list", "enum": ["list", "mistakes", "clear", "learn"]},
                "repo": {"type": "string", "default": ""},
                "task": {"type": "string", "default": ""},
                "outcome": {"type": "string", "default": "success", "enum": ["success", "failed"]},
                "error_reason": {"type": "string", "default": ""},
                "learned_fix": {"type": "string", "default": ""},
                "alternative_repo": {"type": "string", "default": ""},
                "note": {"type": "string", "default": ""},
            },
        },
    },
    {
        "name": "arsenal_learn",
        "description": "Adaptive Mistake Learning: Teach FAZAH AI Arsenal about a tool failure or success on this machine so future tool selections automatically avoid broken packages and recommend verified alternatives.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "repo": {"type": "string", "description": "owner/repo that failed or succeeded"},
                "task": {"type": "string", "description": "The task you were attempting"},
                "outcome": {"type": "string", "enum": ["failed", "success"]},
                "error_reason": {"type": "string", "description": "Specific failure or error trace", "default": ""},
                "learned_fix": {"type": "string", "description": "Solution, workaround, or prerequisite", "default": ""},
                "alternative_repo": {"type": "string", "description": "Working replacement repo (owner/repo)", "default": ""},
                "note": {"type": "string", "default": ""},
            },
            "required": ["repo", "task", "outcome"],
        },
    },
]

MCP_RESOURCES: List[Dict[str, Any]] = [
    {"uri": "arsenal://stats", "name": "Index Statistics (20,078+ Tools)", "mimeType": "application/json"},
    {"uri": "arsenal://stacks", "name": "8 Turnkey Project Stacks", "mimeType": "application/json"},
    {"uri": "arsenal://bookmarks", "name": "Saved Favorite Tools", "mimeType": "application/json"},
    {"uri": "arsenal://memory", "name": "Agent Experience Memory", "mimeType": "application/json"},
]

MCP_PROMPTS: List[Dict[str, Any]] = [
    {
        "name": "fazah-give-tool",
        "description": "Ask FAZAH AI Arsenal to pick, security-scan, and deliver the #1 GitHub tool with runnable code for a task.",
        "arguments": [{"name": "task", "description": "Task description", "required": True}],
    },
    {
        "name": "fazah-build-stack",
        "description": "Scaffold a complete production project from one of the 8 FAZAH AI Arsenal blueprints.",
        "arguments": [{"name": "stack", "description": "Stack ID (e.g. saas-ai, telegram-ai-bot)", "required": True}],
    },
    {
        "name": "fazah-security-audit",
        "description": "Run both Trust Score audit and Deep Supply-Chain Scan on a GitHub repository before installing it.",
        "arguments": [{"name": "repo", "description": "owner/repo", "required": True}],
    },
]


def _call_tool(name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    if name == "arsenal_recommend":
        return arsenal.recommend_data(args["task"], limit=int(args.get("limit") or 5))
    if name == "arsenal_search_offline":
        return arsenal.mega_search_data(
            query=args.get("query", ""),
            category=args.get("category", ""),
            limit=int(args.get("limit") or 12),
        )
    if name == "arsenal_stack":
        return arsenal.stack_data(args.get("name", "list"))
    if name == "arsenal_audit_repo":
        return arsenal.audit_repo_data(args["repo"])
    if name == "arsenal_inspect_repo":
        return arsenal.inspect_repo_data(args["repo"])
    if name == "arsenal_pull_repo":
        return arsenal.pull_repo_data(
            args["repo"], dest=args.get("dest", "./github_tools"), branch=args.get("branch", "")
        )
    if name == "arsenal_install_skill":
        return arsenal.install_skill_data(args["repo"], target=args.get("target", ""))
    if name == "arsenal_quickstart":
        return arsenal.quickstart_repo_data(args["repo"])
    if name == "arsenal_compare":
        return arsenal.compare_repos_data(list(args.get("repos") or []))
    if name == "arsenal_scaffold_stack":
        return arsenal.scaffold_stack_data(args["name"], args["dest"])
    if name == "arsenal_bookmark":
        return arsenal.bookmark_data(
            args.get("action", "list"), args.get("repo", ""), args.get("note", "")
        )
    if name == "arsenal_mcp_inject":
        return arsenal.mcp_inject_data(args["server"], args.get("target", ""))
    if name == "arsenal_deep_scan":
        return arsenal.deep_scan_repo_data(args["repo"])
    if name == "arsenal_analyze_project":
        return arsenal.analyze_project_data(args.get("path", "."))
    if name == "arsenal_give_tool":
        return arsenal.give_tool_data(
            args["task"], auto_pull=bool(args.get("auto_pull", False)), dest=args.get("dest", "./github_tools")
        )
    if name == "arsenal_get_snippet":
        return arsenal.snippet_repo_data(args["repo"], max_blocks=int(args.get("max_blocks") or 4))
    if name == "arsenal_memory":
        return arsenal.memory_data(
            action=args.get("action", "list"),
            repo_input=args.get("repo", ""),
            task=args.get("task", ""),
            outcome=args.get("outcome", "success"),
            note=args.get("note", ""),
            error_reason=args.get("error_reason", ""),
            learned_fix=args.get("learned_fix", ""),
            alternative_repo=args.get("alternative_repo", ""),
        )
    if name == "arsenal_learn":
        return arsenal.memory_data(
            action="learn",
            repo_input=args["repo"],
            task=args.get("task", ""),
            outcome=args["outcome"],
            note=args.get("note", ""),
            error_reason=args.get("error_reason", ""),
            learned_fix=args.get("learned_fix", ""),
            alternative_repo=args.get("alternative_repo", ""),
        )
    raise ValueError(f"Unknown MCP tool: {name}")


def _send(obj: Dict[str, Any]) -> None:
    try:
        sys.stdout.write(json.dumps(obj, ensure_ascii=False) + "\n")
        sys.stdout.flush()
    except Exception as exc:
        sys.stderr.write(f"[mcp_server] Write error: {exc}\n")
        sys.stderr.flush()


def handle_message(msg: Dict[str, Any]) -> None:
    req_id = msg.get("id")
    method = msg.get("method", "")
    params = msg.get("params") or {}

    if method == "initialize":
        _send({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {}, "resources": {}, "prompts": {}},
                "serverInfo": SERVER_INFO,
            },
        })
        return

    if method == "notifications/initialized":
        return

    if method == "ping":
        _send({"jsonrpc": "2.0", "id": req_id, "result": {}})
        return

    if method == "tools/list":
        _send({"jsonrpc": "2.0", "id": req_id, "result": {"tools": MCP_TOOLS}})
        return

    if method == "resources/list":
        _send({"jsonrpc": "2.0", "id": req_id, "result": {"resources": MCP_RESOURCES}})
        return

    if method == "resources/read":
        uri = params.get("uri", "")
        if uri == "arsenal://stats":
            mega = arsenal.load_mega_index()
            payload = {"mega_index_total": mega.get("total_tools", 0), "categories": mega.get("categories", {})}
        elif uri == "arsenal://stacks":
            payload = arsenal.stack_data("list")
        elif uri == "arsenal://bookmarks":
            payload = arsenal.bookmark_data("list")
        elif uri == "arsenal://memory":
            payload = arsenal.memory_data("list")
        else:
            payload = {"error": f"Unknown resource URI: {uri}"}
        _send({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"contents": [{"uri": uri, "mimeType": "application/json", "text": json.dumps(payload, ensure_ascii=False, indent=2)}]},
        })
        return

    if method == "prompts/list":
        _send({"jsonrpc": "2.0", "id": req_id, "result": {"prompts": MCP_PROMPTS}})
        return

    if method == "prompts/get":
        p_name = params.get("name", "")
        p_args = params.get("arguments") or {}
        if p_name == "fazah-give-tool":
            text = f"Call the `arsenal_give_tool` MCP tool with task='{p_args.get('task', '')}' and deliver the verified #1 GitHub tool, security scan, install command, and runnable code snippet."
        elif p_name == "fazah-build-stack":
            text = f"Call `arsenal_scaffold_stack` with name='{p_args.get('stack', 'saas-ai')}' and guide the user through launching it."
        elif p_name == "fazah-security-audit":
            text = f"Call both `arsenal_audit_repo` and `arsenal_deep_scan` on '{p_args.get('repo', '')}' and summarize all security findings before installing."
        else:
            text = f"Use FAZAH AI Arsenal tools to assist with: {p_name}"
        _send({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"messages": [{"role": "user", "content": {"type": "text", "text": text}}]},
        })
        return

    if method == "tools/call":
        t_name = params.get("name", "")
        t_args = params.get("arguments") or {}
        try:
            data = _call_tool(t_name, t_args)
            _send({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(data, ensure_ascii=False, indent=2)}],
                    "isError": False,
                },
            })
        except Exception as exc:
            _send({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": f"Error: {exc}"}],
                    "isError": True,
                },
            })
        return

    if req_id is not None:
        _send({
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method not found: {method}"},
        })


def main() -> None:
    # Ensure standard IO is configured for UTF-8 with immediate line flushing
    try:
        if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
            sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
        if sys.stdin.encoding and sys.stdin.encoding.lower() != "utf-8":
            sys.stdin.reconfigure(encoding="utf-8")
    except Exception:
        pass

    while True:
        try:
            line = sys.stdin.readline()
        except Exception:
            break
        if not line:
            break
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
            if isinstance(msg, dict):
                handle_message(msg)
        except Exception as exc:
            _send({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": f"Parse error: {exc}"}})


if __name__ == "__main__":
    main()
