#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FAZAH AI Arsenal v5.0 — Zero-Dependency Interactive Local Web UI (`fazah ui`)
Runs on pure Python stdlib (http.server) with instant live search across 20,078+ GitHub tools,
Deep Security Scanner, Quickstart generator, and 8 Turnkey Project Stacks.
"""

from __future__ import annotations

import json
import sys
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import gh_arsenal as arsenal

HTML_PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>⚡ FAZAH AI Arsenal v5.0 — 20,078+ GitHub Tools</title>
<style>
  :root {
    --bg: #070b14; --panel: #0f172a; --card: #131c31; --border: #1e293b;
    --cyan: #38bdf8; --purple: #a855f7; --green: #22c55e; --amber: #f59e0b; --red: #ef4444;
    --text: #f8fafc; --muted: #94a3b8;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: radial-gradient(circle at top right, #1e1b4b 0%, var(--bg) 55%); color: var(--text); font-family: 'Segoe UI', system-ui, sans-serif; min-height: 100vh; }
  header { padding: 24px 32px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px; background: rgba(15,23,42,0.85); backdrop-filter: blur(12px); position: sticky; top: 0; z-index: 10; }
  .brand h1 { font-size: 22px; background: linear-gradient(90deg, var(--cyan), var(--purple)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .brand p { font-size: 12px; color: var(--muted); margin-top: 2px; }
  .badges { display: flex; gap: 10px; align-items: center; font-size: 12px; }
  .badge { padding: 5px 12px; border-radius: 999px; background: var(--card); border: 1px solid var(--border); color: var(--cyan); font-weight: 600; }
  main { max-width: 1260px; margin: 28px auto; padding: 0 24px 60px; }
  .search-bar { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 22px; }
  input, select { background: var(--panel); border: 1px solid #334155; color: var(--text); padding: 12px 16px; border-radius: 10px; font-size: 15px; outline: none; }
  input:focus, select:focus { border-color: var(--cyan); box-shadow: 0 0 0 2px rgba(56,189,248,0.2); }
  #q { flex: 1; min-width: 260px; }
  button { background: linear-gradient(135deg, var(--cyan), var(--purple)); color: #fff; border: none; padding: 11px 20px; border-radius: 10px; font-weight: 700; cursor: pointer; font-size: 14px; transition: opacity .15s; }
  button:hover { opacity: 0.9; }
  button.sec { background: var(--card); border: 1px solid #334155; color: var(--text); font-weight: 600; padding: 7px 12px; font-size: 12px; }
  .tabs { display: flex; gap: 10px; margin-bottom: 20px; }
  .tab { padding: 8px 16px; border-radius: 8px; background: var(--panel); border: 1px solid var(--border); cursor: pointer; font-size: 13px; font-weight: 600; color: var(--muted); }
  .tab.active { border-color: var(--cyan); color: var(--cyan); background: rgba(56,189,248,0.1); }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 16px; }
  .card { background: var(--card); border: 1px solid var(--border); border-radius: 14px; padding: 18px; display: flex; flex-direction: column; justify-content: space-between; gap: 12px; transition: border-color .15s, transform .15s; }
  .card:hover { border-color: rgba(56,189,248,0.5); transform: translateY(-2px); }
  .card-top { display: flex; justify-content: space-between; align-items: start; gap: 8px; }
  .card h3 { font-size: 16px; color: var(--text); word-break: break-word; }
  .card a { color: var(--cyan); text-decoration: none; }
  .cat { font-size: 11px; padding: 3px 8px; border-radius: 6px; background: rgba(168,85,247,0.15); color: #d8b4fe; white-space: nowrap; }
  .desc { font-size: 13px; color: var(--muted); line-height: 1.5; }
  .actions { display: flex; gap: 8px; flex-wrap: wrap; }
  .modal-bg { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.75); backdrop-filter: blur(4px); z-index: 50; align-items: center; justify-content: center; padding: 20px; }
  .modal { background: var(--panel); border: 1px solid #334155; border-radius: 16px; max-width: 720px; width: 100%; max-height: 82vh; overflow: auto; padding: 24px; }
  pre { background: #020617; border: 1px solid var(--border); padding: 14px; border-radius: 10px; overflow-x: auto; font-size: 12.5px; color: #a5f3fc; margin-top: 12px; white-space: pre-wrap; }
  .status { font-size: 13px; color: var(--muted); margin-bottom: 14px; }
</style>
</head>
<body>
<header>
  <div class="brand">
    <h1>⚡ FAZAH AI Arsenal v5.0</h1>
    <p>Developer: FAZAH (@testtttttttt11222) • Zero-Dependency Local Dashboard</p>
  </div>
  <div class="badges">
    <span class="badge" id="stat-total">Loading index...</span>
    <span class="badge" style="color:#22c55e;">14 Native MCP Tools</span>
  </div>
</header>

<main>
  <div class="tabs">
    <div class="tab active" onclick="switchTab('search', this)">🔍 Search 20k+ Tools</div>
    <div class="tab" onclick="switchTab('stacks', this)">🏗️ 8 Turnkey Stacks</div>
  </div>

  <div id="view-search">
    <div class="search-bar">
      <input id="q" placeholder="Search 20,078+ GitHub tools (English or Arabic, e.g. 'mcp postgres', 'telegram', 'security')..." oninput="debouncedSearch()" />
      <select id="cat" onchange="doSearch()"><option value="">All 37 Domains</option></select>
      <button onclick="doSearch()">Search</button>
    </div>
    <div class="status" id="status">Ready.</div>
    <div class="grid" id="results"></div>
  </div>

  <div id="view-stacks" style="display:none;">
    <div class="grid" id="stacks-grid"></div>
  </div>
</main>

<div class="modal-bg" id="modal-bg" onclick="if(event.target===this) closeModal()">
  <div class="modal">
    <div style="display:flex;justify-content:space-between;align-items:center;">
      <h2 id="modal-title" style="font-size:18px;color:var(--cyan);">Details</h2>
      <button class="sec" onclick="closeModal()">✕ Close</button>
    </div>
    <pre id="modal-body">Loading...</pre>
  </div>
</div>

<script>
let timer = null;
function debouncedSearch() { clearTimeout(timer); timer = setTimeout(doSearch, 180); }
function openModal(title, content) {
  document.getElementById('modal-title').textContent = title;
  document.getElementById('modal-body').textContent = typeof content === 'string' ? content : JSON.stringify(content, null, 2);
  document.getElementById('modal-bg').style.display = 'flex';
}
function closeModal() { document.getElementById('modal-bg').style.display = 'none'; }

function switchTab(tab, el) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
  document.getElementById('view-search').style.display = tab === 'search' ? 'block' : 'none';
  document.getElementById('view-stacks').style.display = tab === 'stacks' ? 'block' : 'none';
}

async function init() {
  const st = await (await fetch('/api/stats')).json();
  document.getElementById('stat-total').textContent = `${st.mega_index_total.toLocaleString()}+ Indexed Tools`;
  const sel = document.getElementById('cat');
  Object.entries(st.categories).forEach(([c, n]) => {
    const opt = document.createElement('option');
    opt.value = c; opt.textContent = `${c} (${n})`;
    sel.appendChild(opt);
  });
  doSearch();
  const stacks = await (await fetch('/api/stacks')).json();
  const sg = document.getElementById('stacks-grid');
  sg.innerHTML = stacks.available_stacks.map(s => `
    <div class="card">
      <div>
        <div class="card-top"><h3>${s.name}</h3><span class="cat">${s.id}</span></div>
        <p class="desc" style="margin-top:8px;">${s.description}</p>
      </div>
      <div class="actions">
        <button class="sec" onclick="inspectStack('${s.id}')">View Components & Install Commands</button>
      </div>
    </div>
  `).join('');
}

async function inspectStack(id) {
  openModal('Stack: ' + id, 'Loading...');
  const data = await (await fetch('/api/stack?name=' + encodeURIComponent(id))).json();
  openModal('Stack: ' + data.name, data);
}

async function doSearch() {
  const q = document.getElementById('q').value;
  const c = document.getElementById('cat').value;
  const res = await (await fetch(`/api/search?q=${encodeURIComponent(q)}&c=${encodeURIComponent(c)}&limit=36`)).json();
  document.getElementById('status').textContent = `Showing ${res.shown} of ${res.total_matches.toLocaleString()} matching GitHub repositories (offline BM25).`;
  document.getElementById('results').innerHTML = res.tools.map(t => `
    <div class="card">
      <div>
        <div class="card-top">
          <h3><a href="https://github.com/${t.r}" target="_blank">${t.n}</a></h3>
          <span class="cat">${t.c}</span>
        </div>
        <p class="desc" style="margin-top:6px;">${(t.d || t.r).slice(0, 170)}</p>
      </div>
      <div class="actions">
        <button class="sec" onclick="runAction('audit', '${t.r}')">🛡️ Audit</button>
        <button class="sec" onclick="runAction('scan', '${t.r}')">🔬 Deep Scan</button>
        <button class="sec" onclick="runAction('quickstart', '${t.r}')">🚀 Quickstart</button>
      </div>
    </div>
  `).join('');
}

async function runAction(kind, repo) {
  openModal(`${kind.toUpperCase()} — ${repo}`, 'Running live GitHub inspection...');
  const data = await (await fetch(`/api/${kind}?repo=${encodeURIComponent(repo)}`)).json();
  openModal(`${kind.toUpperCase()} — ${repo}`, data);
}

init();
</script>
</body>
</html>
"""


class ArsenalUIHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:
        pass

    def _send_json(self, obj: dict, status: int = 200) -> None:
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        try:
            if parsed.path in ("/", "/index.html"):
                body = HTML_PAGE.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            if parsed.path == "/api/stats":
                mega = arsenal.load_mega_index()
                self._send_json({"mega_index_total": mega.get("total_tools", 0), "categories": mega.get("categories", {})})
                return
            if parsed.path == "/api/search":
                q = (qs.get("q") or [""])[0]
                c = (qs.get("c") or [""])[0]
                lim = int((qs.get("limit") or ["30"])[0])
                self._send_json(arsenal.mega_search_data(query=q, category=c, limit=lim))
                return
            if parsed.path == "/api/stacks":
                self._send_json(arsenal.stack_data("list"))
                return
            if parsed.path == "/api/stack":
                name = (qs.get("name") or ["list"])[0]
                self._send_json(arsenal.stack_data(name))
                return
            if parsed.path == "/api/audit":
                repo = (qs.get("repo") or [""])[0]
                self._send_json(arsenal.audit_repo_data(repo))
                return
            if parsed.path == "/api/scan":
                repo = (qs.get("repo") or [""])[0]
                self._send_json(arsenal.deep_scan_repo_data(repo))
                return
            if parsed.path == "/api/quickstart":
                repo = (qs.get("repo") or [""])[0]
                self._send_json(arsenal.quickstart_repo_data(repo))
                return
            self._send_json({"error": "Not found"}, 404)
        except Exception as exc:
            self._send_json({"error": str(exc)}, 500)


def run_ui(host: str = "127.0.0.1", port: int = 8765, open_browser: bool = True) -> None:
    server = ThreadingHTTPServer((host, port), ArsenalUIHandler)
    url = f"http://{host}:{port}"
    print(f"⚡ FAZAH AI Arsenal v5.0 Web UI running at {url} (Press Ctrl+C to stop)")
    if open_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped FAZAH AI Arsenal Web UI.")
    finally:
        server.server_close()


if __name__ == "__main__":
    run_ui()
