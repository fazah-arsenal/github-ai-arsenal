"""
FAZAH AI Arsenal v6.5 — Studio Narrated Walkthrough Video Generator
Includes live MCP Client demonstration showing agent tool invocation,
deep search, AST security audit, and 1-call code delivery.
"""

import asyncio
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
import edge_tts

WIDTH, HEIGHT = 1280, 720
FPS = 30
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

# Fonts
FONT_DIR = "C:/Windows/Fonts"
font_title = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 28)
font_subtitle = ImageFont.truetype(os.path.join(FONT_DIR, "segoeui.ttf"), 17)
font_card_title = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 19)
font_badge = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 13)
font_body = ImageFont.truetype(os.path.join(FONT_DIR, "segoeui.ttf"), 15)
font_caption = ImageFont.truetype(os.path.join(FONT_DIR, "segoeui.ttf"), 16)

font_code_large = ImageFont.truetype(os.path.join(FONT_DIR, "consolab.ttf"), 17)
font_code = ImageFont.truetype(os.path.join(FONT_DIR, "consola.ttf"), 14)
font_code_small = ImageFont.truetype(os.path.join(FONT_DIR, "consola.ttf"), 12)

# Colors
BG_TOP = (11, 15, 26)
BG_BOTTOM = (5, 8, 15)
CARD_BG = (17, 24, 39)
CARD_BORDER = (31, 41, 55)
HEADER_BG = (24, 32, 50)
ACCENT_CYAN = (56, 189, 248)
ACCENT_PURPLE = (168, 85, 247)
ACCENT_GREEN = (34, 197, 94)
ACCENT_AMBER = (245, 158, 11)
ACCENT_RED = (239, 68, 68)
TEXT_WHITE = (243, 244, 246)
TEXT_MUTED = (156, 163, 175)
TEXT_DIM = (107, 114, 128)

SCENES = [
    {
        "id": "intro",
        "step_name": "1. Overview",
        "title": "⚡ FAZAH AI ARSENAL v6.5",
        "subtitle": "The Ultimate AI Agent Skill & Native MCP Server",
        "narration": "Welcome to FAZAH AI Arsenal, the ultimate developer skill and native Model Context Protocol server for AI coding agents. FAZAH indexes over 20,000 production-ready GitHub repositories and 5,300 MCP servers directly on your machine, saving up to 90% of your AI token quota."
    },
    {
        "id": "install",
        "step_name": "2. Install",
        "title": "📦 Step 1: Downloading & Installing FAZAH",
        "subtitle": "Fast, lightweight, single-command installation",
        "narration": "Installing FAZAH Arsenal is effortless. You can install it with pip by running: pip install fazah-arsenal. Or use our one-line installer for Windows, Linux, and macOS. Within seconds, the entire 20,000-tool offline catalog is compressed and ready on your machine."
    },
    {
        "id": "link",
        "step_name": "3. Auto-Link",
        "title": "🔌 Step 2: Zero-Touch MCP Auto-Link",
        "subtitle": "Automatic connection to all your AI editors & environments",
        "narration": "Forget about manual JSON editing or path headaches. Simply run 'fazah link'. FAZAH automatically discovers and configures every MCP client on your system: Claude Desktop, Cursor IDE, Windsurf, Google Antigravity, and VS Code. Everything is linked with zero friction."
    },
    {
        "id": "mcp_live",
        "step_name": "4. Live MCP Demo",
        "title": "⚡ Step 3: Live MCP Client & Skill Invocation",
        "subtitle": "Watch how the AI agent interacts with FAZAH tools in real time",
        "narration": "Now, let's see FAZAH in action inside an active MCP client. When the user asks to build an async Telegram bot with rate limiting, watch how the AI interacts with the skill. First, it invokes arsenal_search to discover verified libraries offline. Next, it runs arsenal_audit to verify repository security and trust score. Finally, it calls arsenal_give to extract clean boilerplate. The AI produces production-ready code in seconds with zero hallucination and zero token waste."
    },
    {
        "id": "antigravity",
        "step_name": "5. Antigravity",
        "title": "🚀 Step 4: Integration with Google Antigravity",
        "subtitle": "Autonomous tool resolution directly in Antigravity IDE",
        "narration": "Here is how it works with Google Antigravity. When you ask the agent to build a project, Antigravity calls the FAZAH native MCP server. Instead of searching the web or hallucinating packages, it immediately gets verified code for Crawl4AI in a single call, completely offline."
    },
    {
        "id": "deepseek",
        "step_name": "6. DeepSeek",
        "title": "🧠 Step 5: Integration with DeepSeek & Universal AI",
        "subtitle": "DeepSeek V3, R1, Claude, and GPT-4o powered by 18 MCP Tools",
        "narration": "FAZAH is model-agnostic. Whether you are using DeepSeek-V3 or DeepSeek-R1 inside Cline or Continue, or chatting with Claude and GPT, the model gains 18 powerful tools: smart repository search, instant code scaffolding, AST security auditing, and offline tool recommendations."
    },
    {
        "id": "savings",
        "step_name": "7. Savings",
        "title": "💰 Step 6: Token & Quota Savings Tracker",
        "subtitle": "Track your saved tokens, API calls, and developer time",
        "narration": "Every AI search usually burns thousands of tokens. With FAZAH's local index, searches take zero API calls. Run 'fazah savings' to see your live dashboard. Over 320,000 tokens and dozens of external calls saved, directly protecting your wallet and daily quota."
    },
    {
        "id": "memory",
        "step_name": "8. Memory",
        "title": "🛡️ Step 7: Adaptive Error Memory & Self-Healing",
        "subtitle": "AI models never repeat the same mistake twice",
        "narration": "When an AI tries to import a deprecated or incompatible library, FAZAH records the failure and the working alternative into its adaptive memory. Next time any agent requests a similar task, FAZAH warns it and recommends the proven library automatically."
    },
    {
        "id": "finish",
        "step_name": "9. Start",
        "title": "⭐ Get Started with FAZAH AI Arsenal",
        "subtitle": "Open Source · Production Ready · Available Everywhere",
        "narration": "FAZAH AI Arsenal is 100% open source and ready today. Install it with pip, grab the docker container, or check out the code on GitHub at github.com/fazah-arsenal/github-ai-arsenal. Star the repository and upgrade your AI workflow now!"
    }
]

def get_audio_duration(audio_path):
    cmd = [FFMPEG, "-i", str(audio_path)]
    proc = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, errors="ignore")
    for line in proc.stderr.splitlines():
        if "Duration:" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
            h, m, s = float(parts[0]), float(parts[1]), float(parts[2])
            return h * 3600 + m * 60 + s
    return 10.0

async def generate_speech_tracks(temp_dir: Path):
    temp_dir.mkdir(parents=True, exist_ok=True)
    voice = "en-US-GuyNeural"
    tracks = []
    
    for idx, sc in enumerate(SCENES):
        mp3_path = temp_dir / f"scene_{idx:02d}.mp3"
        print(f"🎙️ Generating voiceover for [{sc['step_name']}]...")
        communicate = edge_tts.Communicate(sc["narration"], voice=voice)
        await communicate.save(str(mp3_path))
        duration = get_audio_duration(mp3_path)
        tracks.append({
            "index": idx,
            "scene": sc,
            "audio_path": mp3_path,
            "duration": duration,
            "frames": int(duration * FPS) + 15
        })
        print(f"   -> Duration: {duration:.2f}s ({tracks[-1]['frames']} frames)")
    return tracks

def create_base_canvas(scene_idx, total_scenes):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_BOTTOM)
    draw = ImageDraw.Draw(img)
    
    # Top subtle gradient
    for y in range(160):
        alpha = int((1.0 - (y / 160.0)) * 25)
        draw.line([(0, y), (WIDTH, y)], fill=(BG_TOP[0] + alpha, BG_TOP[1] + alpha, BG_TOP[2] + alpha))

    # Top Navigation Breadcrumbs
    nav_y = 15
    pill_w = 108
    spacing = 12
    start_x = (WIDTH - (len(SCENES) * pill_w + (len(SCENES)-1) * spacing)) // 2
    
    for i, s in enumerate(SCENES):
        bx = start_x + i * (pill_w + spacing)
        is_active = (i == scene_idx)
        is_past = (i < scene_idx)
        
        bg_col = (30, 41, 59) if not is_active else (15, 23, 42)
        border_col = ACCENT_CYAN if is_active else (ACCENT_GREEN if is_past else CARD_BORDER)
        text_col = ACCENT_CYAN if is_active else (ACCENT_GREEN if is_past else TEXT_DIM)
        
        draw.rounded_rectangle([bx, nav_y, bx + pill_w, nav_y + 26], radius=5, fill=bg_col, outline=border_col, width=1)
        draw.text((bx + 8, nav_y + 5), s["step_name"], font=font_code_small, fill=text_col)

    draw.line([(40, 54), (WIDTH - 40, 54)], fill=CARD_BORDER, width=1)
    return img, draw

def draw_window(img, draw, x, y, w, h, title="terminal — fazah@arsenal"):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD_BG, outline=CARD_BORDER, width=1)
    header_h = 32
    draw.rounded_rectangle([x, y, x + w, y + header_h], radius=10, fill=HEADER_BG)
    draw.rectangle([x, y + header_h - 10, x + w, y + header_h], fill=HEADER_BG)
    draw.line([(x, y + header_h), (x + w, y + header_h)], fill=CARD_BORDER, width=1)

    draw.ellipse([x + 14, y + 10, x + 24, y + 20], fill=ACCENT_RED)
    draw.ellipse([x + 30, y + 10, x + 40, y + 20], fill=ACCENT_AMBER)
    draw.ellipse([x + 46, y + 10, x + 56, y + 20], fill=ACCENT_GREEN)

    draw.text((x + w // 2 - 110, y + 6), title, font=font_code_small, fill=TEXT_MUTED)

def draw_bottom_caption(draw, text, frame_progress):
    bar_h = 58
    bar_y = HEIGHT - bar_h - 14
    draw.rounded_rectangle([50, bar_y, WIDTH - 50, bar_y + bar_h], radius=10, fill=(12, 17, 30), outline=CARD_BORDER, width=1)
    
    cx = 72
    cy = bar_y + 29
    wave_h = [8, 18, 24, 14, 22, 10, 16]
    for i, wh in enumerate(wave_h):
        phase = (frame_progress * 12 + i) % 3.14
        dyn_h = int(wh * (0.6 + 0.4 * np.sin(phase)))
        draw.line([(cx + i * 5, cy - dyn_h // 2), (cx + i * 5, cy + dyn_h // 2)], fill=ACCENT_CYAN, width=2)

    draw.text((115, bar_y + 17), text[:130] + ("..." if len(text) > 130 else ""), font=font_caption, fill=TEXT_WHITE)

# ----------------- SCENE RENDERERS -----------------

def render_scene_intro(frame_idx, total_frames, scene_data):
    img, draw = create_base_canvas(0, len(SCENES))
    draw.text((70, 78), scene_data["title"], font=font_title, fill=ACCENT_CYAN)
    draw.text((70, 118), scene_data["subtitle"], font=font_subtitle, fill=TEXT_WHITE)
    
    stats = [
        ("20,078+", "Curated GitHub Tools", ACCENT_CYAN),
        ("5,306", "Indexed MCP Servers", ACCENT_PURPLE),
        ("18 Tools", "Native MCP Capabilities", ACCENT_GREEN),
        ("Up to 90%", "Token & Quota Saved", ACCENT_AMBER),
    ]
    card_w = 270
    card_h = 90
    for i, (num, lbl, col) in enumerate(stats):
        cx = 70 + i * (card_w + 20)
        cy = 165
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=10, fill=CARD_BG, outline=CARD_BORDER, width=1)
        draw.text((cx + 18, cy + 14), num, font=font_card_title, fill=col)
        draw.text((cx + 18, cy + 50), lbl, font=font_body, fill=TEXT_MUTED)

    win_x, win_y, win_w, win_h = 70, 280, WIDTH - 140, 310
    draw_window(img, draw, win_x, win_y, win_w, win_h, "architecture — local-first zero-latency bridge")
    
    features = [
        ("⚡ Zero-Touch MCP Auto-Link", "Autodetects & configures Claude Desktop, Cursor, Windsurf, Antigravity, VS Code"),
        ("📦 1-Call Autonomous Code Delivery", "Delivers verified imports, dependencies, and scaffolds with zero hallucination"),
        ("🛡️ AST Supply-Chain Security Audit", "Analyzes Python AST for dangerous eval, exec, network calls, and obfuscation"),
        ("🧠 Adaptive Error Memory", "Remembers broken packages & recommends battle-tested alternatives automatically"),
        ("💰 Real-time Quota Savings Engine", "Logs every API call avoided, token saved, and exact dollar amount spared"),
        ("🌐 100% Offline Capability", "Complete BM25 ranking algorithm operates locally with zero internet dependency")
    ]
    for i, (ft, desc) in enumerate(features):
        fy = win_y + 40 + i * 42
        draw.text((win_x + 20, fy), ft, font=font_badge, fill=ACCENT_CYAN if i % 2 == 0 else ACCENT_GREEN)
        draw.text((win_x + 350, fy), desc, font=font_code, fill=TEXT_MUTED)
        if i < len(features) - 1:
            draw.line([(win_x + 20, fy + 32), (win_x + win_w - 20, fy + 32)], fill=(22, 28, 42), width=1)

    draw_bottom_caption(draw, scene_data["narration"], frame_idx / total_frames)
    return img

def render_scene_install(frame_idx, total_frames, scene_data):
    img, draw = create_base_canvas(1, len(SCENES))
    draw.text((70, 78), scene_data["title"], font=font_title, fill=ACCENT_GREEN)
    draw.text((70, 118), scene_data["subtitle"], font=font_subtitle, fill=TEXT_WHITE)

    win_x, win_y, win_w, win_h = 70, 165, WIDTH - 140, 425
    draw_window(img, draw, win_x, win_y, win_w, win_h, "powershell / bash — terminal")

    lines = [
        ("$ pip install fazah-arsenal", ACCENT_CYAN, font_code_large),
        ("Collecting fazah-arsenal (v6.5.0)", TEXT_MUTED, font_code),
        ("  Downloading fazah_arsenal-6.5.0-py3-none-any.whl (4.6 MB)", TEXT_MUTED, font_code),
        ("  Installing collected packages: fazah-arsenal", TEXT_MUTED, font_code),
        ("Successfully installed fazah-arsenal-6.5.0", ACCENT_GREEN, font_code_large),
        ("", TEXT_MUTED, font_code),
        ("$ fazah doc", ACCENT_CYAN, font_code_large),
        ("╔═══════════════════════════════════════════════════════════════════════════════════════╗", ACCENT_PURPLE, font_code_small),
        ("║  FAZAH AI ARSENAL v6.5  ·  System Diagnostic & Health Check                           ║", ACCENT_PURPLE, font_code_small),
        ("╠═══════════════════════════════════════════════════════════════════════════════════════╣", ACCENT_PURPLE, font_code_small),
        ("║  ✓ Mega Catalog:     20,078 tools indexed & ready                                     ║", ACCENT_GREEN, font_code_small),
        ("║  ✓ MCP Server:       18 tools, 5 resources, 3 prompts ready                           ║", ACCENT_GREEN, font_code_small),
        ("║  ✓ Error Memory:     Adaptive self-healing active                                     ║", ACCENT_GREEN, font_code_small),
        ("║  ✓ Token Savings:    Tracker initialized (320,000+ tokens recorded)                   ║", ACCENT_AMBER, font_code_small),
        ("╚═══════════════════════════════════════════════════════════════════════════════════════╝", ACCENT_PURPLE, font_code_small),
    ]

    visible_lines = min(len(lines), int((frame_idx / total_frames) * (len(lines) + 3)))
    for idx in range(visible_lines):
        txt, col, fnt = lines[idx]
        draw.text((win_x + 25, win_y + 40 + idx * 22), txt, font=fnt, fill=col)

    draw_bottom_caption(draw, scene_data["narration"], frame_idx / total_frames)
    return img

def render_scene_link(frame_idx, total_frames, scene_data):
    img, draw = create_base_canvas(2, len(SCENES))
    draw.text((70, 78), scene_data["title"], font=font_title, fill=ACCENT_CYAN)
    draw.text((70, 118), scene_data["subtitle"], font=font_subtitle, fill=TEXT_WHITE)

    win_x, win_y, win_w, win_h = 70, 165, WIDTH - 140, 425
    draw_window(img, draw, win_x, win_y, win_w, win_h, "terminal — fazah link")

    clients = [
        ("Claude Desktop", "AppData/Roaming/Claude/claude_desktop_config.json", "LINKED"),
        ("Cursor IDE", ".cursor/mcp.json", "LINKED"),
        ("Windsurf", ".codeium/windsurf/mcp_config.json", "LINKED"),
        ("Google Antigravity", ".gemini/antigravity/mcp_config.json", "LINKED"),
        ("VS Code Cline", "User/globalStorage/saoudrizwan.claude-dev/.../cline_mcp_settings.json", "LINKED"),
        ("VS Code Roo", "User/globalStorage/rooveterinaryinc.roo-cline/.../roo_cline_mcp_settings.json", "LINKED"),
        ("Project Workspace", "./.mcp.json", "LINKED")
    ]

    draw.text((win_x + 25, win_y + 40), "$ fazah link", font=font_code_large, fill=ACCENT_CYAN)
    draw.text((win_x + 25, win_y + 68), "Scanning system for installed AI editors and MCP environments...", font=font_code, fill=TEXT_MUTED)

    visible_clients = min(len(clients), int((frame_idx / total_frames) * (len(clients) + 2)))
    for idx in range(visible_clients):
        cname, cpath, cstatus = clients[idx]
        cy = win_y + 105 + idx * 36
        draw.rounded_rectangle([win_x + 25, cy, win_x + 130, cy + 24], radius=4, fill=(16, 42, 28), outline=ACCENT_GREEN, width=1)
        draw.text((win_x + 35, cy + 3), f"✓ {cstatus}", font=font_code_small, fill=ACCENT_GREEN)
        draw.text((win_x + 145, cy + 3), f"{cname:<18}", font=font_code, fill=TEXT_WHITE)
        draw.text((win_x + 340, cy + 4), f"→ {cpath}", font=font_code_small, fill=TEXT_MUTED)

    if visible_clients >= len(clients):
        draw.text((win_x + 25, win_y + 375), "✨ All 7 MCP clients successfully linked! Zero manual configuration needed.", font=font_code, fill=ACCENT_GREEN)

    draw_bottom_caption(draw, scene_data["narration"], frame_idx / total_frames)
    return img

def render_scene_mcp_live(frame_idx, total_frames, scene_data):
    """Shows active MCP Client with tool calls: search -> audit -> give"""
    img, draw = create_base_canvas(3, len(SCENES))
    draw.text((70, 78), scene_data["title"], font=font_title, fill=ACCENT_AMBER)
    draw.text((70, 118), scene_data["subtitle"], font=font_subtitle, fill=TEXT_WHITE)

    # Master MCP Client Simulation Window
    win_x, win_y, win_w, win_h = 70, 165, WIDTH - 140, 425
    draw_window(img, draw, win_x, win_y, win_w, win_h, "Active MCP Client — Server: fazah-arsenal [CONNECTED · 18 TOOLS]")

    # Top Status Bar
    draw.rounded_rectangle([win_x + 20, win_y + 38, win_x + win_w - 20, win_y + 70], radius=6, fill=(18, 25, 42), outline=CARD_BORDER)
    draw.text((win_x + 32, win_y + 45), "MCP STATUS: ● ACTIVE", font=font_badge, fill=ACCENT_GREEN)
    draw.text((win_x + 220, win_y + 45), "TRANSPORT: stdio JSON-RPC 2.0", font=font_code_small, fill=TEXT_MUTED)
    draw.text((win_x + 480, win_y + 45), "SKILL: FAZAH-Arsenal v6.5", font=font_code_small, fill=ACCENT_CYAN)
    draw.text((win_x + 720, win_y + 45), "CATALOG: 20,078 Repos (Local)", font=font_code_small, fill=ACCENT_PURPLE)

    # User Query Box
    draw.rounded_rectangle([win_x + 20, win_y + 78, win_x + win_w - 20, win_y + 120], radius=6, fill=(24, 32, 50), outline=CARD_BORDER)
    draw.text((win_x + 32, win_y + 85), "USER REQUEST:", font=font_code_small, fill=ACCENT_AMBER)
    draw.text((win_x + 32, win_y + 100), '"Build an async Telegram bot with rate limiting and web scraping capabilities"', font=font_body, fill=TEXT_WHITE)

    # Progression of 3 Tool Invocations
    prog = frame_idx / total_frames

    # Tool Call 1: Search
    call1_y = win_y + 130
    draw.rounded_rectangle([win_x + 20, call1_y, win_x + win_w - 20, call1_y + 60], radius=6, fill=(15, 23, 42), outline=ACCENT_CYAN if prog > 0.15 else CARD_BORDER)
    draw.text((win_x + 32, call1_y + 8), "STEP 1: AGENT CALLS  ▶  arsenal_search(query='telegram bot rate limit')", font=font_code, fill=ACCENT_CYAN)
    if prog > 0.25:
        draw.text((win_x + 32, call1_y + 32), "✓ Matched 4,112 tools offline in 3ms:  1. python-telegram-bot (26.8k★)   2. aiolimiter (1.4k★)", font=font_code_small, fill=ACCENT_GREEN)

    # Tool Call 2: Security Audit
    call2_y = win_y + 200
    draw.rounded_rectangle([win_x + 20, call2_y, win_x + win_w - 20, call2_y + 60], radius=6, fill=(15, 23, 42), outline=ACCENT_PURPLE if prog > 0.45 else CARD_BORDER)
    draw.text((win_x + 32, call2_y + 8), "STEP 2: AGENT CALLS  ▶  arsenal_audit(repo='python-telegram-bot/python-telegram-bot')", font=font_code, fill=ACCENT_PURPLE)
    if prog > 0.55:
        draw.text((win_x + 32, call2_y + 32), "✓ Trust Score: 98/100 · LGPL-3.0 License · AST Audit: 0 eval/exec · Clean dependencies", font=font_code_small, fill=ACCENT_GREEN)

    # Tool Call 3: Autonomous Code Delivery
    call3_y = win_y + 270
    draw.rounded_rectangle([win_x + 20, call3_y, win_x + win_w - 20, call3_y + 60], radius=6, fill=(15, 23, 42), outline=ACCENT_GREEN if prog > 0.70 else CARD_BORDER)
    draw.text((win_x + 32, call3_y + 8), "STEP 3: AGENT CALLS  ▶  arsenal_give(repo='python-telegram-bot/python-telegram-bot')", font=font_code, fill=ACCENT_GREEN)
    if prog > 0.80:
        draw.text((win_x + 32, call3_y + 32), "✓ Injected plug-and-play boilerplate into editor: from telegram.ext import ApplicationBuilder, CommandHandler", font=font_code_small, fill=ACCENT_GREEN)

    # Summary Result Badge
    if prog > 0.85:
        draw.rounded_rectangle([win_x + 20, win_y + 342, win_x + win_w - 20, win_y + 405], radius=6, fill=(16, 38, 28), outline=ACCENT_GREEN)
        draw.text((win_x + 32, win_y + 352), "🎉 AI AGENT OUTCOME: 1-Turn Zero-Hallucination Delivery", font=font_card_title, fill=ACCENT_GREEN)
        draw.text((win_x + 32, win_y + 380), "Saved 18,500 tokens ($0.11) · 0 web API calls made · Verified production code generated instantly", font=font_body, fill=TEXT_WHITE)

    draw_bottom_caption(draw, scene_data["narration"], frame_idx / total_frames)
    return img

def render_scene_antigravity(frame_idx, total_frames, scene_data):
    img, draw = create_base_canvas(4, len(SCENES))
    draw.text((70, 78), scene_data["title"], font=font_title, fill=ACCENT_PURPLE)
    draw.text((70, 118), scene_data["subtitle"], font=font_subtitle, fill=TEXT_WHITE)

    win_x, win_y, win_w, win_h = 70, 165, WIDTH - 140, 425
    draw_window(img, draw, win_x, win_y, win_w, win_h, "Google Antigravity IDE — Autonomous Agent Session")

    draw.rounded_rectangle([win_x + 25, win_y + 40, win_x + win_w - 25, win_y + 88], radius=6, fill=(24, 30, 48), outline=(45, 55, 80))
    draw.text((win_x + 38, win_y + 48), "USER PROMPT:", font=font_code_small, fill=ACCENT_AMBER)
    draw.text((win_x + 38, win_y + 65), '"Build me a high-speed async web scraper and store results in PostgreSQL"', font=font_body, fill=TEXT_WHITE)

    draw.rounded_rectangle([win_x + 25, win_y + 100, win_x + win_w - 25, win_y + 195], radius=6, fill=(15, 23, 42), outline=ACCENT_PURPLE)
    draw.text((win_x + 38, win_y + 108), "ANTIGRAVITY AGENT (Gemini 3.8 Flash):", font=font_code_small, fill=ACCENT_PURPLE)
    draw.text((win_x + 38, win_y + 130), "→ Calling tool: mcp_fazah_arsenal_give(repo='unclecode/crawl4ai')", font=font_code, fill=ACCENT_CYAN)
    draw.text((win_x + 38, win_y + 152), "→ Calling tool: mcp_fazah_arsenal_recommend(task='postgres async client')", font=font_code, fill=ACCENT_CYAN)
    draw.text((win_x + 38, win_y + 174), "✓ Resolved 2 verified libraries offline · 0 external tokens burned · 0 API delay", font=font_code_small, fill=ACCENT_GREEN)

    draw.rounded_rectangle([win_x + 25, win_y + 208, win_x + win_w - 25, win_y + 400], radius=6, fill=(10, 15, 26), outline=CARD_BORDER)
    draw.text((win_x + 38, win_y + 220), "import asyncio\nfrom crawl4ai import AsyncWebCrawler\nimport asyncpg\n\nasync def main():\n    async with AsyncWebCrawler(verbose=True) as crawler:\n        result = await crawler.arun(url='https://example.com')\n        print('Scraped clean markdown:', len(result.markdown))", font=font_code, fill=TEXT_WHITE)

    draw_bottom_caption(draw, scene_data["narration"], frame_idx / total_frames)
    return img

def render_scene_deepseek(frame_idx, total_frames, scene_data):
    img, draw = create_base_canvas(5, len(SCENES))
    draw.text((70, 78), scene_data["title"], font=font_title, fill=ACCENT_CYAN)
    draw.text((70, 118), scene_data["subtitle"], font=font_subtitle, fill=TEXT_WHITE)

    win_x, win_y, win_w, win_h = 70, 165, WIDTH - 140, 425
    draw_window(img, draw, win_x, win_y, win_w, win_h, "DeepSeek-V3 / DeepSeek-R1 / Claude / GPT-4o — Universal MCP Host")

    mx, my, mw, mh = win_x + 20, win_y + 40, 370, 360
    draw.rounded_rectangle([mx, my, mx + mw, my + mh], radius=8, fill=(15, 23, 42), outline=CARD_BORDER)
    draw.text((mx + 18, my + 15), "Supported AI Models", font=font_card_title, fill=TEXT_WHITE)
    
    models = [
        ("DeepSeek V3 & R1", "via Cline, Roo, Continue, or DeepSeek API", ACCENT_CYAN),
        ("Claude 3.5 & 3.7", "via Claude Desktop or Claude Code CLI", ACCENT_PURPLE),
        ("Cursor & Windsurf", "via native agent IDE tool calling", ACCENT_GREEN),
        ("Google Antigravity", "via native antigravity MCP skill", ACCENT_AMBER),
        ("OpenAI GPT-4o", "via any MCP-compatible client / wrapper", TEXT_WHITE),
    ]
    for i, (mtitle, msub, col) in enumerate(models):
        y = my + 52 + i * 58
        draw.text((mx + 18, y), f"● {mtitle}", font=font_badge, fill=col)
        draw.text((mx + 32, y + 22), msub, font=font_code_small, fill=TEXT_MUTED)

    rx, ry, rw, rh = win_x + 410, win_y + 40, win_w - 430, 360
    draw.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=8, fill=(15, 23, 42), outline=CARD_BORDER)
    draw.text((rx + 18, ry + 15), "18 Native MCP Tools Granted to DeepSeek", font=font_card_title, fill=ACCENT_GREEN)

    tools = [
        ("arsenal_search", "Full-text search 20k repos offline"),
        ("arsenal_give", "Delivers verified code snippet in 1 call"),
        ("arsenal_recommend", "Understands Arabic & English intent"),
        ("arsenal_audit", "AST static analysis for repo security"),
        ("arsenal_stack", "Scaffolds complete stacks (e.g. FastAPI+PG)"),
        ("arsenal_learn", "Records package failures into memory"),
        ("arsenal_memory", "Returns known mistakes to prevent errors"),
        ("arsenal_savings", "Reports token and budget savings stats"),
    ]
    for i, (tname, tdesc) in enumerate(tools):
        ty = ry + 52 + i * 36
        draw.text((rx + 18, ty), f"⚡ {tname}", font=font_code, fill=ACCENT_CYAN)
        draw.text((rx + 220, ty + 1), tdesc, font=font_code_small, fill=TEXT_MUTED)

    draw_bottom_caption(draw, scene_data["narration"], frame_idx / total_frames)
    return img

def render_scene_savings(frame_idx, total_frames, scene_data):
    img, draw = create_base_canvas(6, len(SCENES))
    draw.text((70, 78), scene_data["title"], font=font_title, fill=ACCENT_AMBER)
    draw.text((70, 118), scene_data["subtitle"], font=font_subtitle, fill=TEXT_WHITE)

    win_x, win_y, win_w, win_h = 70, 165, WIDTH - 140, 425
    draw_window(img, draw, win_x, win_y, win_w, win_h, "terminal — fazah savings")

    draw.text((win_x + 25, win_y + 40), "$ fazah savings", font=font_code_large, fill=ACCENT_CYAN)

    kpis = [
        ("320,000", "Tokens Saved", ACCENT_GREEN),
        ("$1.90 USD", "Direct Cost Spared", ACCENT_CYAN),
        ("51 Calls", "Web Calls Avoided", ACCENT_AMBER),
        ("~1.0 Hour", "Dev Time Rescued", ACCENT_PURPLE),
    ]
    kw = (win_w - 70) // 4
    for i, (val, label, col) in enumerate(kpis):
        kx = win_x + 25 + i * (kw + 10)
        ky = win_y + 70
        draw.rounded_rectangle([kx, ky, kx + kw, ky + 70], radius=8, fill=(20, 29, 48), outline=CARD_BORDER)
        draw.text((kx + 16, ky + 12), val, font=font_card_title, fill=col)
        draw.text((kx + 16, ky + 42), label, font=font_code_small, fill=TEXT_MUTED)

    ty = win_y + 160
    draw.text((win_x + 25, ty), "SAVINGS BREAKDOWN BY CATEGORY:", font=font_code_large, fill=TEXT_WHITE)
    
    categories = [
        ("Offline Catalog Searches", "30 searches", "105,000 tokens", "$0.61 USD"),
        ("1-Call Code Delivery", "8 deliveries", "100,000 tokens", "$0.61 USD"),
        ("AST Security Scans", "10 audits", "80,000 tokens", "$0.49 USD"),
        ("Self-Healing Error Fixes", "2 retries spared", "20,000 tokens", "$0.12 USD"),
        ("Stack Scaffolds Generated", "1 full stack", "15,000 tokens", "$0.09 USD"),
    ]
    for i, (cname, ccount, ctokens, cusd) in enumerate(categories):
        cy = ty + 30 + i * 36
        draw.text((win_x + 30, cy), f"• {cname:<30}", font=font_code, fill=TEXT_MUTED)
        draw.text((win_x + 380, cy), ccount, font=font_code, fill=ACCENT_CYAN)
        draw.text((win_x + 580, cy), ctokens, font=font_code, fill=ACCENT_GREEN)
        draw.text((win_x + 780, cy), cusd, font=font_code, fill=ACCENT_AMBER)
        draw.line([(win_x + 25, cy + 26), (win_x + win_w - 25, cy + 26)], fill=(20, 26, 40), width=1)

    draw_bottom_caption(draw, scene_data["narration"], frame_idx / total_frames)
    return img

def render_scene_memory(frame_idx, total_frames, scene_data):
    img, draw = create_base_canvas(7, len(SCENES))
    draw.text((70, 78), scene_data["title"], font=font_title, fill=ACCENT_RED)
    draw.text((70, 118), scene_data["subtitle"], font=font_subtitle, fill=TEXT_WHITE)

    win_x, win_y, win_w, win_h = 70, 165, WIDTH - 140, 425
    draw_window(img, draw, win_x, win_y, win_w, win_h, "terminal — fazah memory mistakes")

    draw.text((win_x + 25, win_y + 40), "$ fazah memory mistakes", font=font_code_large, fill=ACCENT_CYAN)
    draw.text((win_x + 25, win_y + 68), "Reading local learned agent mistakes database (~/.fazah_memory.json)...", font=font_code, fill=TEXT_MUTED)

    m1_y = win_y + 105
    draw.rounded_rectangle([win_x + 25, m1_y, win_x + win_w - 25, m1_y + 115], radius=8, fill=(28, 20, 25), outline=ACCENT_RED, width=1)
    draw.text((win_x + 35, m1_y + 12), "⚠ LESSON #1: WEB SCRAPING SPIDER TASK", font=font_badge, fill=ACCENT_RED)
    draw.text((win_x + 35, m1_y + 38), "FAILED PACKAGE:      beautifulsoup4 + requests (Blocked by Cloudflare JS challenge)", font=font_code, fill=TEXT_MUTED)
    draw.text((win_x + 35, m1_y + 62), "RECOMMENDED FIX:     unclecode/crawl4ai (Async, headless, bypasses bot detection)", font=font_code, fill=ACCENT_GREEN)
    draw.text((win_x + 35, m1_y + 86), "AUTOMATIC HEALING:   Future AI queries automatically receive crawl4ai first", font=font_code_small, fill=ACCENT_CYAN)

    m2_y = win_y + 240
    draw.rounded_rectangle([win_x + 25, m2_y, win_x + win_w - 25, m2_y + 115], radius=8, fill=(28, 20, 25), outline=ACCENT_RED, width=1)
    draw.text((win_x + 35, m2_y + 12), "⚠ LESSON #2: POSTGRESQL ASYNC CLIENT", font=font_badge, fill=ACCENT_RED)
    draw.text((win_x + 35, m2_y + 38), "FAILED PACKAGE:      psycopg2 (Synchronous blocking driver inside FastAPI async loop)", font=font_code, fill=TEXT_MUTED)
    draw.text((win_x + 35, m2_y + 62), "RECOMMENDED FIX:     asyncpg (Pure async driver with 5x higher throughput)", font=font_code, fill=ACCENT_GREEN)
    draw.text((win_x + 35, m2_y + 86), "AUTOMATIC HEALING:   Injected into scaffold stack generator", font=font_code_small, fill=ACCENT_CYAN)

    draw_bottom_caption(draw, scene_data["narration"], frame_idx / total_frames)
    return img

def render_scene_finish(frame_idx, total_frames, scene_data):
    img, draw = create_base_canvas(8, len(SCENES))
    draw.text((WIDTH // 2 - 270, 95), scene_data["title"], font=font_title, fill=ACCENT_CYAN)
    draw.text((WIDTH // 2 - 240, 140), scene_data["subtitle"], font=font_subtitle, fill=TEXT_WHITE)

    cards = [
        ("GitHub Repository", "github.com/fazah-arsenal/github-ai-arsenal", "⭐ Star on GitHub", ACCENT_CYAN),
        ("Python PyPI Package", "pip install fazah-arsenal", "v6.5.0 GA Live", ACCENT_GREEN),
        ("Docker Hub Container", "docker run fazaharsenal/fazah-arsenal", "Official Image Ready", ACCENT_PURPLE),
    ]
    cw = (WIDTH - 220) // 3
    for i, (ctitle, ccmd, cbadge, col) in enumerate(cards):
        cx = 70 + i * (cw + 40)
        cy = 205
        draw.rounded_rectangle([cx, cy, cx + cw, cy + 185], radius=12, fill=CARD_BG, outline=CARD_BORDER, width=1)
        draw.text((cx + 20, cy + 20), ctitle, font=font_card_title, fill=col)
        draw.text((cx + 20, cy + 62), ccmd, font=font_code_small, fill=TEXT_WHITE)
        draw.rounded_rectangle([cx + 20, cy + 115, cx + cw - 20, cy + 155], radius=6, fill=(15, 23, 42), outline=col, width=1)
        draw.text((cx + 36, cy + 125), cbadge, font=font_badge, fill=col)

    bx, by, bw, bh = 70, 420, WIDTH - 140, 140
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=12, fill=(15, 23, 42), outline=ACCENT_CYAN, width=1)
    draw.text((bx + 30, by + 25), "Ready to supercharge your AI Coding Agent?", font=font_card_title, fill=TEXT_WHITE)
    draw.text((bx + 30, by + 68), "Run  'pip install fazah-arsenal && fazah link'  to connect all your environments instantly.", font=font_body, fill=ACCENT_GREEN)

    draw_bottom_caption(draw, scene_data["narration"], frame_idx / total_frames)
    return img

RENDERERS = {
    "intro": render_scene_intro,
    "install": render_scene_install,
    "link": render_scene_link,
    "mcp_live": render_scene_mcp_live,
    "antigravity": render_scene_antigravity,
    "deepseek": render_scene_deepseek,
    "savings": render_scene_savings,
    "memory": render_scene_memory,
    "finish": render_scene_finish,
}

async def build_narrated_walkthrough():
    temp_dir = Path("temp_media_build")
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    output_mp4 = Path("assets/demo_walkthrough.mp4")
    output_mp4.parent.mkdir(parents=True, exist_ok=True)
    
    temp_raw_video = temp_dir / "raw_video.mp4"
    master_audio = temp_dir / "master_audio.mp3"
    concat_list = temp_dir / "concat_list.txt"

    print("═══════════════════════════════════════════════════════════════════")
    print("🎬 FAZAH AI ARSENAL v6.5 — STUDIO VIDEO WALKTHROUGH PIPELINE")
    print("═══════════════════════════════════════════════════════════════════")

    # 1. Generate Voiceover
    tracks = await generate_speech_tracks(temp_dir)

    # 2. Concat all audio files
    with open(concat_list, "w", encoding="utf-8") as f:
        for t in tracks:
            f.write(f"file '{t['audio_path'].resolve().as_posix()}'\n")

    print("\n🎵 Concatenating master audio track...")
    subprocess.run([
        FFMPEG, "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy", str(master_audio)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    total_video_frames = sum(t["frames"] for t in tracks)
    print(f"📹 Total Video Frames to Render: {total_video_frames} ({total_video_frames / FPS:.2f} seconds)")

    # 3. Render Video Frames
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(temp_raw_video), fourcc, FPS, (WIDTH, HEIGHT))

    current_frame = 0
    t0 = time.time()
    for t in tracks:
        sid = t["scene"]["id"]
        renderer = RENDERERS[sid]
        scene_frames = t["frames"]
        print(f"🎨 Rendering visual scene: [{t['scene']['step_name']}] ({scene_frames} frames)...")
        
        for f in range(scene_frames):
            pil_img = renderer(f, scene_frames, t["scene"])
            bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            writer.write(bgr)
            current_frame += 1

    writer.release()
    render_time = time.time() - t0
    print(f"✓ Video frames rendered in {render_time:.2f}s!")

    # 4. Mux Video + Audio with FFmpeg
    print(f"\n⚡ Muxing high-definition video and audio with FFmpeg into: {output_mp4}...")
    subprocess.run([
        FFMPEG, "-y",
        "-i", str(temp_raw_video),
        "-i", str(master_audio),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(output_mp4)
    ], check=True)

    # 5. Clean up temporary files
    try:
        shutil.rmtree(temp_dir)
    except Exception:
        pass

    final_size_mb = output_mp4.stat().st_size / (1024 * 1024)
    print(f"\n🎉 SUCCESS: Walkthrough video generated successfully!")
    print(f"   File: {output_mp4} ({final_size_mb:.2f} MB)")
    print("═══════════════════════════════════════════════════════════════════")

if __name__ == "__main__":
    asyncio.run(build_narrated_walkthrough())
