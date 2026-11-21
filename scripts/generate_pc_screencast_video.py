"""
FAZAH AI Arsenal v6.5 — Realistic PC Screencast Walkthrough Generator
Simulates a real Windows PC Desktop workflow:
1. Windows Desktop with Taskbar, System Tray & Desktop Icons
2. User opens Command Prompt (CMD)
3. User installs FAZAH: pip install fazah-arsenal
4. User runs auto-link: fazah link (green checkmarks for all clients)
5. User launches Google Antigravity IDE
6. In Antigravity Agent Chat: User asks "Is FAZAH AI Arsenal linked to you?"
7. Antigravity Agent responds: "Yes! Connected via MCP with 18 native tools"
8. User asks Antigravity to build async web scraper + postgres
9. Antigravity invokes FAZAH MCP tools and delivers verified code in 1 call
10. User opens CMD side-by-side and runs fazah savings to see saved quota
11. Generates both:
    - assets/demo_walkthrough.mp4 (Full HD 720p with studio audio)
    - assets/demo_preview.gif (Smooth animated GIF preview for GitHub README)
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
font_title = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 26)
font_subtitle = ImageFont.truetype(os.path.join(FONT_DIR, "segoeui.ttf"), 16)
font_header = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 18)
font_card = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 15)
font_body = ImageFont.truetype(os.path.join(FONT_DIR, "segoeui.ttf"), 15)
font_body_bold = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 15)
font_caption = ImageFont.truetype(os.path.join(FONT_DIR, "segoeui.ttf"), 15)

font_code_large = ImageFont.truetype(os.path.join(FONT_DIR, "consolab.ttf"), 16)
font_code = ImageFont.truetype(os.path.join(FONT_DIR, "consola.ttf"), 14)
font_code_small = ImageFont.truetype(os.path.join(FONT_DIR, "consola.ttf"), 12)

# Colors
DESKTOP_BG = (13, 20, 36)
TASKBAR_BG = (18, 24, 38)
TASKBAR_BORDER = (35, 45, 65)

CMD_BG = (12, 12, 14)
CMD_HEADER = (30, 30, 35)
CMD_BORDER = (50, 50, 60)

IDE_BG = (17, 24, 39)
IDE_SIDEBAR = (13, 18, 30)
IDE_HEADER = (24, 32, 50)
IDE_BORDER = (37, 47, 66)
CARD_BORDER = (35, 45, 65)

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
        "id": "desktop_open_cmd",
        "title": "Windows PC Desktop — Launching Terminal",
        "narration": "Welcome to this live demonstration of FAZAH AI Arsenal on Windows. We start right from our PC desktop and open the Command Prompt to set up the arsenal."
    },
    {
        "id": "install_and_link",
        "title": "Command Prompt — pip install & fazah link",
        "narration": "In the terminal, we install FAZAH by running 'pip install fazah-arsenal'. Then, we execute 'fazah link'. Notice how FAZAH immediately scans the system and auto-configures every MCP client—including Google Antigravity, Cursor, and Claude Desktop, with zero manual JSON editing."
    },
    {
        "id": "open_antigravity",
        "title": "Launching Google Antigravity IDE",
        "narration": "Now, let's open Google Antigravity from our taskbar. The IDE loads our workspace, and we open the AI agent chat pane to verify the connection."
    },
    {
        "id": "antigravity_check",
        "title": "Agent Chat: Verifying FAZAH Tool Connection",
        "narration": "We ask Antigravity: Is FAZAH AI Arsenal connected to you? The AI agent inspects its MCP server registry and confirms: Yes! FAZAH AI Arsenal is connected, granting 18 active native tools with instant access to over 20,000 repositories."
    },
    {
        "id": "antigravity_build",
        "title": "Agent In Action: 1-Call Code Delivery",
        "narration": "Next, we give Antigravity a real engineering task: Build an async web scraper and store results in PostgreSQL. Watch how the agent works with the skill. It calls arsenal_give and arsenal_recommend, resolving verified libraries and writing production-ready code in a single turn without wasting tokens."
    },
    {
        "id": "check_savings",
        "title": "Terminal: Checking Token & Budget Savings",
        "narration": "Finally, we switch back to our terminal and run 'fazah savings'. We can see over 320,000 tokens saved, 51 external API calls avoided, and nearly two dollars spared. FAZAH AI Arsenal empowers your AI agents while protecting your quota. Star the project on GitHub to get started!"
    }
]

def draw_mouse_cursor(draw, x, y):
    """Draws a crisp white Windows arrow cursor with black outline."""
    points = [
        (x, y),
        (x, y + 16),
        (x + 4, y + 12),
        (x + 8, y + 18),
        (x + 11, y + 16),
        (x + 7, y + 11),
        (x + 12, y + 11)
    ]
    draw.polygon(points, fill=(255, 255, 255), outline=(0, 0, 0))

def draw_windows_taskbar(draw, active_app="cmd", clock_str="14:25"):
    ty = HEIGHT - 46
    # Taskbar body
    draw.rectangle([0, ty, WIDTH, HEIGHT], fill=TASKBAR_BG)
    draw.line([(0, ty), (WIDTH, ty)], fill=TASKBAR_BORDER, width=1)
    
    # Start button (Windows 11 center-left)
    cx = 560
    # 4 squares Windows logo
    draw.rectangle([cx, ty + 14, cx + 7, ty + 21], fill=ACCENT_CYAN)
    draw.rectangle([cx + 9, ty + 14, cx + 16, ty + 21], fill=ACCENT_CYAN)
    draw.rectangle([cx, ty + 23, cx + 7, ty + 30], fill=ACCENT_CYAN)
    draw.rectangle([cx + 9, ty + 23, cx + 16, ty + 30], fill=ACCENT_CYAN)

    # Search Bar
    draw.rounded_rectangle([cx + 28, ty + 10, cx + 160, ty + 36], radius=13, fill=(26, 34, 52), outline=TASKBAR_BORDER)
    draw.text((cx + 42, ty + 14), "Search apps, web...", font=font_code_small, fill=TEXT_MUTED)

    # App Icon 1: CMD
    cmd_x = cx + 175
    draw.rounded_rectangle([cmd_x, ty + 8, cmd_x + 36, ty + 38], radius=6, fill=(35, 45, 68) if active_app == "cmd" else (24, 30, 46))
    draw.rectangle([cmd_x + 8, ty + 14, cmd_x + 28, ty + 30], fill=(0, 0, 0), outline=(80, 80, 90))
    draw.text((cmd_x + 10, ty + 14), ">_", font=font_code_small, fill=ACCENT_GREEN)
    if active_app == "cmd":
        draw.line([(cmd_x + 6, ty + 42), (cmd_x + 30, ty + 42)], fill=ACCENT_CYAN, width=2)

    # App Icon 2: Google Antigravity
    agy_x = cmd_x + 44
    draw.rounded_rectangle([agy_x, ty + 8, agy_x + 36, ty + 38], radius=6, fill=(35, 45, 68) if active_app == "antigravity" else (24, 30, 46))
    draw.text((agy_x + 10, ty + 12), "⚡", font=font_card, fill=ACCENT_PURPLE)
    if active_app == "antigravity":
        draw.line([(agy_x + 6, ty + 42), (agy_x + 30, ty + 42)], fill=ACCENT_PURPLE, width=2)

    # App Icon 3: VS Code
    vsc_x = agy_x + 44
    draw.rounded_rectangle([vsc_x, ty + 8, vsc_x + 36, ty + 38], radius=6, fill=(24, 30, 46))
    draw.text((vsc_x + 11, ty + 12), "∞", font=font_card, fill=ACCENT_CYAN)

    # System Tray & Clock
    draw.text((WIDTH - 150, ty + 14), "ENG · 🗲 · 🛈", font=font_code_small, fill=TEXT_MUTED)
    draw.text((WIDTH - 65, ty + 14), clock_str, font=font_code_small, fill=TEXT_WHITE)

def draw_desktop_icons(draw):
    icons = [
        ("This PC", "🖥️"),
        ("Terminal", "⌨️"),
        ("Antigravity", "⚡"),
        ("Projects", "📁"),
        ("Recycle Bin", "🗑️"),
    ]
    for i, (name, emoji) in enumerate(icons):
        iy = 30 + i * 85
        draw.text((36, iy), emoji, font=font_header, fill=TEXT_WHITE)
        draw.text((22, iy + 28), name, font=font_code_small, fill=TEXT_WHITE)

def draw_caption_banner(draw, text, progress):
    bar_h = 54
    bar_y = HEIGHT - 46 - bar_h - 10
    draw.rounded_rectangle([50, bar_y, WIDTH - 50, bar_y + bar_h], radius=10, fill=(10, 15, 26), outline=(40, 50, 75), width=1)
    
    # soundwave
    cx = 70
    cy = bar_y + 27
    for i in range(7):
        phase = (progress * 15 + i) % 3.14
        h = int(18 * (0.5 + 0.5 * np.sin(phase)))
        draw.line([(cx + i * 5, cy - h // 2), (cx + i * 5, cy + h // 2)], fill=ACCENT_CYAN, width=2)

    draw.text((115, bar_y + 16), text[:130] + ("..." if len(text) > 130 else ""), font=font_caption, fill=TEXT_WHITE)

def get_audio_duration(audio_path):
    cmd = [FFMPEG, "-i", str(audio_path)]
    proc = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, errors="ignore")
    for line in proc.stderr.splitlines():
        if "Duration:" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
            h, m, s = float(parts[0]), float(parts[1]), float(parts[2])
            return h * 3600 + m * 60 + s
    return 12.0

async def generate_speech_tracks(temp_dir: Path):
    temp_dir.mkdir(parents=True, exist_ok=True)
    voice = "en-US-GuyNeural"
    tracks = []
    for idx, sc in enumerate(SCENES):
        mp3_path = temp_dir / f"scene_{idx:02d}.mp3"
        print(f"🎙️ Recording narration for [{sc['title']}]...")
        communicate = edge_tts.Communicate(sc["narration"], voice=voice)
        await communicate.save(str(mp3_path))
        dur = get_audio_duration(mp3_path)
        tracks.append({
            "index": idx,
            "scene": sc,
            "audio_path": mp3_path,
            "duration": dur,
            "frames": int(dur * FPS) + 15
        })
        print(f"   -> {dur:.2f}s ({tracks[-1]['frames']} frames)")
    return tracks

# ----------------- FRAME RENDERERS -----------------

def render_desktop_open_cmd(frame, total, scene):
    img = Image.new("RGB", (WIDTH, HEIGHT), DESKTOP_BG)
    draw = ImageDraw.Draw(img)
    # Wallpaper gradient & subtle grid
    for y in range(0, HEIGHT - 46, 4):
        draw.line([(0, y), (WIDTH, y)], fill=(13 + (y // 40), 20 + (y // 35), 36 + (y // 30)))
    draw_desktop_icons(draw)
    draw_windows_taskbar(draw, active_app="cmd")

    # Mouse animation moving towards center to open CMD
    prog = frame / total
    mx = int(200 + prog * 440)
    my = int(400 - prog * 150)
    
    # CMD Window popping up
    if prog > 0.35:
        # Window
        wx, wy, ww, wh = 180, 100, 920, 480
        draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=8, fill=CMD_BG, outline=CMD_BORDER, width=1)
        draw.rectangle([wx, wy, wx + ww, wy + 32], fill=CMD_HEADER)
        draw.text((wx + 15, wy + 7), "Command Prompt — Administrator", font=font_code_small, fill=TEXT_MUTED)
        # Windows window buttons
        draw.text((wx + ww - 65, wy + 6), "—  □  ✕", font=font_code_small, fill=TEXT_MUTED)

        # Terminal content
        draw.text((wx + 20, wy + 45), "Microsoft Windows [Version 10.0.22631.4460]", font=font_code, fill=TEXT_MUTED)
        draw.text((wx + 20, wy + 68), "(c) Microsoft Corporation. All rights reserved.", font=font_code, fill=TEXT_MUTED)
        draw.text((wx + 20, wy + 110), "C:\\Users\\Developer> ", font=font_code, fill=TEXT_WHITE)
        
        # Cursor blink
        if (frame // 10) % 2 == 0:
            draw.text((wx + 205, wy + 110), "_", font=font_code, fill=ACCENT_GREEN)

    draw_mouse_cursor(draw, mx, my)
    draw_caption_banner(draw, scene["narration"], prog)
    return img

def render_install_and_link(frame, total, scene):
    img = Image.new("RGB", (WIDTH, HEIGHT), DESKTOP_BG)
    draw = ImageDraw.Draw(img)
    draw_desktop_icons(draw)
    draw_windows_taskbar(draw, active_app="cmd")

    wx, wy, ww, wh = 140, 60, 1000, 530
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=8, fill=CMD_BG, outline=CMD_BORDER, width=1)
    draw.rectangle([wx, wy, wx + ww, wy + 32], fill=CMD_HEADER)
    draw.text((wx + 15, wy + 7), "Command Prompt — Administrator (FAZAH AI Arsenal Setup)", font=font_code_small, fill=TEXT_MUTED)
    draw.text((wx + ww - 65, wy + 6), "—  □  ✕", font=font_code_small, fill=TEXT_MUTED)

    prog = frame / total
    lines = [
        ("C:\\Users\\Developer> pip install fazah-arsenal", TEXT_WHITE, 0.05),
        ("Collecting fazah-arsenal (v6.5.0)", TEXT_MUTED, 0.12),
        ("  Downloading fazah_arsenal-6.5.0-py3-none-any.whl (4.6 MB)", TEXT_MUTED, 0.18),
        ("Successfully installed fazah-arsenal-6.5.0", ACCENT_GREEN, 0.25),
        ("", TEXT_MUTED, 0.28),
        ("C:\\Users\\Developer> fazah link", ACCENT_CYAN, 0.35),
        ("╔═══════════════════════════════════════════════════════════════════════════════════════╗", ACCENT_PURPLE, 0.40),
        ("║  FAZAH AI ARSENAL v6.5  ·  Zero-Touch MCP Auto-Link Engine                           ║", ACCENT_PURPLE, 0.42),
        ("╠═══════════════════════════════════════════════════════════════════════════════════════╣", ACCENT_PURPLE, 0.44),
        ("║  ✓ Google Antigravity:   .gemini/antigravity/mcp_config.json          [LINKED]       ║", ACCENT_GREEN, 0.50),
        ("║  ✓ Cursor IDE:           .cursor/mcp.json                             [LINKED]       ║", ACCENT_GREEN, 0.58),
        ("║  ✓ Claude Desktop:       AppData/Roaming/Claude/claude_desktop...     [LINKED]       ║", ACCENT_GREEN, 0.66),
        ("║  ✓ Windsurf:             .codeium/windsurf/mcp_config.json            [LINKED]       ║", ACCENT_GREEN, 0.74),
        ("║  ✓ VS Code Cline & Roo:  globalStorage/mcp_settings.json              [LINKED]       ║", ACCENT_GREEN, 0.82),
        ("║  ✓ Workspace:            ./.mcp.json                                  [LINKED]       ║", ACCENT_GREEN, 0.88),
        ("╚═══════════════════════════════════════════════════════════════════════════════════════╝", ACCENT_PURPLE, 0.90),
        ("✨ 18 Native MCP Tools & 20,078 Curated Repositories Ready Across All Editors!", ACCENT_CYAN, 0.95),
    ]

    curr_y = wy + 45
    for txt, col, thresh in lines:
        if prog >= thresh:
            draw.text((wx + 20, curr_y), txt, font=font_code, fill=col)
        curr_y += 24

    draw_caption_banner(draw, scene["narration"], prog)
    return img

def render_open_antigravity(frame, total, scene):
    img = Image.new("RGB", (WIDTH, HEIGHT), DESKTOP_BG)
    draw = ImageDraw.Draw(img)
    draw_desktop_icons(draw)

    prog = frame / total
    draw_windows_taskbar(draw, active_app="antigravity" if prog > 0.4 else "cmd")

    # Antigravity Window Expanding / Opening
    scale = min(1.0, 0.3 + prog * 1.2)
    ww = int(1120 * scale)
    wh = int(540 * scale)
    wx = (WIDTH - ww) // 2
    wy = 40 + (540 - wh) // 2

    # Draw Antigravity IDE UI
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=8, fill=IDE_BG, outline=IDE_BORDER, width=1)
    draw.rectangle([wx, wy, wx + ww, wy + 36], fill=IDE_HEADER)
    draw.text((wx + 15, wy + 8), "Google Antigravity IDE — [Workspace: FAZAH-Arsenal] — Gemini 3.8 Flash", font=font_code_small, fill=TEXT_WHITE)
    draw.text((wx + ww - 65, wy + 8), "—  □  ✕", font=font_code_small, fill=TEXT_MUTED)

    if scale > 0.8:
        # Sidebar
        draw.rectangle([wx, wy + 36, wx + 180, wy + wh], fill=IDE_SIDEBAR)
        draw.text((wx + 16, wy + 50), "EXPLORER", font=font_code_small, fill=TEXT_MUTED)
        draw.text((wx + 16, wy + 75), "📁 scripts", font=font_code_small, fill=TEXT_WHITE)
        draw.text((wx + 26, wy + 98), "🐍 mcp_server.py", font=font_code_small, fill=ACCENT_CYAN)
        draw.text((wx + 26, wy + 120), "🐍 gh_arsenal.py", font=font_code_small, fill=ACCENT_CYAN)
        draw.text((wx + 16, wy + 145), "📁 references", font=font_code_small, fill=TEXT_WHITE)
        draw.text((wx + 26, wy + 168), "📄 mega_index.json", font=font_code_small, fill=TEXT_MUTED)
        draw.text((wx + 16, wy + 195), "⚙ .mcp.json", font=font_code_small, fill=ACCENT_AMBER)

        # Center Editor Tab
        draw.rectangle([wx + 180, wy + 36, wx + 620, wy + 68], fill=(22, 30, 48))
        draw.text((wx + 195, wy + 44), "main.py ✕", font=font_code_small, fill=TEXT_WHITE)
        draw.text((wx + 200, wy + 85), "# FAZAH AI Agent Workspace\nimport asyncio\n\n# Ready to build with native MCP tools...", font=font_code, fill=TEXT_MUTED)

        # Right Side: Agent Chat Pane
        draw.rectangle([wx + 620, wy + 36, wx + ww, wy + wh], fill=(15, 20, 34))
        draw.line([(wx + 620, wy + 36), (wx + 620, wy + wh)], fill=IDE_BORDER, width=1)
        draw.text((wx + 635, wy + 45), "AGENT CHAT · Gemini 3.8 Flash", font=font_card, fill=ACCENT_PURPLE)
        draw.text((wx + 635, wy + 68), "MCP Status: fazah-arsenal connected", font=font_code_small, fill=ACCENT_GREEN)

    # Mouse animation clicking into Antigravity
    mx = int(680 - (1.0 - prog) * 200)
    my = int(250 + (1.0 - prog) * 150)
    draw_mouse_cursor(draw, mx, my)

    draw_caption_banner(draw, scene["narration"], prog)
    return img

def render_antigravity_check(frame, total, scene):
    img = Image.new("RGB", (WIDTH, HEIGHT), DESKTOP_BG)
    draw = ImageDraw.Draw(img)
    draw_desktop_icons(draw)
    draw_windows_taskbar(draw, active_app="antigravity")

    wx, wy, ww, wh = 70, 40, 1140, 540
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=8, fill=IDE_BG, outline=IDE_BORDER, width=1)
    draw.rectangle([wx, wy, wx + ww, wy + 36], fill=IDE_HEADER)
    draw.text((wx + 15, wy + 8), "Google Antigravity IDE — Agent Verification Session", font=font_code_small, fill=TEXT_WHITE)
    draw.text((wx + ww - 65, wy + 8), "—  □  ✕", font=font_code_small, fill=TEXT_MUTED)

    # Sidebar (left)
    draw.rectangle([wx, wy + 36, wx + 180, wy + wh], fill=IDE_SIDEBAR)
    draw.text((wx + 16, wy + 50), "EXPLORER", font=font_code_small, fill=TEXT_MUTED)
    draw.text((wx + 16, wy + 75), "📁 fazah_arsenal", font=font_code_small, fill=TEXT_WHITE)
    draw.text((wx + 26, wy + 98), "⚙ .mcp.json [✓]", font=font_code_small, fill=ACCENT_GREEN)

    # Chat Pane (full center-right)
    cx = wx + 180
    cw = ww - 180
    draw.rectangle([cx, wy + 36, wx + ww, wy + wh], fill=(14, 19, 32))

    prog = frame / total

    # 1. User Message bubble
    if prog > 0.10:
        draw.rounded_rectangle([cx + 30, wy + 55, cx + cw - 30, wy + 115], radius=8, fill=(24, 32, 52), outline=CARD_BORDER)
        draw.text((cx + 45, wy + 64), "USER:", font=font_code_small, fill=ACCENT_AMBER)
        draw.text((cx + 45, wy + 84), '"Is the FAZAH AI Arsenal tool linked to you and ready to use?"', font=font_body, fill=TEXT_WHITE)

    # 2. Antigravity Agent Tool Inspection Call
    if prog > 0.35:
        draw.rounded_rectangle([cx + 30, wy + 130, cx + cw - 30, wy + 180], radius=8, fill=(18, 25, 42), outline=ACCENT_PURPLE)
        draw.text((cx + 45, wy + 138), "ANTIGRAVITY AGENT (Gemini 3.8 Flash):", font=font_code_small, fill=ACCENT_PURPLE)
        draw.text((cx + 45, wy + 156), "▶ Checking MCP registry: list_tools()  →  Found server 'fazah-arsenal' (18 Tools active)", font=font_code, fill=ACCENT_CYAN)

    # 3. Antigravity Agent Response
    if prog > 0.60:
        draw.rounded_rectangle([cx + 30, wy + 195, cx + cw - 30, wy + 395], radius=8, fill=(16, 22, 38), outline=ACCENT_GREEN, width=1)
        draw.text((cx + 45, wy + 208), "AGENT RESPONSE:", font=font_code_small, fill=ACCENT_GREEN)
        
        reply_lines = [
            "Yes! FAZAH AI Arsenal is successfully linked and active via native MCP.",
            "",
            "Here is what I have direct offline access to:",
            "  • 20,078 Curated GitHub Repositories (searchable locally via BM25 in 3ms)",
            "  • 18 Native Tools: arsenal_search, arsenal_give, arsenal_audit, arsenal_recommend...",
            "  • AST Security Scanner: Automated static analysis for safe code imports",
            "  • Token Savings Engine: Resolving tools locally without burning your external API quota.",
            "",
            "What project would you like me to build for you today?"
        ]
        for idx, line in enumerate(reply_lines):
            draw.text((cx + 45, wy + 232 + idx * 21), line, font=font_code if idx > 1 else font_body_bold, fill=TEXT_WHITE if idx <= 2 else (ACCENT_GREEN if "•" in line else TEXT_MUTED))

    draw_caption_banner(draw, scene["narration"], prog)
    return img

def render_antigravity_build(frame, total, scene):
    img = Image.new("RGB", (WIDTH, HEIGHT), DESKTOP_BG)
    draw = ImageDraw.Draw(img)
    draw_desktop_icons(draw)
    draw_windows_taskbar(draw, active_app="antigravity")

    wx, wy, ww, wh = 70, 40, 1140, 540
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=8, fill=IDE_BG, outline=IDE_BORDER, width=1)
    draw.rectangle([wx, wy, wx + ww, wy + 36], fill=IDE_HEADER)
    draw.text((wx + 15, wy + 8), "Google Antigravity IDE — Autonomous Code Generation", font=font_code_small, fill=TEXT_WHITE)
    draw.text((wx + ww - 65, wy + 8), "—  □  ✕", font=font_code_small, fill=TEXT_MUTED)

    prog = frame / total

    # Left: Chat pane (380px)
    cx, cy, cw, ch = wx, wy + 36, 420, wh - 36
    draw.rectangle([cx, cy, cx + cw, cy + ch], fill=(14, 19, 32))
    draw.line([(cx + cw, cy), (cx + cw, cy + ch)], fill=IDE_BORDER, width=1)

    draw.rounded_rectangle([cx + 15, cy + 15, cx + cw - 15, cy + 75], radius=6, fill=(24, 32, 52))
    draw.text((cx + 25, cy + 22), "USER TASK:", font=font_code_small, fill=ACCENT_AMBER)
    draw.text((cx + 25, cy + 40), '"Build me an async web scraper\nand store results in PostgreSQL"', font=font_code_small, fill=TEXT_WHITE)

    if prog > 0.20:
        draw.rounded_rectangle([cx + 15, cy + 90, cx + cw - 15, cy + 175], radius=6, fill=(18, 25, 42), outline=ACCENT_CYAN)
        draw.text((cx + 25, cy + 98), "ANTIGRAVITY TOOL CALLS:", font=font_code_small, fill=ACCENT_CYAN)
        draw.text((cx + 25, cy + 118), "1. arsenal_give('unclecode/crawl4ai')", font=font_code_small, fill=ACCENT_GREEN)
        draw.text((cx + 25, cy + 136), "2. arsenal_recommend('postgres async')", font=font_code_small, fill=ACCENT_GREEN)
        draw.text((cx + 25, cy + 154), "✓ Offline AST checked: 0 vulnerabilities", font=font_code_small, fill=TEXT_MUTED)

    if prog > 0.40:
        draw.rounded_rectangle([cx + 15, cy + 190, cx + cw - 15, cy + 290], radius=6, fill=(16, 35, 26), outline=ACCENT_GREEN)
        draw.text((cx + 25, cy + 198), "AGENT OUTCOME:", font=font_code_small, fill=ACCENT_GREEN)
        draw.text((cx + 25, cy + 220), "• Crawl4AI + asyncpg selected", font=font_code_small, fill=TEXT_WHITE)
        draw.text((cx + 25, cy + 240), "• Injected code into scraper.py", font=font_code_small, fill=TEXT_WHITE)
        draw.text((cx + 25, cy + 260), "• 0 tokens wasted on web search", font=font_code_small, fill=ACCENT_CYAN)

    # Right: Code Editor showing generated scraper.py
    ex, ey, ew, eh = cx + cw, cy, ww - cw, ch
    draw.rectangle([ex, ey, wx + ww, ey + eh], fill=(10, 15, 26))
    draw.rectangle([ex, ey, ex + 200, ey + 32], fill=(18, 25, 42))
    draw.text((ex + 18, ey + 8), "scraper.py [Generated] ✕", font=font_code_small, fill=ACCENT_CYAN)

    code_text = """import asyncio
from crawl4ai import AsyncWebCrawler
import asyncpg

async def scrape_and_store(target_url: str):
    print(f"[*] Crawling: {target_url}")
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url=target_url)
        content_markdown = result.markdown

    # Store cleanly in PostgreSQL via asyncpg
    conn = await asyncpg.connect("postgresql://user:pass@localhost/arsenal_db")
    await conn.execute(
        "INSERT INTO scraped_pages(url, content) VALUES($1, $2)",
        target_url, content_markdown
    )
    await conn.close()
    print("[✓] Saved to PostgreSQL successfully!")

if __name__ == "__main__":
    asyncio.run(scrape_and_store("https://news.ycombinator.com"))"""

    lines = code_text.splitlines()
    visible_lines = min(len(lines), int((prog - 0.25) * 35)) if prog > 0.25 else 0
    for idx in range(visible_lines):
        draw.text((ex + 25, ey + 45 + idx * 20), lines[idx], font=font_code, fill=TEXT_WHITE if not lines[idx].strip().startswith("#") else ACCENT_GREEN)

    draw_caption_banner(draw, scene["narration"], prog)
    return img

def render_check_savings(frame, total, scene):
    img = Image.new("RGB", (WIDTH, HEIGHT), DESKTOP_BG)
    draw = ImageDraw.Draw(img)
    draw_desktop_icons(draw)
    draw_windows_taskbar(draw, active_app="cmd")

    # Side by side windows: Left Antigravity (faded), Right Terminal (active)
    # Right Terminal
    wx, wy, ww, wh = 100, 50, 1080, 520
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=8, fill=CMD_BG, outline=ACCENT_CYAN, width=1)
    draw.rectangle([wx, wy, wx + ww, wy + 32], fill=CMD_HEADER)
    draw.text((wx + 15, wy + 7), "Command Prompt — fazah savings (Live ROI Tracker)", font=font_code_small, fill=TEXT_WHITE)
    draw.text((wx + ww - 65, wy + 6), "—  □  ✕", font=font_code_small, fill=TEXT_MUTED)

    prog = frame / total
    draw.text((wx + 25, wy + 45), "C:\\Users\\Developer> fazah savings", font=font_code_large, fill=ACCENT_CYAN)

    # 4 KPI boxes
    kpis = [
        ("320,000", "Tokens Saved", ACCENT_GREEN),
        ("$1.90 USD", "Direct Cost Spared", ACCENT_CYAN),
        ("51 Calls", "Web Calls Avoided", ACCENT_AMBER),
        ("~1.0 Hour", "Dev Time Rescued", ACCENT_PURPLE),
    ]
    kw = (ww - 80) // 4
    for i, (val, label, col) in enumerate(kpis):
        kx = wx + 25 + i * (kw + 10)
        ky = wy + 75
        draw.rounded_rectangle([kx, ky, kx + kw, ky + 72], radius=8, fill=(20, 29, 48), outline=CARD_BORDER)
        draw.text((kx + 16, ky + 12), val, font=font_card, fill=col)
        draw.text((kx + 16, ky + 42), label, font=font_code_small, fill=TEXT_MUTED)

    ty = wy + 168
    draw.text((wx + 25, ty), "SAVINGS BREAKDOWN (SESSION AUDIT):", font=font_code, fill=TEXT_WHITE)
    
    categories = [
        ("Offline Catalog Searches", "30 searches", "105,000 tokens", "$0.61 USD"),
        ("1-Call Code Delivery", "8 deliveries", "100,000 tokens", "$0.61 USD"),
        ("AST Security Scans", "10 audits", "80,000 tokens", "$0.49 USD"),
        ("Self-Healing Error Fixes", "2 retries spared", "20,000 tokens", "$0.12 USD"),
        ("Stack Scaffolds Generated", "1 full stack", "15,000 tokens", "$0.09 USD"),
    ]
    for i, (cname, ccount, ctokens, cusd) in enumerate(categories):
        cy = ty + 28 + i * 35
        draw.text((wx + 30, cy), f"• {cname:<30}", font=font_code, fill=TEXT_MUTED)
        draw.text((wx + 380, cy), ccount, font=font_code, fill=ACCENT_CYAN)
        draw.text((wx + 580, cy), ctokens, font=font_code, fill=ACCENT_GREEN)
        draw.text((wx + 780, cy), cusd, font=font_code, fill=ACCENT_AMBER)
        draw.line([(wx + 25, cy + 24), (wx + ww - 25, cy + 24)], fill=(20, 26, 40), width=1)

    # Bottom Call to Action
    draw.rounded_rectangle([wx + 25, wy + 380, wx + ww - 25, wy + 460], radius=8, fill=(16, 25, 42), outline=ACCENT_GREEN)
    draw.text((wx + 40, wy + 395), "⭐ Star on GitHub: github.com/fazah-arsenal/github-ai-arsenal", font=font_card, fill=ACCENT_CYAN)
    draw.text((wx + 40, wy + 425), "📦 Install now: pip install fazah-arsenal && fazah link", font=font_body, fill=ACCENT_GREEN)

    draw_caption_banner(draw, scene["narration"], prog)
    return img

RENDERERS = {
    "desktop_open_cmd": render_desktop_open_cmd,
    "install_and_link": render_install_and_link,
    "open_antigravity": render_open_antigravity,
    "antigravity_check": render_antigravity_check,
    "antigravity_build": render_antigravity_build,
    "check_savings": render_check_savings,
}

async def build_pc_screencast():
    temp_dir = Path("temp_pc_screencast")
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    output_mp4 = Path("assets/demo_walkthrough.mp4")
    output_gif = Path("assets/demo_preview.gif")
    output_mp4.parent.mkdir(parents=True, exist_ok=True)
    
    temp_raw_video = temp_dir / "raw_video.mp4"
    master_audio = temp_dir / "master_audio.mp3"
    concat_list = temp_dir / "concat_list.txt"

    print("═══════════════════════════════════════════════════════════════════")
    print("🎬 FAZAH AI ARSENAL v6.5 — PC DESKTOP SCREENCAST PIPELINE")
    print("═══════════════════════════════════════════════════════════════════")

    # 1. Voiceover
    tracks = await generate_speech_tracks(temp_dir)

    with open(concat_list, "w", encoding="utf-8") as f:
        for t in tracks:
            f.write(f"file '{t['audio_path'].resolve().as_posix()}'\n")

    print("\n🎵 Concatenating master audio track...")
    subprocess.run([
        FFMPEG, "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy", str(master_audio)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    total_frames = sum(t["frames"] for t in tracks)
    print(f"📹 Rendering {total_frames} frames ({total_frames / FPS:.2f}s)...")

    # 2. Render Video Frames
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(temp_raw_video), fourcc, FPS, (WIDTH, HEIGHT))

    gif_frames = []
    sample_rate = 12 # sample 1 frame every 12 frames for GIF preview (~2.5 fps)

    global_frame = 0
    t0 = time.time()
    for t in tracks:
        sid = t["scene"]["id"]
        renderer = RENDERERS[sid]
        scene_frames = t["frames"]
        print(f"🎨 Rendering scene: [{t['scene']['title']}] ({scene_frames} frames)...")
        
        for f in range(scene_frames):
            pil_img = renderer(f, scene_frames, t["scene"])
            
            # Collect sample frames for the animated GIF preview
            if global_frame % sample_rate == 0 and len(gif_frames) < 120:
                # Resize to 800x450 for fast loading on GitHub README
                thumb = pil_img.resize((800, 450), Image.Resampling.LANCZOS)
                gif_frames.append(thumb)

            bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            writer.write(bgr)
            global_frame += 1

    writer.release()
    print(f"✓ Frames rendered in {time.time() - t0:.2f}s!")

    # 3. Mux Video + Audio with FFmpeg
    print(f"\n⚡ Muxing MP4 with FFmpeg into: {output_mp4}...")
    subprocess.run([
        FFMPEG, "-y",
        "-i", str(temp_raw_video),
        "-i", str(master_audio),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(output_mp4)
    ], check=True)

    # 4. Generate Animated GIF for GitHub README
    print(f"\n🎞️ Generating animated GIF preview for GitHub README into: {output_gif}...")
    if gif_frames:
        gif_frames[0].save(
            str(output_gif),
            save_all=True,
            append_images=gif_frames[1:],
            duration=int(1000 / (FPS / sample_rate)),
            loop=0,
            optimize=True
        )
        print(f"✓ GIF generated: {output_gif} ({output_gif.stat().st_size / (1024*1024):.2f} MB)")

    # 5. Clean temp
    try:
        shutil.rmtree(temp_dir)
    except Exception:
        pass

    mp4_sz = output_mp4.stat().st_size / (1024 * 1024)
    print(f"\n🎉 SUCCESS: All media assets ready!")
    print(f"   MP4 Video: {output_mp4} ({mp4_sz:.2f} MB)")
    print(f"   GIF Preview: {output_gif}")
    print("═══════════════════════════════════════════════════════════════════")

if __name__ == "__main__":
    asyncio.run(build_pc_screencast())
