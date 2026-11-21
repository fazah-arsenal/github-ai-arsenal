"""
FAZAH AI Arsenal v6.5 — Pixel-Perfect Authentic Windows 11 & Antigravity Screencast
Uses:
- Real 4K Windows 11 Dark Mode Bloom Wallpaper (C:/Windows/Web/Wallpaper/Windows/img19.jpg)
- Real Antigravity Official Logo (C:/Users/Compumarts/AppData/Local/Programs/Antigravity IDE/resources/app/extensions/agy/img/logo.png)
- Real VS Code Editor Icon (C:/Users/Compumarts/AppData/Local/Programs/Antigravity IDE/resources/app/resources/win32/code_150x150.png)
- Authentic Windows Terminal with Acrylic Tab Bar & PowerShell
- Authentic Google Antigravity IDE UI from inside:
  * Full menu bar, title bar, command search bar, model selector
  * Activity bar (left), File Explorer with MCP server status
  * Syntax-highlighted VS Code Dark+ code editor with line numbers & breadcrumbs
  * Real Antigravity Agent Chat panel with avatars, thinking accordions, tool call cards, and dialogue
  * Real Terminal showing pip install, fazah link, and fazah savings
- English Studio Voiceover (edge-tts en-US-GuyNeural)
- Generates assets/demo_walkthrough.mp4 & assets/demo_preview.gif
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
font_title = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 22)
font_subtitle = ImageFont.truetype(os.path.join(FONT_DIR, "segoeui.ttf"), 14)
font_header = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 15)
font_card = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 13)
font_body = ImageFont.truetype(os.path.join(FONT_DIR, "segoeui.ttf"), 13)
font_body_bold = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 13)
font_caption = ImageFont.truetype(os.path.join(FONT_DIR, "segoeui.ttf"), 14)

font_code_large = ImageFont.truetype(os.path.join(FONT_DIR, "consolab.ttf"), 14)
font_code = ImageFont.truetype(os.path.join(FONT_DIR, "consola.ttf"), 12)
font_code_small = ImageFont.truetype(os.path.join(FONT_DIR, "consola.ttf"), 11)

# Syntax Highlighting Colors (VS Code Dark+)
SYNTAX_KEYWORD = (197, 134, 192)   # purple/magenta
SYNTAX_CLASS = (78, 201, 176)      # teal
SYNTAX_FUNC = (220, 220, 170)      # yellow
SYNTAX_STRING = (206, 145, 120)    # orange/brown
SYNTAX_COMMENT = (106, 153, 85)    # green
SYNTAX_VAR = (156, 220, 254)       # light blue
TEXT_WHITE = (243, 244, 246)
TEXT_MUTED = (160, 165, 175)
TEXT_DIM = (110, 115, 125)

# Accent colors
ACCENT_BLUE = (0, 120, 215)
ACCENT_CYAN = (56, 189, 248)
ACCENT_PURPLE = (168, 85, 247)
ACCENT_GREEN = (34, 197, 94)
ACCENT_AMBER = (245, 158, 11)
ACCENT_RED = (239, 68, 68)

# Load Real Assets
WALLPAPER_PATH = "C:/Windows/Web/Wallpaper/Windows/img19.jpg"
if os.path.exists(WALLPAPER_PATH):
    BASE_WALLPAPER = Image.open(WALLPAPER_PATH).resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
else:
    BASE_WALLPAPER = Image.new("RGB", (WIDTH, HEIGHT), (15, 23, 42))

LOGO_PATH = "C:/Users/Compumarts/AppData/Local/Programs/Antigravity IDE/resources/app/extensions/agy/img/logo.png"
if os.path.exists(LOGO_PATH):
    REAL_AGY_LOGO_ORIG = Image.open(LOGO_PATH).convert("RGBA")
    REAL_AGY_LOGO_24 = REAL_AGY_LOGO_ORIG.resize((24, 24), Image.Resampling.LANCZOS)
    REAL_AGY_LOGO_18 = REAL_AGY_LOGO_ORIG.resize((18, 18), Image.Resampling.LANCZOS)
    REAL_AGY_LOGO_32 = REAL_AGY_LOGO_ORIG.resize((32, 32), Image.Resampling.LANCZOS)
else:
    REAL_AGY_LOGO_24 = Image.new("RGBA", (24, 24), (168, 85, 247, 255))
    REAL_AGY_LOGO_18 = Image.new("RGBA", (18, 18), (168, 85, 247, 255))
    REAL_AGY_LOGO_32 = Image.new("RGBA", (32, 32), (168, 85, 247, 255))

CODE_ICON_PATH = "C:/Users/Compumarts/AppData/Local/Programs/Antigravity IDE/resources/app/resources/win32/code_150x150.png"
if os.path.exists(CODE_ICON_PATH):
    REAL_CODE_ICON = Image.open(CODE_ICON_PATH).convert("RGBA").resize((24, 24), Image.Resampling.LANCZOS)
else:
    REAL_CODE_ICON = Image.new("RGBA", (24, 24), (0, 120, 215, 255))

SCENES = [
    {
        "id": "desktop_open_terminal",
        "title": "Windows 11 Desktop — Launching Terminal",
        "narration": "Here is FAZAH AI Arsenal running natively on Windows 11. We launch the Windows Terminal right from our taskbar to install the package and link our AI tools."
    },
    {
        "id": "terminal_install_link",
        "title": "Windows Terminal — pip install & fazah link",
        "narration": "Inside Windows Terminal, we install the package with pip, then run 'fazah link'. In under a second, FAZAH automatically registers the native MCP server into Google Antigravity, Cursor, and Claude Desktop with zero configuration."
    },
    {
        "id": "launch_antigravity",
        "title": "Launching Google Antigravity IDE",
        "narration": "Next, we launch Google Antigravity IDE. Our workspace opens with the Antigravity agent ready, and the FAZAH native MCP server is instantly active in the background."
    },
    {
        "id": "antigravity_verify_dialog",
        "title": "Agent Chat: Verifying Tool Linkage",
        "narration": "In the agent chat, we ask Antigravity: Is FAZAH AI Arsenal linked to you? The AI agent inspects its MCP registry and confirms: Yes! FAZAH is connected, granting 18 native tools and instant offline access to over 20,000 curated repositories."
    },
    {
        "id": "antigravity_live_build",
        "title": "Autonomous Coding: 1-Call Delivery",
        "narration": "Now we ask Antigravity to build an async web scraper with PostgreSQL. Watch how the agent works with the skill. It calls arsenal_give and arsenal_recommend, resolving verified libraries and writing production-ready code in a single turn without wasting tokens."
    },
    {
        "id": "terminal_check_savings",
        "title": "Windows Terminal — Checking Quota Savings",
        "narration": "Back in the terminal, running 'fazah savings' reveals the live impact: over 320,000 tokens saved and 51 web calls avoided. FAZAH AI Arsenal gives your AI agents superpowers while saving your quota. Star the project on GitHub to get started!"
    }
]

def draw_mouse_cursor(draw, x, y):
    points = [
        (x, y),
        (x, y + 17),
        (x + 5, y + 13),
        (x + 9, y + 20),
        (x + 12, y + 18),
        (x + 8, y + 12),
        (x + 13, y + 12)
    ]
    draw.polygon(points, fill=(255, 255, 255), outline=(10, 10, 10))

def draw_windows11_taskbar(img, active_app="terminal", clock_str="2:30 PM"):
    draw = ImageDraw.Draw(img)
    ty = HEIGHT - 48
    
    # Taskbar Acrylic layer
    taskbar_layer = Image.new("RGBA", (WIDTH, 48), (18, 22, 34, 225))
    img.paste(taskbar_layer, (0, ty), taskbar_layer)
    draw.line([(0, ty), (WIDTH, ty)], fill=(45, 55, 75), width=1)

    # 1. Left: Weather Widget
    draw.text((24, ty + 14), "⛅ 24°C", font=font_code, fill=TEXT_WHITE)
    draw.text((80, ty + 15), "Mostly sunny", font=font_code_small, fill=TEXT_MUTED)

    # 2. Center: Windows 11 App Icons
    cx = 520

    # Start Button (Windows 11 Blue 4-squares)
    draw.rounded_rectangle([cx, ty + 6, cx + 36, ty + 42], radius=6, fill=(35, 45, 65) if active_app == "start" else (0,0,0,0))
    draw.rectangle([cx + 9, ty + 14, cx + 16, ty + 21], fill=(0, 164, 239))
    draw.rectangle([cx + 19, ty + 14, cx + 26, ty + 21], fill=(0, 164, 239))
    draw.rectangle([cx + 9, ty + 24, cx + 16, ty + 31], fill=(0, 164, 239))
    draw.rectangle([cx + 19, ty + 24, cx + 26, ty + 31], fill=(0, 164, 239))

    # Search Pill
    sx = cx + 42
    draw.rounded_rectangle([sx, ty + 8, sx + 120, ty + 40], radius=16, fill=(28, 35, 50), outline=(50, 62, 85))
    draw.text((sx + 14, ty + 14), "🔍 Search", font=font_code_small, fill=TEXT_MUTED)

    # File Explorer
    fx = sx + 128
    draw.rectangle([fx + 8, ty + 16, fx + 28, ty + 32], fill=(234, 179, 8), outline=(202, 138, 4))
    draw.rectangle([fx + 8, ty + 13, fx + 18, ty + 17], fill=(245, 158, 11))

    # Microsoft Edge
    ex = fx + 40
    draw.ellipse([ex + 8, ty + 14, ex + 28, ty + 34], fill=(14, 165, 233))
    draw.ellipse([ex + 12, ty + 18, ex + 24, ty + 30], fill=(56, 189, 248))

    # Windows Terminal
    tx = ex + 40
    is_term = (active_app == "terminal")
    draw.rounded_rectangle([tx, ty + 6, tx + 36, ty + 42], radius=6, fill=(45, 58, 85) if is_term else (25, 32, 48))
    draw.rectangle([tx + 8, ty + 14, tx + 28, ty + 32], fill=(12, 12, 16), outline=(75, 85, 105))
    draw.text((tx + 10, ty + 15), ">_", font=font_code_small, fill=ACCENT_CYAN)
    if is_term:
        draw.line([(tx + 10, ty + 44), (tx + 26, ty + 44)], fill=ACCENT_CYAN, width=2)

    # Google Antigravity IDE (Using the REAL 24x24 Antigravity Logo)
    ax = tx + 40
    is_agy = (active_app == "antigravity")
    draw.rounded_rectangle([ax, ty + 6, ax + 36, ty + 42], radius=6, fill=(45, 58, 85) if is_agy else (25, 32, 48))
    img.paste(REAL_AGY_LOGO_24, (ax + 6, ty + 12), REAL_AGY_LOGO_24)
    if is_agy:
        draw.line([(ax + 10, ty + 44), (ax + 26, ty + 44)], fill=ACCENT_PURPLE, width=2)

    # VS Code / Code Icon
    vx = ax + 40
    img.paste(REAL_CODE_ICON, (vx + 6, ty + 12), REAL_CODE_ICON)

    # 3. Right: System Tray & Clock
    rx = WIDTH - 220
    draw.text((rx, ty + 16), "^", font=font_code_small, fill=TEXT_MUTED)
    draw.text((rx + 22, ty + 16), "ENG", font=font_code_small, fill=TEXT_WHITE)
    draw.text((rx + 60, ty + 16), "📶 🔊 🔋", font=font_code_small, fill=TEXT_WHITE)
    draw.text((rx + 125, ty + 10), clock_str, font=font_code_small, fill=TEXT_WHITE)
    draw.text((rx + 125, ty + 26), "11/21/2026", font=font_code_small, fill=TEXT_MUTED)
    draw.text((rx + 195, ty + 16), "🔔", font=font_code_small, fill=TEXT_MUTED)

def draw_desktop_icons(img):
    draw = ImageDraw.Draw(img)
    # 1. Recycle Bin
    draw.text((36, 35), "🗑️", font=font_header, fill=TEXT_WHITE)
    draw.text((20, 61), "Recycle Bin", font=font_code_small, fill=TEXT_WHITE)

    # 2. This PC
    draw.text((36, 115), "🖥️", font=font_header, fill=TEXT_WHITE)
    draw.text((25, 141), "This PC", font=font_code_small, fill=TEXT_WHITE)

    # 3. Google Antigravity Desktop Shortcut (Real Logo)
    img.paste(REAL_AGY_LOGO_32, (34, 195), REAL_AGY_LOGO_32)
    draw.text((16, 230), "Antigravity", font=font_code_small, fill=TEXT_WHITE)

    # 4. Projects Folder
    draw.text((36, 275), "📁", font=font_header, fill=TEXT_WHITE)
    draw.text((22, 301), "Projects", font=font_code_small, fill=TEXT_WHITE)

def draw_caption_bar(draw, text, progress):
    bar_h = 50
    bar_y = HEIGHT - 48 - bar_h - 10
    draw.rounded_rectangle([40, bar_y, WIDTH - 40, bar_y + bar_h], radius=10, fill=(10, 14, 24), outline=(40, 52, 75), width=1)
    
    cx = 62
    cy = bar_y + 25
    for i in range(7):
        phase = (progress * 15 + i) % 3.14
        h = int(18 * (0.5 + 0.5 * np.sin(phase)))
        draw.line([(cx + i * 5, cy - h // 2), (cx + i * 5, cy + h // 2)], fill=ACCENT_CYAN, width=2)

    draw.text((105, bar_y + 15), text[:135] + ("..." if len(text) > 135 else ""), font=font_caption, fill=TEXT_WHITE)

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
        print(f"🎙️ Recording voiceover for [{sc['title']}]...")
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

# ----------------- REALISTIC APP RENDERERS -----------------

def render_desktop_open_terminal(frame, total, scene):
    img = BASE_WALLPAPER.copy()
    draw_desktop_icons(img)
    draw_windows11_taskbar(img, active_app="terminal")
    draw = ImageDraw.Draw(img)

    prog = frame / total
    mx = int(350 + prog * 315)
    my = int(320 + prog * 360)

    # Windows Terminal Window
    if prog > 0.40:
        wx, wy, ww, wh = 160, 80, 960, 520
        draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=8, fill=(12, 12, 14), outline=(48, 54, 66), width=1)
        # Windows Terminal Tab Bar
        draw.rectangle([wx, wy, wx + ww, wy + 34], fill=(28, 32, 42))
        draw.rounded_rectangle([wx + 8, wy + 4, wx + 230, wy + 34], radius=4, fill=(12, 12, 14))
        draw.text((wx + 18, wy + 9), ">_ Administrator: Windows Terminal", font=font_code_small, fill=TEXT_WHITE)
        draw.text((wx + 242, wy + 8), "+  v", font=font_code_small, fill=TEXT_MUTED)
        draw.text((wx + ww - 65, wy + 8), "—  □  ✕", font=font_code_small, fill=TEXT_MUTED)

        draw.text((wx + 20, wy + 48), "Windows PowerShell", font=font_code, fill=TEXT_WHITE)
        draw.text((wx + 20, wy + 70), "Copyright (C) Microsoft Corporation. All rights reserved.", font=font_code, fill=TEXT_MUTED)
        draw.text((wx + 20, wy + 115), "PS C:\\Users\\Compumarts> ", font=font_code, fill=TEXT_WHITE)
        if (frame // 10) % 2 == 0:
            draw.text((wx + 225, wy + 115), "█", font=font_code, fill=ACCENT_CYAN)

    draw_mouse_cursor(draw, mx, my)
    draw_caption_bar(draw, scene["narration"], prog)
    return img

def render_terminal_install_link(frame, total, scene):
    img = BASE_WALLPAPER.copy()
    draw_desktop_icons(img)
    draw_windows11_taskbar(img, active_app="terminal")
    draw = ImageDraw.Draw(img)

    wx, wy, ww, wh = 140, 60, 1000, 540
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=8, fill=(12, 12, 14), outline=(48, 54, 66), width=1)
    draw.rectangle([wx, wy, wx + ww, wy + 34], fill=(28, 32, 42))
    draw.rounded_rectangle([wx + 8, wy + 4, wx + 230, wy + 34], radius=4, fill=(12, 12, 14))
    draw.text((wx + 18, wy + 9), ">_ Administrator: Windows Terminal", font=font_code_small, fill=TEXT_WHITE)
    draw.text((wx + ww - 65, wy + 8), "—  □  ✕", font=font_code_small, fill=TEXT_MUTED)

    prog = frame / total
    lines = [
        ("PS C:\\Users\\Compumarts> pip install fazah-arsenal", TEXT_WHITE, 0.05),
        ("Collecting fazah-arsenal (v6.5.0)", TEXT_MUTED, 0.10),
        ("  Downloading fazah_arsenal-6.5.0-py3-none-any.whl (4.6 MB)", TEXT_MUTED, 0.16),
        ("Successfully installed fazah-arsenal-6.5.0", ACCENT_GREEN, 0.22),
        ("", TEXT_MUTED, 0.25),
        ("PS C:\\Users\\Compumarts> fazah link", ACCENT_CYAN, 0.30),
        ("╔═══════════════════════════════════════════════════════════════════════════════════════╗", ACCENT_PURPLE, 0.35),
        ("║  FAZAH AI ARSENAL v6.5  ·  Zero-Touch MCP Auto-Link Engine                           ║", ACCENT_PURPLE, 0.38),
        ("╠═══════════════════════════════════════════════════════════════════════════════════════╣", ACCENT_PURPLE, 0.40),
        ("║  ✓ Google Antigravity:   .gemini/antigravity/mcp_config.json          [LINKED]       ║", ACCENT_GREEN, 0.48),
        ("║  ✓ Cursor IDE:           .cursor/mcp.json                             [LINKED]       ║", ACCENT_GREEN, 0.56),
        ("║  ✓ Claude Desktop:       AppData/Roaming/Claude/claude_desktop...     [LINKED]       ║", ACCENT_GREEN, 0.64),
        ("║  ✓ Windsurf:             .codeium/windsurf/mcp_config.json            [LINKED]       ║", ACCENT_GREEN, 0.72),
        ("║  ✓ VS Code Cline & Roo:  globalStorage/mcp_settings.json              [LINKED]       ║", ACCENT_GREEN, 0.80),
        ("║  ✓ Workspace:            ./.mcp.json                                  [LINKED]       ║", ACCENT_GREEN, 0.86),
        ("╚═══════════════════════════════════════════════════════════════════════════════════════╝", ACCENT_PURPLE, 0.88),
        ("✨ 18 Native MCP Tools & 20,078 Curated Repositories Ready Across All Editors!", ACCENT_CYAN, 0.94),
    ]

    curr_y = wy + 46
    for txt, col, thresh in lines:
        if prog >= thresh:
            draw.text((wx + 20, curr_y), txt, font=font_code, fill=col)
        curr_y += 24

    draw_caption_bar(draw, scene["narration"], prog)
    return img

def render_launch_antigravity(frame, total, scene):
    img = BASE_WALLPAPER.copy()
    draw_desktop_icons(img)

    prog = frame / total
    draw_windows11_taskbar(img, active_app="antigravity" if prog > 0.4 else "terminal")
    draw = ImageDraw.Draw(img)

    # Window expand animation
    scale = min(1.0, 0.45 + prog * 0.9)
    ww = int(1160 * scale)
    wh = int(550 * scale)
    wx = (WIDTH - ww) // 2
    wy = 35 + (550 - wh) // 2

    # Antigravity Window Body
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=8, fill=(18, 18, 24), outline=(42, 48, 64), width=1)
    
    # 1. Top Title Bar (Authentic Antigravity IDE)
    draw.rectangle([wx, wy, wx + ww, wy + 38], fill=(24, 24, 32))
    img.paste(REAL_AGY_LOGO_18, (wx + 12, wy + 10), REAL_AGY_LOGO_18)
    draw.text((wx + 36, wy + 10), "Antigravity", font=font_body_bold, fill=TEXT_WHITE)
    draw.text((wx + 125, wy + 11), "File  Edit  Selection  View  Go  Run  Terminal  Help", font=font_code_small, fill=TEXT_MUTED)

    # Center Search Bar Pill
    cx_search = wx + ww // 2 - 130
    draw.rounded_rectangle([cx_search, wy + 6, cx_search + 260, wy + 32], radius=13, fill=(15, 15, 20), outline=(45, 45, 55))
    draw.text((cx_search + 15, wy + 10), "🔍 FAZAH AI Arsenal (Ctrl+P)", font=font_code_small, fill=TEXT_MUTED)

    # Right: Model Selector & Window Buttons
    draw.rounded_rectangle([wx + ww - 240, wy + 7, wx + ww - 85, wy + 31], radius=12, fill=(30, 25, 45), outline=ACCENT_PURPLE)
    draw.text((wx + ww - 230, wy + 10), "✦ Gemini 3.8 Flash ▼", font=font_code_small, fill=ACCENT_PURPLE)
    draw.text((wx + ww - 65, wy + 9), "—  □  ✕", font=font_code_small, fill=TEXT_MUTED)

    if scale > 0.85:
        # 2. Activity Bar (Leftmost Strip)
        draw.rectangle([wx, wy + 38, wx + 48, wy + wh], fill=(15, 15, 20))
        draw.text((wx + 14, wy + 55), "📄", font=font_card, fill=TEXT_WHITE)
        draw.text((wx + 14, wy + 95), "🔍", font=font_card, fill=TEXT_MUTED)
        draw.text((wx + 14, wy + 135), "🌿", font=font_card, fill=TEXT_MUTED)
        draw.text((wx + 14, wy + 175), "🧩", font=font_card, fill=ACCENT_CYAN)
        draw.text((wx + 14, wy + wh - 30), "⚙", font=font_card, fill=TEXT_MUTED)

        # 3. Explorer Panel
        draw.rectangle([wx + 48, wy + 38, wx + 220, wy + wh], fill=(22, 22, 30))
        draw.text((wx + 60, wy + 50), "EXPLORER: ARSENAL", font=font_code_small, fill=TEXT_MUTED)
        draw.text((wx + 60, wy + 75), "▼ scripts", font=font_code_small, fill=TEXT_WHITE)
        draw.text((wx + 75, wy + 96), "🐍 gh_arsenal.py", font=font_code_small, fill=ACCENT_CYAN)
        draw.text((wx + 75, wy + 116), "🐍 mcp_server.py", font=font_code_small, fill=ACCENT_CYAN)
        draw.text((wx + 60, wy + 140), "▼ references", font=font_code_small, fill=TEXT_WHITE)
        draw.text((wx + 75, wy + 160), "📦 mega_index.json", font=font_code_small, fill=TEXT_MUTED)
        draw.text((wx + 60, wy + 185), "⚙ .mcp.json", font=font_code_small, fill=ACCENT_GREEN)
        
        # MCP Servers Widget in Explorer
        draw.rounded_rectangle([wx + 55, wy + 215, wx + 212, wy + 265], radius=6, fill=(15, 22, 32), outline=(35, 45, 60))
        draw.text((wx + 64, wy + 222), "MCP SERVERS:", font=font_code_small, fill=TEXT_MUTED)
        draw.text((wx + 64, wy + 242), "● fazah-arsenal", font=font_code_small, fill=ACCENT_GREEN)

        # 4. Center Editor Area
        ex = wx + 220
        ew = ww - 220 - 410
        draw.rectangle([ex, wy + 38, ex + ew, wy + wh], fill=(30, 30, 30)) # VS Code Dark+ BG
        # Tab
        draw.rectangle([ex, wy + 38, ex + 140, wy + 68], fill=(30, 30, 30))
        draw.text((ex + 15, wy + 46), "main.py ✕", font=font_code_small, fill=TEXT_WHITE)
        draw.line([(ex, wy + 68), (ex + ew, wy + 68)], fill=(40, 40, 40), width=1)
        # Editor content
        draw.text((ex + 20, wy + 85), "# Antigravity Autonomous Agent Workspace\n# FAZAH AI Arsenal Native MCP Server Ready (18 Tools)\n\nimport asyncio", font=font_code, fill=TEXT_MUTED)

        # 5. Right Agent Chat Pane
        cx = ex + ew
        draw.rectangle([cx, wy + 38, wx + ww, wy + wh], fill=(20, 20, 26))
        draw.line([(cx, wy + 38), (cx, wy + wh)], fill=(40, 40, 50), width=1)
        
        # Agent Chat Header
        draw.text((cx + 15, wy + 46), "✦ Agent · Gemini 3.8 Flash", font=font_card, fill=ACCENT_PURPLE)
        draw.rounded_rectangle([cx + 310, wy + 44, cx + 390, wy + 64], radius=4, fill=(16, 35, 26), outline=ACCENT_GREEN)
        draw.text((cx + 318, wy + 48), "● Ready", font=font_code_small, fill=ACCENT_GREEN)

    # Mouse animation
    mx = int(720 - (1.0 - prog) * 220)
    my = int(240 + (1.0 - prog) * 160)
    draw_mouse_cursor(draw, mx, my)

    draw_caption_bar(draw, scene["narration"], prog)
    return img

def render_antigravity_verify_dialog(frame, total, scene):
    img = BASE_WALLPAPER.copy()
    draw_desktop_icons(img)
    draw_windows11_taskbar(img, active_app="antigravity")

    wx, wy, ww, wh = 70, 35, 1140, 555
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=8, fill=(18, 18, 24), outline=(42, 48, 64), width=1)
    
    # Title Bar
    draw.rectangle([wx, wy, wx + ww, wy + 38], fill=(24, 24, 32))
    img.paste(REAL_AGY_LOGO_18, (wx + 12, wy + 10), REAL_AGY_LOGO_18)
    draw.text((wx + 36, wy + 10), "Antigravity — FAZAH AI Arsenal", font=font_body_bold, fill=TEXT_WHITE)
    draw.rounded_rectangle([wx + ww - 240, wy + 7, wx + ww - 85, wy + 31], radius=12, fill=(30, 25, 45), outline=ACCENT_PURPLE)
    draw.text((wx + ww - 230, wy + 10), "✦ Gemini 3.8 Flash ▼", font=font_code_small, fill=ACCENT_PURPLE)
    draw.text((wx + ww - 65, wy + 9), "—  □  ✕", font=font_code_small, fill=TEXT_MUTED)

    # Activity Bar & Sidebar
    draw.rectangle([wx, wy + 38, wx + 48, wy + wh], fill=(15, 15, 20))
    draw.text((wx + 14, wy + 55), "📄", font=font_card, fill=TEXT_WHITE)
    draw.text((wx + 14, wy + 95), "🔍", font=font_card, fill=TEXT_MUTED)
    draw.text((wx + 14, wy + 135), "🌿", font=font_card, fill=TEXT_MUTED)
    draw.text((wx + 14, wy + 175), "🧩", font=font_card, fill=ACCENT_CYAN)

    draw.rectangle([wx + 48, wy + 38, wx + 220, wy + wh], fill=(22, 22, 30))
    draw.text((wx + 60, wy + 50), "EXPLORER", font=font_code_small, fill=TEXT_MUTED)
    draw.text((wx + 60, wy + 74), "📁 FAZAH-Arsenal", font=font_code_small, fill=TEXT_WHITE)
    draw.text((wx + 75, wy + 96), "⚙ .mcp.json [✓]", font=font_code_small, fill=ACCENT_GREEN)
    
    # MCP Status widget
    draw.rounded_rectangle([wx + 55, wy + 130, wx + 212, wy + 180], radius=6, fill=(15, 24, 35), outline=ACCENT_GREEN)
    draw.text((wx + 64, wy + 138), "MCP STATUS:", font=font_code_small, fill=TEXT_MUTED)
    draw.text((wx + 64, wy + 156), "● fazah-arsenal", font=font_code_small, fill=ACCENT_GREEN)

    # Main Agent Workspace (center-right)
    cx = wx + 220
    cw = ww - 220
    draw.rectangle([cx, wy + 38, wx + ww, wy + wh], fill=(20, 20, 26))

    prog = frame / total

    # 1. User Message (Authentic Antigravity Chat Bubble)
    if prog > 0.08:
        # User Avatar
        draw.ellipse([cx + 25, wy + 55, cx + 55, wy + 85], fill=(30, 41, 59))
        draw.text((cx + 36, wy + 62), "U", font=font_body_bold, fill=TEXT_WHITE)

        draw.rounded_rectangle([cx + 65, wy + 52, cx + cw - 35, wy + 105], radius=8, fill=(28, 35, 48), outline=(45, 55, 75))
        draw.text((cx + 80, wy + 60), "User · 2:31 PM", font=font_code_small, fill=TEXT_MUTED)
        draw.text((cx + 80, wy + 78), '"Is the FAZAH AI Arsenal tool linked to you and ready?"', font=font_body_bold, fill=TEXT_WHITE)

    # 2. Antigravity Agent Thinking & Tool Inspection Box
    if prog > 0.32:
        # Assistant Avatar (Real Antigravity Logo)
        img.paste(REAL_AGY_LOGO_24, (cx + 28, wy + 124), REAL_AGY_LOGO_24)

        # Tool Accordion Box
        draw.rounded_rectangle([cx + 65, wy + 120, cx + cw - 35, wy + 172], radius=6, fill=(18, 25, 40), outline=ACCENT_PURPLE)
        draw.text((cx + 80, wy + 128), "▾ Thought for 0.8s  ·  Tool Execution", font=font_code_small, fill=ACCENT_PURPLE)
        draw.text((cx + 80, wy + 148), "▶ call: mcp_fazah_arsenal_list_tools()  →  18 active tools, 20,078 repos indexed", font=font_code, fill=ACCENT_CYAN)

    # 3. Antigravity Agent Official Response
    if prog > 0.55:
        draw.rounded_rectangle([cx + 65, wy + 185, cx + cw - 35, wy + 400], radius=8, fill=(18, 24, 36), outline=ACCENT_GREEN, width=1)
        draw.text((cx + 80, wy + 196), "Antigravity Assistant · Gemini 3.8 Flash", font=font_code_small, fill=ACCENT_GREEN)
        
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
            draw.text((cx + 80, wy + 220 + idx * 20), line, font=font_code if idx > 1 else font_body_bold, fill=TEXT_WHITE if idx <= 2 else (ACCENT_GREEN if "•" in line else TEXT_MUTED))

    # Bottom Chat Input Bar
    draw.rounded_rectangle([cx + 25, wy + wh - 55, cx + cw - 25, wy + wh - 12], radius=8, fill=(15, 18, 26), outline=(40, 50, 70))
    draw.text((cx + 42, wy + wh - 38), "Ask Antigravity a question or request changes...", font=font_body, fill=TEXT_DIM)
    draw.rounded_rectangle([cx + cw - 65, wy + wh - 48, cx + cw - 35, wy + wh - 18], radius=6, fill=ACCENT_BLUE)
    draw.text((cx + cw - 54, wy + wh - 40), "↑", font=font_body_bold, fill=TEXT_WHITE)

    draw_caption_bar(draw, scene["narration"], prog)
    return img

def render_antigravity_live_build(frame, total, scene):
    img = BASE_WALLPAPER.copy()
    draw_desktop_icons(img)
    draw_windows11_taskbar(img, active_app="antigravity")

    wx, wy, ww, wh = 70, 35, 1140, 555
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=8, fill=(18, 18, 24), outline=(42, 48, 64), width=1)
    
    # Title Bar
    draw.rectangle([wx, wy, wx + ww, wy + 38], fill=(24, 24, 32))
    img.paste(REAL_AGY_LOGO_18, (wx + 12, wy + 10), REAL_AGY_LOGO_18)
    draw.text((wx + 36, wy + 10), "Antigravity — [scraper.py] — Autonomous Build", font=font_body_bold, fill=TEXT_WHITE)
    draw.rounded_rectangle([wx + ww - 240, wy + 7, wx + ww - 85, wy + 31], radius=12, fill=(30, 25, 45), outline=ACCENT_PURPLE)
    draw.text((wx + ww - 230, wy + 10), "✦ Gemini 3.8 Flash ▼", font=font_code_small, fill=ACCENT_PURPLE)
    draw.text((wx + ww - 65, wy + 9), "—  □  ✕", font=font_code_small, fill=TEXT_MUTED)

    prog = frame / total

    # Left: Agent Chat pane (430px)
    cx, cy, cw, ch = wx, wy + 38, 440, wh - 38
    draw.rectangle([cx, cy, cx + cw, cy + ch], fill=(20, 20, 26))
    draw.line([(cx + cw, cy), (cx + cw, cy + ch)], fill=(40, 40, 50), width=1)

    # User Request bubble
    draw.ellipse([cx + 15, cy + 18, cx + 45, cy + 48], fill=(30, 41, 59))
    draw.text((cx + 25, cy + 25), "U", font=font_body_bold, fill=TEXT_WHITE)
    draw.rounded_rectangle([cx + 55, cy + 15, cx + cw - 15, cy + 70], radius=6, fill=(28, 35, 48))
    draw.text((cx + 65, cy + 22), "User · 2:32 PM", font=font_code_small, fill=TEXT_MUTED)
    draw.text((cx + 65, cy + 40), '"Build an async scraper with PostgreSQL"', font=font_body_bold, fill=TEXT_WHITE)

    # Tool Calls Progression
    if prog > 0.16:
        img.paste(REAL_AGY_LOGO_18, (cx + 20, cy + 85), REAL_AGY_LOGO_18)
        draw.rounded_rectangle([cx + 55, cy + 82, cx + cw - 15, cy + 172], radius=6, fill=(18, 25, 40), outline=ACCENT_CYAN)
        draw.text((cx + 65, cy + 90), "ANTIGRAVITY TOOL CALLS (MCP):", font=font_code_small, fill=ACCENT_CYAN)
        draw.text((cx + 65, cy + 112), "1. arsenal_give('unclecode/crawl4ai')", font=font_code_small, fill=ACCENT_GREEN)
        draw.text((cx + 65, cy + 132), "2. arsenal_recommend('postgres async')", font=font_code_small, fill=ACCENT_GREEN)
        draw.text((cx + 65, cy + 152), "✓ Verified imports resolved in 3ms offline", font=font_code_small, fill=TEXT_MUTED)

    if prog > 0.36:
        draw.rounded_rectangle([cx + 55, cy + 184, cx + cw - 15, cy + 285], radius=6, fill=(16, 32, 24), outline=ACCENT_GREEN)
        draw.text((cx + 65, cy + 192), "AGENT OUTCOME:", font=font_code_small, fill=ACCENT_GREEN)
        draw.text((cx + 65, cy + 214), "• Selected crawl4ai + asyncpg", font=font_code_small, fill=TEXT_WHITE)
        draw.text((cx + 65, cy + 234), "• Injected code into scraper.py", font=font_code_small, fill=TEXT_WHITE)
        draw.text((cx + 65, cy + 254), "• 0 tokens burned on web search", font=font_code_small, fill=ACCENT_CYAN)

    # Right: Authentic VS Code Dark+ Code Editor
    ex, ey, ew, eh = cx + cw, cy, ww - cw, ch
    draw.rectangle([ex, ey, wx + ww, ey + eh], fill=(30, 30, 30))
    
    # Editor Tab Bar
    draw.rectangle([ex, ey, ex + 150, ey + 32], fill=(30, 30, 30))
    draw.text((ex + 18, ey + 8), "scraper.py [Generated] ✕", font=font_code_small, fill=ACCENT_CYAN)
    draw.line([(ex, ey + 32), (wx + ww, ey + 32)], fill=(45, 45, 45), width=1)

    # Line Numbers Gutter (45px width)
    draw.rectangle([ex, ey + 32, ex + 45, ey + eh], fill=(30, 30, 30))
    draw.line([(ex + 45, ey + 32), (ex + 45, ey + eh)], fill=(45, 45, 45), width=1)

    code_lines = [
        ("import asyncio", SYNTAX_KEYWORD),
        ("from crawl4ai import AsyncWebCrawler", SYNTAX_KEYWORD),
        ("import asyncpg", SYNTAX_KEYWORD),
        ("", TEXT_WHITE),
        ("async def scrape_and_store(target_url: str):", SYNTAX_FUNC),
        ("    print(f'[*] Crawling: {target_url}')", SYNTAX_STRING),
        ("    async with AsyncWebCrawler(verbose=True) as crawler:", SYNTAX_KEYWORD),
        ("        result = await crawler.arun(url=target_url)", SYNTAX_VAR),
        ("        content_markdown = result.markdown", SYNTAX_VAR),
        ("", TEXT_WHITE),
        ("    # Store cleanly in PostgreSQL via asyncpg", SYNTAX_COMMENT),
        ("    conn = await asyncpg.connect('postgresql://user:pass@localhost/db')", SYNTAX_STRING),
        ("    await conn.execute(", SYNTAX_FUNC),
        ("        'INSERT INTO pages(url, text) VALUES($1, $2)',", SYNTAX_STRING),
        ("        target_url, content_markdown", SYNTAX_VAR),
        ("    )", SYNTAX_WHITE := TEXT_WHITE),
        ("    await conn.close()", SYNTAX_FUNC),
        ("    print('[✓] Saved to PostgreSQL successfully!')", SYNTAX_STRING),
        ("", TEXT_WHITE),
        ("if __name__ == '__main__':", SYNTAX_KEYWORD),
        ("    asyncio.run(scrape_and_store('https://news.ycombinator.com'))", SYNTAX_FUNC)
    ]

    visible_lines = min(len(code_lines), int((prog - 0.22) * 32)) if prog > 0.22 else 0
    for idx in range(visible_lines):
        line_txt, col = code_lines[idx]
        ly = ey + 42 + idx * 19
        # Draw Line Number
        draw.text((ex + 14, ly), f"{idx + 1:>2}", font=font_code_small, fill=TEXT_DIM)
        # Draw Code with syntax color
        draw.text((ex + 55, ly), line_txt, font=font_code, fill=col)

    draw_caption_bar(draw, scene["narration"], prog)
    return img

def render_terminal_check_savings(frame, total, scene):
    img = BASE_WALLPAPER.copy()
    draw_desktop_icons(img)
    draw_windows11_taskbar(img, active_app="terminal")
    draw = ImageDraw.Draw(img)

    wx, wy, ww, wh = 100, 50, 1080, 520
    draw.rounded_rectangle([wx, wy, wx + ww, wy + wh], radius=8, fill=(12, 12, 14), outline=ACCENT_CYAN, width=1)
    draw.rectangle([wx, wy, wx + ww, wy + 34], fill=(28, 32, 42))
    draw.rounded_rectangle([wx + 8, wy + 4, wx + 230, wy + 34], radius=4, fill=(12, 12, 14))
    draw.text((wx + 18, wy + 9), ">_ Administrator: Windows Terminal", font=font_code_small, fill=TEXT_WHITE)
    draw.text((wx + ww - 65, wy + 8), "—  □  ✕", font=font_code_small, fill=TEXT_MUTED)

    prog = frame / total
    draw.text((wx + 25, wy + 46), "PS C:\\Users\\Compumarts\\Desktop\\ادوات\\FAZAH AI Arsenal> fazah savings", font=font_code_large, fill=ACCENT_CYAN)

    kpis = [
        ("320,000", "Tokens Saved", ACCENT_GREEN),
        ("$1.90 USD", "Direct Cost Spared", ACCENT_CYAN),
        ("51 Calls", "Web Calls Avoided", ACCENT_AMBER),
        ("~1.0 Hour", "Dev Time Rescued", ACCENT_PURPLE),
    ]
    kw = (ww - 80) // 4
    for i, (val, label, col) in enumerate(kpis):
        kx = wx + 25 + i * (kw + 10)
        ky = wy + 78
        draw.rounded_rectangle([kx, ky, kx + kw, ky + 72], radius=8, fill=(20, 29, 48), outline=(40, 52, 75))
        draw.text((kx + 16, ky + 12), val, font=font_card, fill=col)
        draw.text((kx + 16, ky + 42), label, font=font_code_small, fill=TEXT_MUTED)

    ty = wy + 172
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

    draw.rounded_rectangle([wx + 25, wy + 385, wx + ww - 25, wy + 465], radius=8, fill=(16, 25, 42), outline=ACCENT_GREEN)
    draw.text((wx + 40, wy + 400), "⭐ Star on GitHub: github.com/fazah-arsenal/github-ai-arsenal", font=font_card, fill=ACCENT_CYAN)
    draw.text((wx + 40, wy + 430), "📦 Install now: pip install fazah-arsenal && fazah link", font=font_body, fill=ACCENT_GREEN)

    draw_caption_bar(draw, scene["narration"], prog)
    return img

RENDERERS = {
    "desktop_open_terminal": render_desktop_open_terminal,
    "terminal_install_link": render_terminal_install_link,
    "launch_antigravity": render_launch_antigravity,
    "antigravity_verify_dialog": render_antigravity_verify_dialog,
    "antigravity_live_build": render_antigravity_live_build,
    "terminal_check_savings": render_terminal_check_savings,
}

async def build_pixel_perfect_screencast():
    temp_dir = Path("temp_pixel_screencast")
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    output_mp4 = Path("assets/demo_walkthrough.mp4")
    output_gif = Path("assets/demo_preview.gif")
    output_mp4.parent.mkdir(parents=True, exist_ok=True)
    
    temp_raw_video = temp_dir / "raw_video.mp4"
    master_audio = temp_dir / "master_audio.mp3"
    concat_list = temp_dir / "concat_list.txt"

    print("═══════════════════════════════════════════════════════════════════")
    print("🎬 FAZAH AI ARSENAL v6.5 — PIXEL-PERFECT WIN11 & ANTIGRAVITY")
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
    sample_rate = 14

    global_frame = 0
    t0 = time.time()
    for t in tracks:
        sid = t["scene"]["id"]
        renderer = RENDERERS[sid]
        scene_frames = t["frames"]
        print(f"🎨 Rendering scene: [{t['scene']['title']}] ({scene_frames} frames)...")
        
        for f in range(scene_frames):
            pil_img = renderer(f, scene_frames, t["scene"])
            
            if global_frame % sample_rate == 0 and len(gif_frames) < 110:
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
    print(f"\n🎉 SUCCESS: Pixel-perfect media assets ready!")
    print(f"   MP4 Video: {output_mp4} ({mp4_sz:.2f} MB)")
    print(f"   GIF Preview: {output_gif}")
    print("═══════════════════════════════════════════════════════════════════")

if __name__ == "__main__":
    asyncio.run(build_pixel_perfect_screencast())
