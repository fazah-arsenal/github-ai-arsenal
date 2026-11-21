"""
FAZAH AI Arsenal v6.5 — Video Walkthrough Generator
Renders a 720p HD MP4 video demonstrating all core features:
1. Zero-Touch MCP Auto-Link
2. 1-Call Autonomous Tool Delivery
3. Adaptive Error Memory & Self-Healing
4. Token & Quota Savings Dashboard
"""

import os
import sys
import time
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1280, 720
FPS = 30

FONT_CODE_PATH = "C:/Windows/Fonts/consola.ttf"
FONT_TEXT_PATH = "C:/Windows/Fonts/segoeui.ttf"

font_title = ImageFont.truetype(FONT_TEXT_PATH, 34)
font_subtitle = ImageFont.truetype(FONT_TEXT_PATH, 20)
font_badge = ImageFont.truetype(FONT_TEXT_PATH, 16)
font_code_large = ImageFont.truetype(FONT_CODE_PATH, 19)
font_code = ImageFont.truetype(FONT_CODE_PATH, 16)
font_code_small = ImageFont.truetype(FONT_CODE_PATH, 14)

# Color Palette
BG_COLOR = (7, 11, 20)
CARD_BG = (15, 23, 42)
HEADER_BG = (22, 30, 49)
BORDER_COLOR = (30, 41, 59)
TEXT_WHITE = (248, 250, 252)
TEXT_MUTED = (148, 163, 184)
CYAN = (56, 189, 248)
PURPLE = (168, 85, 247)
GREEN = (34, 197, 94)
AMBER = (245, 158, 11)
RED = (239, 68, 68)

def create_base_canvas():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    # Subtle top gradient
    for y in range(120):
        alpha = int((1.0 - (y / 120.0)) * 24)
        draw.line([(0, y), (WIDTH, y)], fill=(20 + alpha, 18 + alpha, 45 + alpha))
    return img, draw

def draw_window(img, draw, x, y, w, h, title="terminal — fazah@arsenal"):
    # Window card background
    draw.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=CARD_BG, outline=BORDER_COLOR, width=1)
    # Window header bar
    header_h = 36
    draw.rounded_rectangle([x, y, x + w, y + header_h], radius=12, fill=HEADER_BG)
    draw.rectangle([x, y + header_h - 12, x + w, y + header_h], fill=HEADER_BG)
    draw.line([(x, y + header_h), (x + w, y + header_h)], fill=BORDER_COLOR, width=1)

    # Window traffic lights
    draw.ellipse([x + 16, y + 12, x + 28, y + 24], fill=(239, 68, 68))
    draw.ellipse([x + 36, y + 12, x + 48, y + 24], fill=(245, 158, 11))
    draw.ellipse([x + 56, y + 12, x + 68, y + 24], fill=(34, 197, 94))

    # Window title
    draw.text((x + w // 2 - 110, y + 8), title, font=font_code_small, fill=TEXT_MUTED)

def render_frame_intro(frame_idx, total_frames):
    img, draw = create_base_canvas()
    
    # Hero Title
    title = "⚡ FAZAH AI ARSENAL v6.5"
    draw.text((WIDTH // 2 - 250, 160), title, font=font_title, fill=CYAN)
    
    sub = "20,078+ Curated GitHub Tools & Autonomous AI Agent Skill"
    draw.text((WIDTH // 2 - 275, 215), sub, font=font_subtitle, fill=TEXT_WHITE)

    # Feature badges
    badges = [
        "✓ Zero-Touch MCP Link",
        "✓ 1-Call Tool Broker",
        "✓ AST Supply-Chain Audit",
        "✓ Self-Healing Error Memory",
        "✓ Token & Quota Tracker",
    ]
    bx = WIDTH // 2 - 340
    by = 280
    for i, b in enumerate(badges):
        x = bx + (i % 3) * 235
        y = by + (i // 3) * 55
        draw.rounded_rectangle([x, y, x + 220, y + 42], radius=8, fill=CARD_BG, outline=BORDER_COLOR, width=1)
        draw.text((x + 14, y + 10), b, font=font_badge, fill=GREEN if i == 0 else (CYAN if i % 2 == 1 else PURPLE))

    # Install pill
    pill_w = 460
    px = WIDTH // 2 - pill_w // 2
    py = 430
    draw.rounded_rectangle([px, py, px + pill_w, py + 50], radius=10, fill=(15, 23, 42), outline=CYAN, width=1)
    draw.text((px + 24, py + 14), "$ pip install -U fazah-arsenal", font=font_code_large, fill=TEXT_WHITE)

    # Footer note
    draw.text((WIDTH // 2 - 180, 520), "Compatible with Claude Desktop, Cursor, Windsurf, Antigravity", font=font_code_small, fill=TEXT_MUTED)
    return img

def render_terminal_scene(top_tag, top_title, cmd, lines_with_colors, progress_ratio):
    img, draw = create_base_canvas()

    # Top Tag & Title
    draw.rounded_rectangle([60, 24, 60 + 140, 56], radius=6, fill=(56, 189, 248, 30), outline=CYAN, width=1)
    draw.text((72, 30), top_tag, font=font_badge, fill=CYAN)
    draw.text((220, 26), top_title, font=font_title, fill=TEXT_WHITE)

    # Terminal box
    tx, ty, tw, th = 60, 80, 1160, 580
    draw_window(img, draw, tx, ty, tw, th, title=f"bash — fazah@arsenal — {cmd}")

    # Prompt
    prompt_y = ty + 50
    draw.text((tx + 24, prompt_y), "fazah@arsenal:~$ ", font=font_code_large, fill=PURPLE)
    draw.text((tx + 24 + 195, prompt_y), cmd, font=font_code_large, fill=TEXT_WHITE)

    # Output lines
    curr_y = prompt_y + 36
    for line, color in lines_with_colors:
        draw.text((tx + 24, curr_y), line, font=font_code, fill=color)
        curr_y += 24

    # Bottom video progress bar
    bar_w = int((WIDTH - 120) * progress_ratio)
    draw.line([(60, HEIGHT - 20), (60 + bar_w, HEIGHT - 20)], fill=CYAN, width=3)

    return img

def main():
    assets_dir = Path("assets")
    assets_dir.mkdir(parents=True, exist_ok=True)
    video_path = assets_dir / "demo_walkthrough.mp4"

    print(f"🎬 Generating Walkthrough Video -> {video_path}...")
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(str(video_path), fourcc, float(FPS), (WIDTH, HEIGHT))

    # Scene 1: Intro (4 seconds = 120 frames)
    print("  [1/6] Rendering Scene 1: Introduction Card...")
    for f in range(120):
        img = render_frame_intro(f, 120)
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        out.write(frame)

    # Scene 2: Zero-Touch Auto-Link (7 seconds = 210 frames)
    print("  [2/6] Rendering Scene 2: Zero-Touch MCP Link...")
    cmd2 = "fazah link"
    lines2 = [
        ("=== ⚡ FAZAH Zero-Touch MCP Auto-Link ===", CYAN),
        ("Server Executable : C:/Users/.../Python312/Scripts/fazah-mcp.EXE", TEXT_MUTED),
        ("", TEXT_WHITE),
        ("Connected MCP Clients:", TEXT_WHITE),
        ("  [✓ CONNECTED] Claude Desktop   -> AppData/Roaming/Claude/claude_desktop_config.json", GREEN),
        ("  [✓ CONNECTED] Cursor User      -> .cursor/mcp.json", GREEN),
        ("  [✓ CONNECTED] Windsurf         -> .codeium/windsurf/mcp_config.json", GREEN),
        ("  [✓ CONNECTED] Antigravity      -> .gemini/antigravity/mcp_config.json", GREEN),
        ("  [✓ CONNECTED] VS Code Cline    -> cline_mcp_settings.json", GREEN),
        ("  [✓ CONNECTED] VS Code Roo      -> cline_mcp_settings.json", GREEN),
        ("  [✓ CONNECTED] Current Workspace -> .mcp.json", GREEN),
        ("", TEXT_WHITE),
        ("✓ Zero manual steps! Restart Claude Desktop or Cursor to activate 20,078+ tools.", AMBER),
    ]
    for f in range(210):
        # Progressively show lines
        show_count = min(len(lines2), int((f / 120.0) * len(lines2)) + 1)
        visible_lines = lines2[:show_count]
        ratio = (120 + f) / 1050.0
        img = render_terminal_scene("FEATURE 1", "Zero-Touch MCP Auto-Link Engine", cmd2, visible_lines, ratio)
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        out.write(frame)

    # Scene 3: 1-Call Tool Delivery (7 seconds = 210 frames)
    print("  [3/6] Rendering Scene 3: Autonomous Tool Delivery & AST Scan...")
    cmd3 = 'fazah give "scrape dynamic web pages"'
    lines3 = [
        ("=== ⚡ FAZAH Autonomous Tool Delivery ===", CYAN),
        ("Task     : scrape dynamic web pages", TEXT_WHITE),
        ("Winner   : Crawl4AI (LLM Web Crawler) — https://github.com/unclecode/crawl4ai", GREEN),
        ("Why      : Extracting clean LLM-ready Markdown, JSON, and JS-rendered pages.", TEXT_MUTED),
        ("Install  : pip install crawl4ai", AMBER),
        ("Security : [SAFE] Risk Score: 0/100 — Scanned 3 build files: No supply-chain red flags.", GREEN),
        ("Memory   : Previously verified on this machine (unclecode/crawl4ai)", PURPLE),
        ("", TEXT_WHITE),
        ("Ready-to-Use Code Snippet:", CYAN),
        ("  curl -s https://api.crawl4ai.com/scrape \\", TEXT_WHITE),
        ("    -H 'Authorization: Bearer $KEY' \\", TEXT_WHITE),
        ("    -d '{\"url\": \"https://news.ycombinator.com\"}' | jq -r .markdown", TEXT_WHITE),
    ]
    for f in range(210):
        show_count = min(len(lines3), int((f / 120.0) * len(lines3)) + 1)
        visible_lines = lines3[:show_count]
        ratio = (330 + f) / 1050.0
        img = render_terminal_scene("FEATURE 2", "1-Call Autonomous Tool Delivery", cmd3, visible_lines, ratio)
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        out.write(frame)

    # Scene 4: Adaptive Error Memory & Self-Healing (6 seconds = 180 frames)
    print("  [4/6] Rendering Scene 4: Adaptive Error Memory...")
    cmd4 = "fazah mem mistakes"
    lines4 = [
        ("=== ⚡ FAZAH Agent Error Memory & Self-Healing ===", CYAN),
        ("Recorded Tool Failures & Learned Fixes (Active Reflex):", TEXT_WHITE),
        ("", TEXT_WHITE),
        ("  ⛔ broken-org/broken-scraper    [rate_limited] (Failed 1x)", RED),
        ("       Task   : web scraping", TEXT_MUTED),
        ("       Error  : Cloudflare 403 Forbidden captcha block", TEXT_MUTED),
        ("       Fix    : Use crawl4ai instead", GREEN),
        ("       Alt    : https://github.com/unclecode/crawl4ai", CYAN),
        ("", TEXT_WHITE),
        ("  ⛔ bogus/broken-scraper         [missing_dependency] (Failed 2x)", RED),
        ("       Task   : scraping", TEXT_MUTED),
        ("       Error  : ModuleNotFoundError: No module named 'libxml2'", TEXT_MUTED),
        ("       Fix    : Use unclecode/crawl4ai which is pure python", GREEN),
        ("       Alt    : https://github.com/unclecode/crawl4ai", CYAN),
        ("", TEXT_WHITE),
        ("✓ Future tool selections automatically avoid broken repos and recommend replacements!", GREEN),
    ]
    for f in range(180):
        show_count = min(len(lines4), int((f / 100.0) * len(lines4)) + 1)
        visible_lines = lines4[:show_count]
        ratio = (540 + f) / 1050.0
        img = render_terminal_scene("FEATURE 3", "Self-Healing Memory & Penalty Engine", cmd4, visible_lines, ratio)
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        out.write(frame)

    # Scene 5: Token & Quota Savings Tracker (7 seconds = 210 frames)
    print("  [5/6] Rendering Scene 5: Token & Quota Savings Dashboard...")
    cmd5 = "fazah savings"
    lines5 = [
        ("========================================================================", CYAN),
        ("      ⚡ FAZAH AI ARSENAL — TOKEN & QUOTA SAVINGS DASHBOARD ⚡", CYAN),
        ("========================================================================", CYAN),
        ("  💎 Total Tokens Saved     : 171,500 tokens (~171.5k)", GREEN),
        ("  💰 Estimated Cost Saved   : $1.03 USD (Claude 3.5 Sonnet / GPT-4o blend)", GREEN),
        ("  🚀 Web / API Calls Saved  : 24 searches & scraping calls avoided", TEXT_WHITE),
        ("  ⏱️ Agent Latency Saved     : ~0.5 hours of multi-turn wait time", TEXT_WHITE),
        ("------------------------------------------------------------------------", BORDER_COLOR),
        ("  • Offline 20k Index Search      :  12 calls →  42,000 tokens ($0.25) [█████████████░░░░░░░] 24.5%", CYAN),
        ("  • 1-Call Autonomous Delivery    :   5 calls →  62,500 tokens ($0.38) [████████████████████] 36.4%", GREEN),
        ("  • Offline Supply-Chain AST Scan :   4 calls →  32,000 tokens ($0.19) [██████████░░░░░░░░░░] 18.7%", PURPLE),
        ("  • Self-Healing Reflex (Saved)   :   2 calls →  20,000 tokens ($0.12) [██████░░░░░░░░░░░░░░] 11.7%", AMBER),
        ("  • Full-Stack Project Scaffold   :   1 calls →  15,000 tokens ($0.09) [████░░░░░░░░░░░░░░░░]  8.7%", TEXT_MUTED),
        ("------------------------------------------------------------------------", BORDER_COLOR),
        ("  💡 Every query served locally preserves your AI model context & quota!", AMBER),
    ]
    for f in range(210):
        show_count = min(len(lines5), int((f / 120.0) * len(lines5)) + 1)
        visible_lines = lines5[:show_count]
        ratio = (720 + f) / 1050.0
        img = render_terminal_scene("FEATURE 4", "Token & Quota Savings Tracker", cmd5, visible_lines, ratio)
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        out.write(frame)

    # Scene 6: Outro & Links (4 seconds = 120 frames)
    print("  [6/6] Rendering Scene 6: Outro & Installation...")
    for f in range(120):
        img, draw = create_base_canvas()
        draw.text((WIDTH // 2 - 200, 150), "⚡ FAZAH AI ARSENAL v6.5", font=font_title, fill=CYAN)
        draw.text((WIDTH // 2 - 240, 205), "Ready to supercharge your AI Coding Agents", font=font_subtitle, fill=TEXT_WHITE)

        box_w = 680
        bx = WIDTH // 2 - box_w // 2
        by = 280
        draw.rounded_rectangle([bx, by, bx + box_w, by + 190], radius=12, fill=CARD_BG, outline=BORDER_COLOR, width=1)
        draw.text((bx + 30, by + 30), "📦 PyPI   :  pip install -U fazah-arsenal", font=font_code_large, fill=TEXT_WHITE)
        draw.text((bx + 30, by + 75), "🐙 GitHub :  github.com/fazah-arsenal/github-ai-arsenal", font=font_code_large, fill=CYAN)
        draw.text((bx + 30, by + 120), "🐳 Docker :  docker pull fazaharsenal/github-ai-arsenal", font=font_code_large, fill=AMBER)

        draw.text((WIDTH // 2 - 130, 520), "Developer: FAZAH (@testtttttttt11222)", font=font_code, fill=PURPLE)
        
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        out.write(frame)

    out.release()
    file_size_mb = os.path.getsize(str(video_path)) / (1024 * 1024)
    print(f"🎉 Done! Walkthrough video generated: {video_path} ({file_size_mb:.2f} MB)")

if __name__ == "__main__":
    main()
