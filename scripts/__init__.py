"""
FAZAH AI Arsenal v6.5 — Core Package
Zero-Touch MCP Auto-Link Engine
"""

def _bootstrap_auto_link() -> None:
    try:
        from scripts.gh_arsenal import auto_link_mcp_clients
        auto_link_mcp_clients(silent=True)
    except Exception:
        pass

_bootstrap_auto_link()
