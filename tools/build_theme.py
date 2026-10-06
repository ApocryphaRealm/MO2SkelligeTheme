r"""Builds the Skellige MO2 theme as plain files (paste stylesheets\Skellige.qss and stylesheets\Skellige\ into MO2's
stylesheets folder).

The owner, 2026-10-05: "build a matching MO2 theme for the Skellige theme that we used on AMF". Skellige is the Apocrypha
Menu Framework for The Witcher 3's default theme: AMF's Oathvein (thin grey lines, a blood-red highlight) on the black of
the game's own main-menu column. So this repo began as a copy of the Oathvein MO2 Theme (same author, same stylesheet
and build), with these changes:
  * colours - AMF Witcher 3's themes\skellige.ini: background #020203, the rest as Oathvein;
  * no background texture - AMF's Skellige has none (its plates folder holds only the frame and the toggle);
  * the game's frame round the highlighted row - AMF Witcher 3 draws the frame the game puts round its own menu entries
    (a thin outer line and an inner line whose corners step in; Renderer.cpp DrawGameFrame) round the item under the
    mouse or the controller. Here it is drawn round the row under the mouse (55% text colour, as AMF's hover frame) and
    the selected row (95%, as AMF's controller frame), in four pieces so a row of many columns gets one frame;
  * frame art - AMF's own skellige\frame.png (src\amf-art\), drawn for AMF;
  * button faces, check boxes, radio buttons and arrows - Oathvein's shape language (drawn here);
  * icons - the Njordlinger MO2 Theme's set (src\icons\), recoloured to the theme's line colour.
The stylesheet itself (src\theme.qss.in) is written for these themes; no other MO2 theme's files and no game files are
used.

Run from the repo root:  python tools\build_theme.py
"""
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

OUT = os.path.join(ROOT, "stylesheets")

# AMF's palettes. bg/frame/border/text/dim/accent are AMF's sBackground/sFrame/sBorder/sText/sTextDim/sAccent.
# separator is this theme's own choice for MO2's separator rows (AMF has no separator rows); shape picks the art.
THEME = json.load(open(os.path.join(ROOT, "src", "theme.json"), encoding="utf-8"))


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def hexc(c):
    return "#%02x%02x%02x" % tuple(max(0, min(255, round(v))) for v in c)


def mix(a, b, t):
    """a blended toward b by t (solid colour)."""
    ca, cb = rgb(a), rgb(b)
    return hexc(tuple(ca[i] + (cb[i] - ca[i]) * t for i in range(3)))


def rgba(h, a):
    r, g, b = rgb(h)
    return "rgba(%d, %d, %d, %s)" % (r, g, b, ("%.2f" % a).rstrip("0").rstrip("."))


def tokens(t, version):
    folder = t["title"]
    bg, border, accent = t["bg"], t["border"], t["accent"]
    tok = {
        "title": t["title"], "version": version, "folder": folder,
        "bg": bg.lower(), "frame": t["frame"].lower(), "border": border.lower(), "text": t["text"].lower(),
        "dim": t["dim"].lower(), "accent": accent.lower(),
        # AMF's graded tints (Theme.cpp): lines 55 / 28 / 14 %, accent 22 / 42 %
        "border_dim": rgba(border, 0.55), "border_soft": rgba(border, 0.28), "border_faint": rgba(border, 0.14),
        "accent_faint": rgba(accent, 0.22), "accent_soft": rgba(accent, 0.42), "accent_mid": rgba(accent, 0.70),
        "accent_text": accent.lower(),
        "input": mix(bg, border, 0.07), "input_focus": mix(bg, border, 0.13),
        "invalid": mix(bg, "#8E2A2E", 0.55),
        "mod_row": bg.lower(), "separator": t["separator"].lower(),
    }
    if t["art"] and t.get("background", True):
        tok["bg_image"] = 'background-image: url("./%s/art/background.png");' % folder
    else:
        tok["bg_image"] = ""
    if t["art"]:
        # full size: AMF draws these frames with 26px corners; at half size they read too faint (the owner, 2026-09-26:
        # "we need to scale up the corner art to make it more prominent")
        tok["frame_decl"] = 'border-image: url("./%s/art/frame.png") 26 26 26 26 stretch; border-width: 26px;' % folder
    else:
        tok["frame_decl"] = "border: 1px solid %s;" % border.lower()
    return tok


# ---- art ---------------------------------------------------------------------------------------------------------
def svg(w, h, body):
    return '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">%s</svg>' % (w, h, w, h, body)


def button(t, state):
    """48x24 plate, nine-sliced 8px by the sheet. state: normal / hover / pressed / disabled."""
    bg, border, accent = t["bg"], t["border"], t["accent"]
    fill = {"normal": mix(bg, border, 0.08), "hover": mix(bg, border, 0.20),
            "pressed": mix(bg, accent, 0.30), "disabled": bg}[state]
    line = {"normal": border, "hover": t["frame"], "pressed": t["frame"], "disabled": mix(bg, border, 0.4)}[state]
    s = t["shape"]
    if s == "norden":        # plain rounded plate, bright ticks at the corners
        body = ('<rect x="0.5" y="0.5" width="47" height="23" rx="3" fill="%s" stroke="%s" stroke-width="1"/>'
                '<path d="M0.5 5V0.5H5M43 0.5h4.5V5M47.5 19v4.5H43M5 23.5H0.5V19" fill="none" stroke="%s" stroke-width="1"/>'
                % (fill, line, t["frame"] if state != "disabled" else line))
    elif s == "oathvein":    # thin grey line, a crossed scratch at two corners
        body = ('<rect x="0.5" y="0.5" width="47" height="23" fill="%s" stroke="%s" stroke-width="1"/>'
                '<path d="M1 7L7 1M3 1l4 4M41 23l6-6M41 19l4 4" fill="none" stroke="%s" stroke-width="0.8"/>'
                % (fill, line, accent if state in ("hover", "pressed") else line))
    elif s == "veldun":      # cut corners, a small diamond at each end
        body = ('<path d="M5.5 0.5H42.5L47.5 5.5V18.5L42.5 23.5H5.5L0.5 18.5V5.5Z" fill="%s" stroke="%s" stroke-width="1"/>'
                '<path d="M2.5 12l1.5-1.5 1.5 1.5-1.5 1.5zM42.5 12l1.5-1.5 1.5 1.5-1.5 1.5z" fill="%s"/>'
                % (fill, line, line))
    else:                    # untarnished: a single warm hairline
        body = '<rect x="0.5" y="0.5" width="47" height="23" fill="%s" stroke="%s" stroke-width="1"/>' % (fill, line)
    return svg(48, 24, body)


def check(t, kind):
    bg, border, accent, text = t["bg"], t["border"], t["accent"], t["text"]
    box_line = {"off": border, "off-hover": t["frame"], "on": t["frame"], "part": t["frame"], "disabled": mix(bg, border, 0.4)}[kind]
    fill = mix(bg, border, 0.10) if kind != "disabled" else bg
    if t["shape"] == "veldun":
        box = '<path d="M3.5 0.5H10.5L13.5 3.5V10.5L10.5 13.5H3.5L0.5 10.5V3.5Z" fill="%s" stroke="%s"/>' % (fill, box_line)
    elif t["shape"] == "norden":
        box = '<rect x="0.5" y="0.5" width="13" height="13" rx="2" fill="%s" stroke="%s"/>' % (fill, box_line)
    else:
        box = '<rect x="0.5" y="0.5" width="13" height="13" fill="%s" stroke="%s"/>' % (fill, box_line)
    mark = ""
    tick = accent if t["shape"] == "oathvein" else text
    if kind == "on":
        mark = '<path d="M3.5 7.2l2.3 2.3 4.7-5" fill="none" stroke="%s" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>' % tick
    elif kind == "part":
        mark = '<rect x="4" y="6.2" width="6" height="1.6" fill="%s"/>' % tick
    return svg(14, 14, box + mark)


def radio(t, kind):
    bg, border, accent, text = t["bg"], t["border"], t["accent"], t["text"]
    line = {"off": border, "off-hover": t["frame"], "on": t["frame"]}[kind]
    if t["shape"] == "veldun":
        ring = '<path d="M7 0.7L13.3 7 7 13.3 0.7 7Z" fill="%s" stroke="%s"/>' % (mix(bg, border, 0.10), line)
        dot = '<path d="M7 3.8L10.2 7 7 10.2 3.8 7Z" fill="%s"/>' % text
    else:
        ring = '<circle cx="7" cy="7" r="6.3" fill="%s" stroke="%s"/>' % (mix(bg, border, 0.10), line)
        dot = '<circle cx="7" cy="7" r="3" fill="%s"/>' % (accent if t["shape"] == "oathvein" else text)
    return svg(14, 14, ring + (dot if kind == "on" else ""))


def arrow(t, direction):
    paths = {"down": "M2 4l4 4 4-4", "up": "M2 8l4-4 4 4", "right": "M4 2l4 4-4 4", "left": "M8 2l-4 4 4 4"}
    return svg(12, 12, '<path d="%s" fill="none" stroke="%s" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>'
               % (paths[direction], t["text"]))


# ---- the game's frame ----------------------------------------------------------------------------------------------
# AMF Witcher 3's DrawGameFrame at scale 1: a 1px outer line, an inner line 3px inside it whose corners step in by 4px.
# Written as nine-slice PNGs (8px slices: the step ends at 7px, inside the corner slice), at 1x only: with @2x files
# beside them, a render at 150% display scaling cut the steps apart (2026-10-05).
# A tree row is drawn one cell at a time, so each colour comes in four pieces:
# -only (a whole frame: lists, single-column rows), -first (left end, lines running off to the right), -middle (top and
# bottom lines) and -last (right end); the sheet picks them by Qt's :only-one / :first / :middle / :last item states.
FRAME_SLICE = 8
FRAME_TILE = 24


def game_frame_strip(colour, alpha, s):
    """One whole frame three tiles wide at scale s; the pieces are cut from it."""
    from PIL import Image, ImageDraw
    w, h = FRAME_TILE * 3 * s, FRAME_TILE * s
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    r, g, b = rgb(colour)
    c = (r, g, b, round(255 * alpha))
    t, gap, n = s, 3 * s, 4 * s

    def hline(x0, x1, y):
        d.rectangle([min(x0, x1), y, max(x0, x1) + t - 1, y + t - 1], fill=c)

    def vline(x, y0, y1):
        d.rectangle([x, min(y0, y1), x + t - 1, max(y0, y1) + t - 1], fill=c)

    R, B = w - t, h - t                       # the outer line's far edges
    hline(0, R, 0); hline(0, R, B); vline(0, 0, B); vline(R, 0, B)
    ax, ay, bx, by = gap, gap, R - gap, B - gap
    hline(ax + n, bx - n, ay); hline(ax + n, bx - n, by)
    vline(ax, ay + n, by - n); vline(bx, ay + n, by - n)
    for cx, sx in ((ax, 1), (bx, -1)):        # the stepped corners
        for cy, sy in ((ay, 1), (by, -1)):
            vline(cx + sx * n, cy, cy + sy * n)
            hline(cx, cx + sx * n, cy + sy * n)
    return im


def game_frames(t, art):
    for name, alpha in (("hover", 0.55), ("selected", 0.95)):
        for s, suffix in ((1, ""),):
            strip = game_frame_strip(t["text"], alpha, s)
            T = FRAME_TILE * s
            pieces = {"first": (0, 0, T, T), "middle": (T, 0, 2 * T, T), "last": (2 * T, 0, 3 * T, T)}
            for piece, box in pieces.items():
                strip.crop(box).save(os.path.join(art, "gameframe-%s-%s%s.png" % (name, piece, suffix)))
            # a whole frame one tile wide
            only = strip.crop((0, 0, T, T))
            only.paste(strip.crop((3 * T - T // 2, 0, 3 * T, T)), (T // 2, 0))
            only.save(os.path.join(art, "gameframe-%s-only%s.png" % (name, suffix)))


NJORDLINGER_LINE = "#dbd6cd"   # the bone grey of Njordlinger's icon set


def recolour_icon(src, dst, colour):
    """Njordlinger's icon in another line colour. SVG: the line colour is swapped in the markup. PNG: every pixel with
    little saturation (the grey lines and their anti-aliasing) takes the new colour with its alpha kept, scaled by its
    brightness relative to the original grey; saturated pixels (the Nexus logo) are left as they are."""
    if src.lower().endswith(".svg"):
        text = open(src, encoding="utf-8").read()
        text = re.sub(re.escape(NJORDLINGER_LINE), colour.lower(), text, flags=re.I)
        open(dst, "w", encoding="utf-8").write(text)
        return
    from PIL import Image
    im = Image.open(src).convert("RGBA")
    px = im.load()
    nr, ng, nb = rgb(colour)
    ref = sum(rgb(NJORDLINGER_LINE)) / 3
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a == 0 or max(r, g, b) - min(r, g, b) > 40:
                continue
            k = min(1.0, ((r + g + b) / 3) / ref)
            px[x, y] = (round(nr * k), round(ng * k), round(nb * k), a)
    im.save(dst)


TOOLBAR = ["instances", "install", "nexus", "modpage", "profiles", "refresh", "executables", "tools", "settings",
           "endorse", "problems", "update", "help"]


def build(t, template, version):
    tok = tokens(t, version)
    folder = os.path.join(OUT, t["title"])
    if os.path.isdir(folder):
        shutil.rmtree(folder)
    os.makedirs(os.path.join(folder, "art"))
    os.makedirs(os.path.join(folder, "icons"))
    sheet = re.sub(r"\$([a-z_]+)\$", lambda m: tok[m.group(1)], template)
    open(os.path.join(OUT, t["title"] + ".qss"), "w", encoding="utf-8", newline="\n").write(sheet)
    art = os.path.join(folder, "art")
    if t["art"]:
        for n in ("frame.png", "background.png") if t.get("background", True) else ("frame.png",):
            shutil.copy2(os.path.join(ROOT, "src", "amf-art", t["art"], n), os.path.join(art, n))
    for st in ("normal", "hover", "pressed", "disabled"):
        open(os.path.join(art, "button%s.svg" % ("" if st == "normal" else "-" + st)), "w", encoding="utf-8").write(button(t, st))
    for k in ("off", "off-hover", "on", "part", "disabled"):
        open(os.path.join(art, "check-%s.svg" % k), "w", encoding="utf-8").write(check(t, k))
    for k in ("off", "off-hover", "on"):
        open(os.path.join(art, "radio-%s.svg" % k), "w", encoding="utf-8").write(radio(t, k))
    if t.get("gameframe"):
        game_frames(t, art)
    for d in ("up", "down", "left", "right"):
        open(os.path.join(art, "arrow-%s.svg" % d), "w", encoding="utf-8").write(arrow(t, d))
    # icons: Njordlinger's set in every theme (the owner: "i like the icons in njordlinger so keep all of them for every
    # theme"), recoloured to the theme ("you can keep the icons but recolor them to fit the themes"): the bone-grey
    # lines take the theme's line colour (AMF's frame colour); saturated pixels (the Nexus logo's orange) and the
    # warning triangle's black fill are kept. src\icons\ is a copy of the Njordlinger MO2 Theme's built icons folder.
    src_icons = os.path.join(ROOT, "src", "icons")
    wanted = sorted(set(re.findall(r"icons/([\w.]+)", sheet)))
    for n in wanted:
        recolour_icon(os.path.join(src_icons, n), os.path.join(folder, "icons", n), t["frame"])
    missing = [u for u in re.findall(r'url\("\./([^"]+)"\)', sheet) if not os.path.isfile(os.path.join(OUT, u))]
    if missing:
        raise SystemExit("%s: the sheet names files that were not written: %s" % (t["title"], ", ".join(sorted(set(missing)))))
    return len(sheet), len(os.listdir(art)), len(wanted)


def main():
    version = open(os.path.join(ROOT, "VERSION"), encoding="utf-8-sig").read().strip()   # issued by the version gate
    template = open(os.path.join(ROOT, "src", "theme.qss.in"), encoding="utf-8").read()
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    size, n_art, n_icons = build(THEME, template, version)
    print("%s %s: %d bytes, %d art, %d icons" % (THEME["title"], version, size, n_art, n_icons))


if __name__ == "__main__":
    main()
