#!/usr/bin/env python3
"""Render a retro-terminal profile GIF (dark + light), in the style of
github-readme-terminal: a shell session that types itself out and ends on a
neofetch-style panel.

Pillow + DejaVu Sans Mono. No external services, no fonts downloaded.
"""
import os, shutil, tempfile
from PIL import Image, ImageDraw, ImageFont

OUT = "/home/ubuntu/terminal-profile/assets"
os.makedirs(OUT, exist_ok=True)

COLS, ROWS = 84, 26
CW, CH = 9, 18                     # character cell at 1x
PAD = 14
BAR = 30                            # title bar height

THEMES = {
    "dark": dict(bg="#0b0d10", bar="#151a21", edge="#242c37", fg="#e6edf3", dim="#8b949e",
                 prompt="#7ee787", accent="#e3b341", link="#79c0ff", cursor="#e6edf3"),
    "light": dict(bg="#fbfbfa", bar="#eceef1", edge="#d8dde4", fg="#1f2328", dim="#59636e",
                  prompt="#1a7f37", accent="#9a6700", link="#0969da", cursor="#1f2328"),
}

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT = ImageFont.truetype(FONT_PATH, 15)
FONTB = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 15)

# ---------------------------------------------------------------- the session
# Each item: ("cmd", text) | ("out", text, colour) | ("pause", frames) | ("clear",)
SESSION = [
    ("out", "Last login: today on ttys001", "dim"),
    ("cmd", "whoami"),
    ("out", "Simão Lopes — CTO · AI engineer · Porto, PT", "fg"),
    ("pause", 6),
    ("cmd", "cat role.txt"),
    ("out", "Lead the team. Make the company AI-first. Ship it, not slide it.", "fg"),
    ("out", "Owning the boring half: evals, cost, on-call, model swaps.", "dim"),
    ("pause", 8),
    ("cmd", "git log --oneline --decorate"),
    ("out", "* 9f1c0d3 (HEAD -> cto)   AI-first across product and ops", "accent"),
    ("out", "* 4a7b2e1 (head-of-ai)    fleet of AI microservices", "fg"),
    ("out", "* c1d5f80 (solo-build)    chatbot — 6 months in production", "fg"),
    ("pause", 8),
    ("cmd", "ls ~/projects"),
    ("out", "hassius/      v100-engines/   nonius/", "link"),
    ("out", "free-llm/     dev-farm/       games/ (44)", "link"),
    ("pause", 8),
    ("cmd", "cat stack.json"),
    ("out", '"python","go","rust","typescript","cuda/sm70",', "fg"),
    ("out", '"llama.cpp","vllm","sqlite","systemd","tailscale"', "fg"),
    ("pause", 8),
    ("cmd", 'contact --open-to "AI Lead · Head of AI · CTO"'),
    ("out", "→ linkedin.com/in/simao-lopes", "prompt"),
    ("pause", 12),
    ("out", "", "fg"),
    ("out", "▌ready when you are.", "dim"),
]

PROMPT = "simao@porto:~$ "

def wrap(line, width):
    return [line[i:i + width] for i in range(0, max(1, len(line)), width)]

def build_frames(theme):
    c = THEMES[theme]
    W = COLS * CW + PAD * 2
    H = ROWS * CH + PAD * 2 + BAR
    # visible screen state: list of (text, colour)
    lines = []
    frames = []          # (image, duration_ms)

    def render(cursor=True):
        img = Image.new("RGB", (W, H), c["bg"])
        d = ImageDraw.Draw(img)
        # window chrome
        d.rectangle([0, 0, W, BAR], fill=c["bar"])
        d.line([0, BAR, W, BAR], fill=c["edge"], width=1)
        for i, col in enumerate(("#ff5f57", "#febc2e", "#28c840")):
            d.ellipse([PAD + 2 + i * 18, BAR // 2 - 5, PAD + 12 + i * 18, BAR // 2 + 5], fill=col)
        d.text((PAD + 66, BAR // 2 - 8), "simao@porto: ~ — zsh", font=FONT, fill=c["dim"])
        d.rectangle([0, 0, W - 1, H - 1], outline=c["edge"], width=1)

        y = BAR + PAD
        # keep the tail that fits; the screen scrolls like a real terminal
        visible = lines[-(ROWS - 1):] if len(lines) >= ROWS else lines
        for text, colour in visible:
            d.text((PAD, y), text, font=FONT, fill=c[colour])
            y += CH
        if cursor:
            cx = PAD + (len(visible[-1][0]) if visible else 0) * CW
            cy = BAR + PAD + max(0, len(visible) - 1) * CH
            if visible:
                d.rectangle([cx + 1, cy + 2, cx + CW - 1, cy + CH - 2], fill=c["cursor"])
            else:
                d.rectangle([PAD, cy + 2, PAD + CW - 2, cy + CH - 2], fill=c["cursor"])
        return img

    def push(img, ms=50):
        frames.append((img.copy(), ms))

    # boot: a couple of blank beats
    push(render())

    for item in SESSION:
        kind = item[0]
        if kind == "pause":
            for i in range(item[1]):
                push(render(cursor=i % 8 < 4))
        elif kind == "cmd":
            typed = ""
            lines.append((PROMPT, "prompt"))
            for ch in item[1]:
                typed += ch
                lines[-1] = (PROMPT + typed, "prompt")
                push(render())
            push(render(), 220)
        else:
            text, colour = item[1], item[2]
            for part in wrap(text, COLS - 2):
                lines.append((part, colour))
                push(render())
                frames[-1] = (frames[-1][0], 90)

    # tail: blinking cursor hold
    for i in range(24):
        push(render(cursor=i % 8 < 4), 110 if i else 500)
    return frames

def save(frames, path, scale=1, colors=16):
    imgs = []
    for f, _ in frames:
        im = f.resize((f.width * scale, f.height * scale), Image.NEAREST) if scale != 1 else f
        imgs.append(im.convert("P", palette=Image.ADAPTIVE, colors=colors))
    durs = [d for _, d in frames]
    imgs[0].save(path, save_all=True, append_images=imgs[1:], duration=durs,
                 loop=0, optimize=True, disposal=1)
    return os.path.getsize(path)

for theme in ("dark", "light"):
    fr = build_frames(theme)
    p = os.path.join(OUT, f"terminal-{theme}.gif")
    size = save(fr, p)
    print(f"{theme}: {len(fr)} frames, {size/1024:.0f} KB -> {p}")
