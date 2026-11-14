#!/usr/bin/env python3
"""v5 — transparent, theme-paired profile art. No fills, no blobs.

Two SVGs from one layout: dark.svg and light.svg. Every shape is a stroke or text
in the theme's ink colour, so the art sits on GitHub's own background in either mode.
README wraps them in <picture> with prefers-color-scheme.
"""
import os

OUT = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(OUT, "assets")
os.makedirs(A, exist_ok=True)

MONO = "ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,monospace"

THEMES = {
    "dark":  dict(ink="#e6edf3", dim="#8b949e", faint="#30363d", accent="#d29922", good="#3fb950"),
    "light": dict(ink="#1f2328", dim="#59636e", faint="#d1d9e0", accent="#9a6700", good="#1a7f37"),
}

G = {
 "A": ["01110","10001","10001","11111","10001","10001","10001"],
 "B": ["11110","10001","10001","11110","10001","10001","11110"],
 "C": ["01110","10001","10000","10000","10000","10001","01110"],
 "D": ["11110","10001","10001","10001","10001","10001","11110"],
 "E": ["11111","10000","10000","11110","10000","10000","11111"],
 "F": ["11111","10000","10000","11110","10000","10000","10000"],
 "G": ["01110","10001","10000","10111","10001","10001","01111"],
 "H": ["10001","10001","10001","11111","10001","10001","10001"],
 "I": ["11111","00100","00100","00100","00100","00100","11111"],
 "J": ["00111","00010","00010","00010","00010","10010","01100"],
 "K": ["10001","10010","10100","11000","10100","10010","10001"],
 "L": ["10000","10000","10000","10000","10000","10000","11111"],
 "M": ["10001","11011","10101","10101","10001","10001","10001"],
 "N": ["10001","11001","10101","10011","10001","10001","10001"],
 "O": ["01110","10001","10001","10001","10001","10001","01110"],
 "P": ["11110","10001","10001","11110","10000","10000","10000"],
 "Q": ["01110","10001","10001","10001","10101","10010","01101"],
 "R": ["11110","10001","10001","11110","10100","10010","10001"],
 "S": ["01111","10000","10000","01110","00001","00001","11110"],
 "T": ["11111","00100","00100","00100","00100","00100","00100"],
 "U": ["10001","10001","10001","10001","10001","10001","01110"],
 "V": ["10001","10001","10001","10001","10001","01010","00100"],
 "W": ["10001","10001","10001","10101","10101","11011","10001"],
 "X": ["10001","10001","01010","00100","01010","10001","10001"],
 "Y": ["10001","10001","01010","00100","00100","00100","00100"],
 "Z": ["11111","00001","00010","00100","01000","10000","11111"],
 "0": ["01110","10001","10011","10101","11001","10001","01110"],
 "1": ["00100","01100","00100","00100","00100","00100","01110"],
 "2": ["01110","10001","00001","00110","01000","10000","11111"],
 "3": ["11110","00001","00001","01110","00001","00001","11110"],
 "4": ["00010","00110","01010","10010","11111","00010","00010"],
 "5": ["11111","10000","11110","00001","00001","10001","01110"],
 "6": ["00110","01000","10000","11110","10001","10001","01110"],
 "7": ["11111","00001","00010","00100","01000","01000","01000"],
 "8": ["01110","10001","10001","01110","10001","10001","01110"],
 "9": ["01110","10001","10001","01111","00001","00010","01100"],
 " ": ["00000"]*7,
 ".": ["00000","00000","00000","00000","00000","01100","01100"],
 "-": ["00000","00000","00000","11111","00000","00000","00000"],
 "/": ["00001","00010","00010","00100","01000","01000","10000"],
 "·": ["00000","00000","01100","01100","00000","00000","00000"],
 ":": ["00000","01100","01100","00000","01100","01100","00000"],
}
TILDE = ["01101", "10010"]

def ptext(s, x, y, scale, fill, tracking=1):
    out, cx = [], x
    for ch in s:
        up = ch.upper()
        if up in G:
            for ry, row in enumerate(G[up]):
                c = 0
                while c < 5:
                    if row[c] == "1":
                        run = 1
                        while c + run < 5 and row[c + run] == "1":
                            run += 1
                        out.append(f'<rect x="{cx + c*scale}" y="{y + ry*scale}" width="{run*scale}" height="{scale}" fill="{fill}"/>')
                        c += run
                    else:
                        c += 1
            if ch == "Ã":
                for ry, row in enumerate(TILDE):
                    for c, bit in enumerate(row):
                        if bit == "1":
                            out.append(f'<rect x="{cx + c*scale}" y="{y - (2 - ry)*scale}" width="{scale}" height="{scale}" fill="{fill}"/>')
        cx += (5 + tracking) * scale
    return "".join(out)

def wof(s, scale, tracking=1):
    return len(s) * (5 + tracking) * scale - tracking * scale

W, M = 1400, 64

def seg_bar(x, y, n, on, colour, w=13, h=22, gap=5, empty=None):
    out = []
    for i in range(n):
        out.append(f'<rect x="{x + i*(w+gap)}" y="{y}" width="{w}" height="{h}" rx="1" fill="{colour if i < on else "none"}" stroke="{colour if i < on else empty}" stroke-width="1.5"/>')
    return "".join(out), n * (w + gap) - gap

def build(mode):
    c = THEMES[mode]
    ink, dim, faint, acc, good = c["ink"], c["dim"], c["faint"], c["accent"], c["good"]
    p = []
    y = 64
    p.append(ptext("PLAYER 1", M, y, 4, acc, 2))
    p.append(ptext("AI LEAD · CTO", W - M - wof("AI LEAD · CTO", 4, 2), y, 4, dim, 2))
    y += 54
    p.append(ptext("SIMÃO LOPES", M, y, 10, ink, 2))
    y += 92
    p.append(f'<text x="{M}" y="{y}" font-family="{MONO}" font-size="27" fill="{dim}">CTO at a product company in Porto — turning the whole company AI-first.</text>')
    y += 18
    p.append(f'<line x1="{M}" y1="{y}" x2="{W-M}" y2="{y}" stroke="{faint}" stroke-width="2"/>')

    y += 42
    bars = [("SHIPPING", 22, 24, good, "chatbot in production 6 months"),
            ("AI SYSTEMS", 21, 24, acc, "a fleet of microservices shipped"),
            ("LEADERSHIP", 16, 24, ink, "CTO — leading the team")]
    for i, (label, on, segs, col, note) in enumerate(bars):
        by = y + i * 50
        p.append(ptext(label, M, by, 3, dim, 2))
        b, bw = seg_bar(M + 250, by - 6, segs, on, col, empty=faint)
        p.append(b)
        p.append(f'<text x="{M+250+bw+22}" y="{by+14}" font-family="{MONO}" font-size="22" fill="{dim}">{note}</text>')
    y += len(bars) * 50 + 10
    p.append(f'<line x1="{M}" y1="{y}" x2="{W-M}" y2="{y}" stroke="{faint}" stroke-width="2"/>')

    y += 44
    p.append(ptext("QUEST LOG", M, y, 5, ink, 2))
    y += 26
    quests = [("ACT III", "CTO", "ACTIVE", acc, "Leading the team, AI-first end to end."),
              ("ACT II", "HEAD OF AI", "CLEARED", good, "AI microservices: design, infra, delivery."),
              ("ACT I", "SOLO BUILD", "LEGENDARY", acc, "Solo-built chatbot, 6 months in prod.")]
    for i, (act, title, status, col, desc) in enumerate(quests):
        ry = y + i * 104
        p.append(f'<rect x="{M}" y="{ry}" width="{W-2*M}" height="88" rx="3" fill="none" stroke="{faint}" stroke-width="1.5"/>')
        p.append(f'<rect x="{M}" y="{ry+14}" width="3" height="60" fill="{col}"/>')
        p.append(ptext(act, M + 28, ry + 24, 3, col, 2))
        p.append(ptext(title, M + 28, ry + 52, 5, ink, 2))
        p.append(f'<text x="{M+430}" y="{ry+52}" font-family="{MONO}" font-size="23" fill="{dim}">{desc}</text>')
        p.append(ptext(status, W - M - 26 - wof(status, 3, 2), ry + 38, 3, col, 2))
    y += len(quests) * 104 + 2
    p.append(f'<line x1="{M}" y1="{y}" x2="{W-M}" y2="{y}" stroke="{faint}" stroke-width="2"/>')

    y += 44
    p.append(ptext("INVENTORY", M, y, 5, ink, 2))
    y += 26
    items = [("HASSIUS", "LEG", acc, "spec repos to agent PRs"),
             ("V100", "EPIC", ink, "LLMs on one Tesla V100"),
             ("NONIUS", "EPIC", ink, "158 exams, structured"),
             ("FREE-LLM", "RARE", good, "free tiers, re-verified"),
             ("DEV-FARM", "RARE", good, "3 Macs, one tailnet"),
             ("44 GAMES", "RARE", good, "one file per game")]
    cols, cw, ch, gap = 3, 400, 128, 24
    for i, (name, rarity, col, desc) in enumerate(items):
        cx = M + (i % cols) * (cw + gap)
        cy = y + (i // cols) * (ch + gap)
        p.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="3" fill="none" stroke="{faint}" stroke-width="1.5"/>')
        p.append(f'<line x1="{cx}" y1="{cy}" x2="{cx+cw}" y2="{cy}" stroke="{col}" stroke-width="2.5"/>')
        p.append(ptext(name, cx + 20, cy + 30, 4, ink, 2))
        p.append(ptext(rarity, cx + 20, cy + 60, 2, col, 2))
        p.append(f'<text x="{cx+20}" y="{cy+102}" font-family="{MONO}" font-size="20" fill="{dim}">{desc}</text>')
    y += 2 * (ch + gap) + 4
    p.append(f'<line x1="{M}" y1="{y}" x2="{W-M}" y2="{y}" stroke="{faint}" stroke-width="2"/>')

    y += 42
    p.append(ptext("STACK", M, y, 3, dim, 2))
    p.append(f'<text x="{M+132}" y="{y+14}" font-family="{MONO}" font-size="22" fill="{ink}">PYTHON · GO · RUST · TYPESCRIPT · CUDA/SM_70 · LLAMA.CPP · VLLM</text>')
    y += 46
    p.append(ptext("OPEN TO", M, y, 3, dim, 2))
    p.append(f'<text x="{M+132}" y="{y+14}" font-family="{MONO}" font-size="22" fill="{good}">AI LEAD / HEAD OF AI / CTO — LINKEDIN.COM/IN/SIMAO-LOPES</text>')
    y += 74
    p.append(ptext("INSERT COIN", M, y, 3, acc, 2))
    p.append(f'<text x="{M+196}" y="{y+14}" font-family="{MONO}" font-size="20" fill="{dim}">github.com/Simao-Lopes · Porto, Portugal</text>')
    y += 48
    H = int(y)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Simão Lopes — CTO and AI lead, Porto">
  {''.join(p)}
</svg>
"""
    return svg, W, H

for mode in ("dark", "light"):
    svg, w, h = build(mode)
    path = os.path.join(A, f"profile-{mode}.svg")
    open(path, "w", encoding="utf-8").write(svg)
    print(mode, f"{w}x{h}", os.path.getsize(path), "bytes")
