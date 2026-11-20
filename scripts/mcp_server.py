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

SERVER_INFO = {"name": "github-ai-arsenal", "version": "4.0.0"}
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
    raise ValueError(f"Unknown MCP tool: {name}")


def _send(obj: Dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(obj, ensure_ascii=False) + "\n")
    sys.stdout.flush()


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
                "capabilities": {"tools": {}},
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
    for line in sys.stdin:
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
