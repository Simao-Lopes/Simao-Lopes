#!/usr/bin/env python3
"""Profile plates v3 — pixel HUD for an AI-lead / CTO audience."""
import os

OUT = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(OUT, "assets")
os.makedirs(A, exist_ok=True)

BG    = "#0a0b0d"
PANEL = "#0e1014"
INK   = "#f4f5f7"
DIM   = "#8f97a3"
FAINT = "#23262d"
AMBER = "#f0b45e"
MINT  = "#7ee0b0"
VIOL  = "#b79cff"
RED   = "#ff7a7a"
MONO  = "ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,monospace"

def css():
    return f"""<style>
    .lab {{ font-family:{MONO}; font-weight:600; letter-spacing:3.5px; fill:{DIM}; }}
    .big {{ font-family:{MONO}; font-weight:700; letter-spacing:-1px; fill:{INK}; }}
    .txt {{ font-family:{MONO}; font-weight:400; fill:{DIM}; }}
    .val {{ font-family:{MONO}; font-weight:700; fill:{INK}; }}
    .accent {{ fill:{AMBER}; }}
    .blink {{ animation: blink 1.1s steps(1) infinite; }}
    @keyframes blink {{ 0%,49% {{opacity:1}} 50%,100% {{opacity:0}} }}
    @media (prefers-reduced-motion: reduce) {{ .blink {{animation:none}} }}
  </style>"""

def pixels(map_rows, x, y, s, palette):
    """Draw a char-grid sprite as rects (authentic 8-bit, resolution-independent)."""
    out = []
    for ry, row in enumerate(map_rows):
        cx = 0
        while cx < len(row):
            ch = row[cx]
            if ch in (".", " "):
                cx += 1
                continue
            run = 1
            while cx + run < len(row) and row[cx + run] == ch:
                run += 1
            out.append(f'<rect x="{x + cx*s}" y="{y + ry*s}" width="{run*s}" height="{s}" fill="{palette[ch]}"/>')
            cx += run
    return "".join(out)

PLAYER = [
    "................",
    "................",
    ".....######.....",
    "....########....",
    "...##########...",
    "...##OOOOOO##...",
    "...##OOOOOO##...",
    "...##O#OO#O##...",
    "...###OOOO###...",
    "....########....",
    ".....######.....",
    "....########....",
    "...###.##.###...",
    "..####.##.####..",
    "..###......###..",
    "................",
]
PAL = {"#": "#dfe3ea", "O": AMBER}

def bar(x, y, w, h, pct, colour):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{FAINT}"/>'
            f'<rect x="{x+2}" y="{y+2}" width="{(w-4)*pct:.1f}" height="{h-4}" fill="{colour}"/>')

def hero():
    W, H = 1400, 470
    stats = [("SHIPPING", .96, MINT, "6 months in prod"),
             ("AI SYSTEMS", .92, AMBER, "in production"),
             ("LEADERSHIP", .72, VIOL, "CTO")]
    rows = []
    for i, (label, pct, col, note) in enumerate(stats):
        y = 268 + i * 62
        rows.append(f'<text x="620" y="{y}" class="lab" font-size="22">{label}</text>'
                    f'{bar(760, y-18, 420, 22, pct, col)}'
                    f'<text x="{W-64}" y="{y}" text-anchor="end" class="txt" font-size="20">{note}</text>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Player 1 — Simão Lopes, CTO and AI engineer">
  {css()}
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect x="24" y="24" width="{W-48}" height="{H-48}" fill="{PANEL}" stroke="{FAINT}" stroke-width="2"/>
  <!-- stepped pixel frame corners -->
  <g fill="{AMBER}">
    <rect x="24" y="24" width="10" height="4"/><rect x="24" y="24" width="4" height="10"/>
    <rect x="{W-34}" y="24" width="10" height="4"/><rect x="{W-28}" y="24" width="4" height="10"/>
    <rect x="24" y="{H-28}" width="10" height="4"/><rect x="24" y="{H-34}" width="4" height="10"/>
    <rect x="{W-34}" y="{H-28}" width="10" height="4"/><rect x="{W-28}" y="{H-34}" width="4" height="10"/>
  </g>

  {pixels(PLAYER, 64, 96, 14, PAL)}
  <text x="330" y="118" class="lab" font-size="24" fill="{AMBER}">PLAYER 1</text>
  <text x="330" y="196" class="big" font-size="86">SIMÃO LOPES</text>
  <text x="332" y="242" class="txt" font-size="26">CTO · AI ENGINEER — Porto, Portugal</text>

  {''.join(rows)}

  <text x="64" y="{H-40}" class="lab" font-size="20">GITHUB.COM/SIMAO-LOPES</text>
  <text x="{W-64}" y="{H-40}" text-anchor="end" class="lab" font-size="20" fill="{MINT}">INSERT COIN TO CONTINUE<tspan class="blink">_</tspan></text>
</svg>
"""

QUESTS = [
    ("ACT III", "CTO", "ACTIVE", AMBER, "Leading the team and making the whole company AI-first."),
    ("ACT II", "HEAD OF AI", "CLEARED", MINT, "Shipped a fleet of AI-powered microservices."),
    ("ACT I", "SOLO BUILD", "LEGENDARY", VIOL, "Built a full chatbot alone — 6 months in production."),
]

def quests():
    W, H = 1400, 420
    rows = []
    for i, (act, title, status, col, text) in enumerate(QUESTS):
        y = 130 + i * 96
        rows.append(f"""
  <g>
    <rect x="64" y="{y}" width="{W-128}" height="78" fill="{BG}" stroke="{FAINT}"/>
    <rect x="64" y="{y}" width="6" height="78" fill="{col}"/>
    <text x="92" y="{y+31}" class="lab" font-size="20" fill="{col}">{act}</text>
    <text x="92" y="{y+62}" class="big" font-size="30">{title}</text>
    <text x="400" y="{y+49}" class="txt" font-size="22">{text}</text>
    <text x="{W-92}" y="{y+31}" text-anchor="end" class="lab" font-size="18" fill="{col}">{status}</text>
  </g>""")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Quest log — career">
  {css()}
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <text x="64" y="76" class="lab" font-size="22">QUEST LOG // CAREER</text>
  <line x1="64" y1="96" x2="{W-64}" y2="96" stroke="{FAINT}" stroke-width="2"/>
  {''.join(rows)}
</svg>
"""

ITEMS = [
    ("HASSIUS", "LEGENDARY", AMBER, "Spec repos to agent PRs, human-gated."),
    ("V100 ENGINES", "EPIC", VIOL, "Modern LLMs on one Tesla V100."),
    ("NONIUS", "EPIC", VIOL, "Practice engine, 158 exams parsed."),
    ("FREE LLM", "RARE", MINT, "Free API tiers, re-verified weekly."),
    ("DEV-FARM", "RARE", MINT, "Three Macs, one mesh, code pods."),
    ("44 GAMES", "RARE", MINT, "Self-contained HTML5 games."),
]
GLYPH = [
    "..######..",
    ".########.",
    ".##.##.##.",
    ".##.##.##.",
    ".########.",
    ".##.##.##.",
    ".##.##.##.",
    "..######..",
]

def inventory():
    W, H = 1400, 520
    cells = []
    for i, (name, rarity, col, desc) in enumerate(ITEMS):
        cx = 64 + (i % 2) * 656
        cy = 132 + (i // 2) * 122
        cells.append(f"""
  <g>
    <rect x="{cx}" y="{cy}" width="620" height="104" fill="{PANEL}" stroke="{FAINT}"/>
    {pixels(GLYPH, cx+18, cy+22, 6.2, {'#': col})}
    <text x="{cx+96}" y="{cy+38}" class="big" font-size="27">{name}</text>
    <text x="{cx+600}" y="{cy+38}" text-anchor="end" class="lab" font-size="16" fill="{col}">{rarity}</text>
    <text x="{cx+96}" y="{cy+74}" class="txt" font-size="20">{desc}</text>
  </g>""")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Inventory — projects">
  {css()}
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <text x="64" y="76" class="lab" font-size="22">INVENTORY // PROJECTS</text>
  <line x1="64" y1="96" x2="{W-64}" y2="96" stroke="{FAINT}" stroke-width="2"/>
  {''.join(cells)}
</svg>
"""

for name, fn in (("hero.svg", hero), ("quests.svg", quests), ("inventory.svg", inventory)):
    p = os.path.join(A, name)
    open(p, "w", encoding="utf-8").write(fn())
    print("wrote", p, os.path.getsize(p))
