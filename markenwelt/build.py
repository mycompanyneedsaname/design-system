import math, random

random.seed(7)

# ---------- isometric helpers ----------
C30, S30 = math.cos(math.radians(30)), math.sin(math.radians(30))

def iso(x, y, z, s):
    return ((x - y) * C30 * s, (x + y) * S30 * s - z * s)

def pts(lst):
    return " ".join(f"{a:.1f},{b:.1f}" for a, b in lst)

def lerp(p, q, t):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)

def block(x, y, z, w, d, h, s, stroke, top, left, right, hatch=0, sw=1.6, hatch_face="right"):
    P = lambda a, b, c: iso(a, b, c, s)
    T = [P(x, y, z + h), P(x + w, y, z + h), P(x + w, y + d, z + h), P(x, y + d, z + h)]
    L = [P(x, y + d, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x, y + d, z + h)]
    R = [P(x + w, y, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x + w, y, z + h)]
    out = []
    out.append(f'<polygon points="{pts(L)}" fill="{left}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>')
    out.append(f'<polygon points="{pts(R)}" fill="{right}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>')
    out.append(f'<polygon points="{pts(T)}" fill="{top}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>')
    if hatch:
        face = R if hatch_face == "right" else L
        a0, a1, b1, b0 = face[0], face[1], face[2], face[3]
        for i in range(1, hatch):
            t = i / hatch
            p = lerp(a0, a1, t); q = lerp(b0, b1, t)
            out.append(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="{stroke}" stroke-width="1" stroke-opacity=".45"/>')
    return "\n".join(out), T

def bbox(svg_parts):
    import re
    xs, ys = [], []
    for m in re.finditer(r'points="([^"]+)"', svg_parts):
        for pair in m.group(1).split():
            a, b = pair.split(","); xs.append(float(a)); ys.append(float(b))
    return min(xs), min(ys), max(xs), max(ys)

def top_center(T):
    return ((T[0][0] + T[2][0]) / 2, (T[0][1] + T[2][1]) / 2)

# ---------- palette ----------
PETROL = "#0F3B3F"; DEEP = "#071F22"; OCKER = "#D9A441"; PAPER = "#F7F5F0"; SAND = "#E9E1CF"; INK = "#1A1A18"; MIST = "#EEF0EC"
FACE_T = "#14474C"; FACE_L = "#0B3236"; FACE_R = "#0E393D"

def hero_iso():
    s = 34
    parts = []
    g, _ = block(0, 0, 0, 7, 7, 0.35, s, OCKER, FACE_T, FACE_L, FACE_R, sw=1.4)
    parts.append(g)
    specs = [  # x y z w d h label hatch dx dy anchor
        (0.6, 0.6, 0.35, 2.2, 2.2, 2.6, "Druckluft", 5, 0, -58, "middle"),
        (3.6, 0.6, 0.35, 2.4, 2.2, 1.2, "LED", 0, 70, -36, "start"),
        (0.6, 3.6, 0.35, 2.2, 2.4, 3.6, "Abwärme", 6, -78, -30, "end"),
        (3.6, 3.6, 0.35, 2.4, 2.4, 1.9, "PV", 0, 96, 30, "start"),
        (3.6, 3.6, 2.25, 1.1, 1.1, 0.9, "", 0, 0, 0, "start"),
    ]
    labels = []
    for (x, y, z, w, d, h, lab, hatch, dx, dy, anc) in sorted(specs, key=lambda t: (t[0] + t[1], t[2])):
        g, T = block(x, y, z, w, d, h, s, OCKER, FACE_T, FACE_L, FACE_R, hatch=hatch)
        parts.append(g)
        if lab:
            labels.append((lab, top_center(T), dx, dy, anc))
    body = "\n".join(parts)
    x0, y0, x1, y1 = bbox(body)
    pad = 70
    # hand labels
    lab_svg = []
    for lab, (cx, cy), dx, dy, anc in labels:
        lx, ly = cx + dx, cy + dy
        ex = lx if anc == "middle" else (lx - 6 if anc == "start" else lx + 6)
        ey = ly + 6 if dy < 0 else ly - 14
        lab_svg.append(f'<path d="M{ex:.0f} {ey:.0f} Q {(ex+cx)/2:.0f} {(ey+cy)/2 - 10:.0f} {cx:.0f} {cy:.0f}" fill="none" stroke="{OCKER}" stroke-width="1.5" stroke-linecap="round" stroke-dasharray="3 3"/>')
        lab_svg.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="3" fill="{OCKER}"/>')
        lab_svg.append(f'<text x="{lx:.0f}" y="{ly:.0f}" text-anchor="{anc}" font-family="Kalam, cursive" font-size="19" font-weight="700" fill="{OCKER}">{lab}</text>')
    base_lab = f'<text x="{x1-4:.0f}" y="{y1+30:.0f}" text-anchor="end" font-family="Kalam, cursive" font-size="18" font-weight="700" fill="{OCKER}">Grundplatte: Effizienz-Kompass, 2 + 2 Tage</text>'
    base_arrow = ''
    vb = f"{x0-pad:.0f} {y0-pad:.0f} {x1-x0+2*pad:.0f} {y1-y0+2*pad+10:.0f}"
    return f'<svg viewBox="{vb}" class="iso-hero" role="img" aria-label="Isometrische Bausteine Druckluft, LED, Abwärme und PV auf einer Grundplatte Effizienz-Kompass">{body}\n{"".join(lab_svg)}{base_lab}{base_arrow}</svg>'

def module_iso(label, h, hatch, size=30, tone="dark"):
    s = size
    stroke = OCKER if tone == "dark" else PETROL
    if tone == "dark":
        t, l, r = FACE_T, FACE_L, FACE_R
    else:
        t, l, r = "#FFFFFF", SAND, MIST
    g, T = block(0, 0, 0, 2, 2, h, s, stroke, t, l, r, hatch=hatch, sw=1.5)
    x0, y0, x1, y1 = bbox(g)
    return f'<svg viewBox="{x0-6:.0f} {y0-6:.0f} {x1-x0+12:.0f} {y1-y0+12:.0f}" aria-hidden="true">{g}</svg>'

def poster_iso():
    s = 40
    parts = []
    specs = [(0, 0, 0, 2, 2, 1.2, 4), (2.4, 0, 0, 2, 2, 2.2, 0), (0, 2.4, 0, 2, 2, 3.1, 6), (2.4, 2.4, 0, 2, 2, 1.6, 0), (2.4, 2.4, 1.6, 2, 2, 1.4, 5)]
    for (x, y, z, w, d, h, hatch) in sorted(specs, key=lambda t: (t[0] + t[1], t[2])):
        g, _ = block(x, y, z, w, d, h, s, OCKER, FACE_T, FACE_L, FACE_R, hatch=hatch)
        parts.append(g)
    body = "\n".join(parts)
    x0, y0, x1, y1 = bbox(body)
    return f'<svg viewBox="{x0-20:.0f} {y0-20:.0f} {x1-x0+40:.0f} {y1-y0+40:.0f}" aria-hidden="true">{body}</svg>'

# ---------- hand-drawn primitives (inline reuse) ----------
STRIKE = '<svg class="strike" viewBox="0 0 200 20" preserveAspectRatio="none" aria-hidden="true"><path d="M2 12 Q 50 4 100 10 T 198 8" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"/></svg>'
CIRCLE = '<svg class="ring" viewBox="0 0 120 60" preserveAspectRatio="none" aria-hidden="true"><path d="M16 30 C 10 8, 60 2, 96 10 C 122 16, 118 46, 70 54 C 30 60, 4 48, 12 26 C 16 16, 30 10, 42 10" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg>'
CHECK = '<svg viewBox="0 0 40 40" width="28" height="28" aria-hidden="true"><path d="M6 22 q 6 4 11 12 q 6 -20 18 -30" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARROW = '<svg viewBox="0 0 120 60" width="90" height="45" aria-hidden="true"><path d="M6 48 Q 40 6 106 22" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/><path d="M92 8 l16 14 -20 8" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def logo(curve, dot, text, size=64, w1=22, sub=True, mono=None):
    subhtml = f'<div class="zs" style="color:{mono or text}">Büro für Energie- und<br>Ressourceneffizienz</div>' if sub else ""
    return (f'<div class="logo" style="color:{text}"><svg viewBox="0 0 64 64" width="{size}" height="{size}" aria-hidden="true">'
            f'<path d="M6 52 C 30 52 34 12 58 12" fill="none" stroke="{curve}" stroke-width="4.5" stroke-linecap="round"/>'
            f'<circle cx="32" cy="32" r="5.5" fill="{dot}"/></svg>'
            f'<div><div class="w1" style="font-size:{w1}px">Wendepunkt</div><div class="w2" style="font-size:{w1}px">Ingenieure</div>{subhtml}</div></div>')

ICONS = {
 "Messen": '<path d="M7 30 A 13 13 0 1 1 33 30"/><path d="M20 27 l 7 -11"/><circle cx="20" cy="28" r="1.6" fill="currentColor" stroke="none"/><path d="M6 33 h28"/>',
 "Nachrechnen": '<path d="M10 5 l 21 1 -1 29 -21 -1 z"/><path d="M15 13 h11 M15 19 h7 M15 25 h11"/><path d="M27 21 q -2 4 1 7" />',
 "Priorisieren": '<path d="M9 12 h20 M9 20 h13 M9 28 h7"/><path d="M6 9 C 4 4, 32 3, 33 9 C 35 14, 24 17, 8 15 C 3 14, 2 11, 6 9" stroke-opacity=".9"/>',
 "Umsetzen": '<path d="M6 32 L 18 20"/><path d="M16 15 l 9 -9 8 8 -9 9 z"/><path d="M25 6 l 5 -3 M33 14 l 3 -5"/>',
 "Handwerk": '<path d="M8 33 L 20 21"/><path d="M17 12 l 10 -6 6 6 -6 10"/><path d="M14 16 l 8 8"/>',
 "Strom": '<path d="M22 4 l -11 18 h 9 l -4 15 l 13 -20 h -9 z"/>',
 "Wärme": '<path d="M12 33 c 0 -7 6 -7 6 -13 s -6 -7 -6 -13"/><path d="M22 33 c 0 -7 6 -7 6 -13 s -6 -7 -6 -13"/>',
 "Material": '<path d="M7 24 l 13 7 13 -7 -13 -7 z"/><path d="M7 16 l 13 7 13 -7"/><path d="M7 8 l 13 7 13 -7 -13 -7 z"/>',
 "Wasser": '<path d="M20 5 c 6 9 10 14 10 19 a 10 10 0 0 1 -20 0 c 0 -5 4 -10 10 -19 z"/><path d="M15 24 q 0 5 5 6"/>',
 "Abwärme": '<path d="M12 34 v -16 h 8 v 16"/><path d="M8 34 h 26"/><path d="M24 12 c 4 -3 4 -6 0 -9 M30 16 c 4 -3 4 -6 0 -9"/>',
 "PV": '<path d="M6 30 l 6 -16 h 22 l -6 16 z"/><path d="M11 22 h 20 M14 14 l -3 8 M23 14 l -3 16"/><path d="M6 34 h 28"/>',
 "Speicher": '<path d="M7 12 h 24 v 18 h -24 z"/><path d="M31 17 h 4 v 8 h -4"/><path d="M12 17 v 8 M18 17 v 8"/>',
}

def icon(name, color="currentColor", size=44):
    return (f'<svg viewBox="0 0 40 40" width="{size}" height="{size}" fill="none" stroke="{color}" stroke-width="2.2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')

MODULES = [("Messen", 1.0, 0), ("Nachrechnen", 1.4, 4), ("Priorisieren", 1.8, 0), ("Umsetzen", 2.2, 5), ("Handwerk", 1.2, 0), ("Strom", 2.0, 4),
           ("Wärme", 1.6, 0), ("Material", 1.3, 4), ("Wasser", 1.1, 0), ("Abwärme", 2.4, 5), ("PV", 0.9, 0), ("Speicher", 1.7, 4)]

def modules_html():
    out = []
    for name, h, hatch in MODULES:
        out.append(f'<div class="mod"><div class="mod-iso">{module_iso(name, h, hatch)}</div><div class="mod-ic">{icon(name, OCKER, 30)}</div><b>{name}</b></div>')
    return "\n".join(out)

def icons_html():
    return "\n".join(f'<div class="hic">{icon(n, OCKER, 40)}<span>{n}</span></div>' for n, _, _ in MODULES)

html = f'''<title>Wendepunkt Markenwelt</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&family=Kalam:wght@400;700&display=swap">
<style>
  :root{{
    --petrol:{PETROL}; --deep:{DEEP}; --ocker:{OCKER}; --paper:{PAPER}; --sand:{SAND}; --ink:{INK}; --mist:{MIST};
    --line-l:#D8D3C8; --line-d:rgba(255,255,255,.14); --muted:#4E5A5B;
    --sans:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
    --mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
    --hand:"Kalam","Segoe Print","Bradley Hand",cursive;
  }}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:16px;line-height:1.55;-webkit-font-smoothing:antialiased}}
  h1,h2,h3,h4{{margin:0;line-height:1.1;text-wrap:balance;font-weight:600;letter-spacing:-.02em}}
  p{{margin:0}}
  a{{color:inherit}}
  a:focus-visible,button:focus-visible{{outline:2px solid var(--ocker);outline-offset:3px}}
  .wrap{{max-width:1200px;margin:0 auto;padding-inline:24px}}
  section{{padding-block:72px}}
  .dark{{background:var(--petrol);color:#fff}}
  .deep{{background:var(--deep);color:#fff}}
  .dots{{background-image:radial-gradient(rgba(217,164,65,.28) 1.1px,transparent 1.2px);background-size:22px 22px}}
  .sand{{background:var(--sand)}}
  .mist{{background:var(--mist)}}
  .eyebrow{{font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase;opacity:.75}}
  .hand{{font-family:var(--hand);font-weight:700;line-height:1.15}}
  .tag{{display:inline-block;font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;padding:5px 9px;border:1px solid currentColor}}
  .dark .tag,.deep .tag{{color:var(--ocker)}}
  .grid2{{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center}}
  .grid3{{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}}
  .grid4{{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}}
  .lede{{font-size:19px;max-width:58ch}}
  .muted{{color:var(--muted)}}
  .dark .muted,.deep .muted{{color:rgba(255,255,255,.72)}}
  .sec-head{{margin-bottom:36px;max-width:70ch}}
  .sec-head h2{{font-size:clamp(28px,3.4vw,42px);margin-top:10px}}
  .sec-head p{{margin-top:14px;font-size:17px}}

  /* logo */
  .logo{{display:flex;align-items:center;gap:14px;font-family:var(--sans);line-height:1.02}}
  .logo .w1{{font-weight:600;letter-spacing:-.015em}}
  .logo .w2{{font-weight:400;letter-spacing:-.01em}}
  .logo .zs{{font-family:var(--mono);font-size:8.5px;letter-spacing:.04em;margin-top:6px;line-height:1.25}}

  /* top bar */
  .top{{display:flex;justify-content:space-between;align-items:center;padding-block:20px;border-bottom:1px solid var(--line-d)}}
  .top ul{{display:flex;gap:26px;list-style:none;margin:0;padding:0;font-size:14px}}
  .top .meta{{font-family:var(--mono);font-size:12px;opacity:.7}}

  /* hero */
  .hero{{padding-block:64px 80px}}
  .hero h1{{font-size:clamp(40px,5vw,64px);line-height:1.02;margin-top:22px}}
  .hero .sub{{margin-top:22px;font-size:19px;max-width:46ch}}
  .cta{{display:inline-block;background:var(--ocker);color:var(--deep);font:600 15px/1 var(--sans);padding:15px 20px;border:0;text-decoration:none;white-space:nowrap}}
  .cta.ghost{{background:transparent;color:#fff;border:1px solid var(--line-d)}}
  .actions{{display:flex;gap:14px;align-items:center;margin-top:30px;flex-wrap:wrap}}
  .iso-hero{{width:100%;max-width:560px;height:auto;display:block;margin-inline:auto}}

  /* signature device: Behauptung → nachgerechnet */
  .claim{{display:block}}
  .claim .struck{{display:inline;color:rgba(255,255,255,.5);-webkit-box-decoration-break:clone;box-decoration-break:clone;
    background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 20' preserveAspectRatio='none'%3E%3Cpath d='M2 12 Q 50 4 100 10 T 198 8' fill='none' stroke='%23D9A441' stroke-width='4' stroke-linecap='round'/%3E%3C/svg%3E") no-repeat center / 100% .5em}}
  .claim .re{{display:block;font-family:var(--hand);font-weight:700;color:var(--ocker);font-size:.7em;line-height:1.05;margin-top:.18em;letter-spacing:0;transform:rotate(-1.5deg);transform-origin:left}}
  .light .claim .struck{{color:rgba(26,26,24,.42);
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 20' preserveAspectRatio='none'%3E%3Cpath d='M2 12 Q 50 4 100 10 T 198 8' fill='none' stroke='%230F3B3F' stroke-width='4' stroke-linecap='round'/%3E%3C/svg%3E")}}
  .light .claim .re{{color:var(--petrol)}}
  .ring{{position:absolute;left:-10%;top:-28%;width:120%;height:156%;pointer-events:none}}
  .ringed{{position:relative;display:inline-block;padding:0 .12em}}

  /* prinzip */
  .prinzip{{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--line-l);border:1px solid var(--line-l)}}
  .prinzip > div{{background:var(--paper);padding:26px 24px 28px;min-height:250px;display:flex;flex-direction:column;justify-content:space-between;gap:20px}}
  .prinzip .big{{font-size:26px;font-weight:600;letter-spacing:-.02em;line-height:1.15}}
  .prinzip .k{{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}}
  .prinzip .why{{font-size:14px;color:var(--muted)}}

  /* baukasten */
  .mods{{display:grid;grid-template-columns:repeat(6,1fr);gap:14px}}
  .mod{{display:grid;grid-template-rows:auto auto auto;gap:8px;justify-items:center;text-align:center;padding:16px 8px 14px;border:1px solid var(--line-d)}}
  .mod-iso svg{{width:86px;height:auto;display:block}}
  .mod b{{font-weight:500;font-size:13.5px}}
  .mod-ic svg{{display:block}}

  /* hand icons */
  .hicons{{display:grid;grid-template-columns:repeat(6,1fr);gap:1px;background:var(--line-d);border:1px solid var(--line-d)}}
  .hic{{background:var(--deep);display:grid;justify-items:center;gap:8px;padding:18px 8px 14px;font-size:13px}}
  .hic svg{{display:block}}

  /* photo treatment */
  .photo{{position:relative;background:#2E3634;min-height:420px;overflow:hidden}}
  .photo .base{{position:absolute;inset:0;width:100%;height:100%}}
  .photo .ann{{position:absolute;inset:0;width:100%;height:100%}}
  .photo .cap{{position:absolute;left:16px;bottom:16px;font-family:var(--mono);font-size:12px;background:rgba(7,31,34,.85);color:#fff;padding:6px 10px}}

  /* posters */
  .posters{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}}
  .poster{{aspect-ratio:3/4;position:relative;padding:22px;display:flex;flex-direction:column;justify-content:space-between;overflow:hidden}}
  .poster .art{{flex:1;display:flex;align-items:center;justify-content:center;min-height:0}}
  .poster .art svg{{width:78%;height:auto;max-height:100%}}
  .poster .line{{font-size:15px;line-height:1.3;max-width:24ch}}
  .poster .foot{{display:flex;justify-content:space-between;font-family:var(--mono);font-size:10px;letter-spacing:.06em;text-transform:uppercase;opacity:.8}}

  /* applications */
  .apps{{display:grid;grid-template-columns:1.1fr .9fr;gap:20px}}
  .apps .col{{display:grid;gap:20px}}
  .report{{background:#fff;border:1px solid var(--line-l);aspect-ratio:210/297;padding:8%;display:flex;flex-direction:column;justify-content:space-between;position:relative}}
  .report h3{{font-size:clamp(22px,2.6vw,34px);margin-top:14px}}
  .report .num{{font-family:var(--mono);font-size:clamp(40px,5vw,64px);font-weight:500;line-height:1;letter-spacing:-.03em;color:var(--petrol)}}
  .report table{{border-collapse:collapse;width:100%;font-size:12px;font-variant-numeric:tabular-nums}}
  .report td,.report th{{text-align:left;padding:6px 0;border-bottom:1px solid var(--line-l)}}
  .report th{{font-family:var(--mono);font-weight:500;font-size:10px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}}
  .report td.n,.report th.n{{text-align:right;font-family:var(--mono)}}
  .report .stamp{{position:absolute;right:8%;top:50%;transform:rotate(-8deg);color:var(--petrol);display:flex;align-items:center;gap:6px;font-family:var(--hand);font-weight:700;font-size:22px}}
  .card{{aspect-ratio:85/55;padding:18px 20px;display:flex;flex-direction:column;justify-content:space-between;border:1px solid var(--line-l);position:relative;overflow:hidden}}
  .card .who{{font-size:12px;line-height:1.4}}
  .card .who b{{font-size:13px}}
  .card .who .m{{font-family:var(--mono);font-size:10px}}
  .li{{aspect-ratio:1;background:var(--deep);color:#fff;padding:9%;display:flex;flex-direction:column;justify-content:space-between}}
  .li .q{{font-size:clamp(22px,2.6vw,32px);font-weight:600;letter-spacing:-.02em;line-height:1.12}}
  .li .foot{{display:flex;justify-content:space-between;align-items:flex-end;font-family:var(--mono);font-size:11px;opacity:.85}}
  .sig{{background:#fff;border:1px solid var(--line-l);padding:18px 20px;font-size:13px;line-height:1.45}}
  .sig .m{{font-family:var(--mono);font-size:12px}}

  /* system */
  .sw{{display:grid;grid-template-columns:repeat(6,1fr);gap:10px}}
  .sw > div{{border:1px solid var(--line-l);background:#fff}}
  .sw .chip{{height:70px}}
  .sw .lbl{{padding:8px 9px;font-size:12px;line-height:1.35}}
  .sw .lbl b{{display:block;font-weight:600}}
  .sw .lbl code{{font-family:var(--mono);font-size:11px;color:var(--muted)}}
  .type{{display:grid;gap:0;border:1px solid var(--line-l);background:#fff}}
  .type .row{{display:grid;grid-template-columns:150px 1fr;gap:16px;align-items:baseline;padding:16px 18px;border-top:1px solid var(--line-l)}}
  .type .row:first-child{{border-top:0}}
  .type .k{{font-family:var(--mono);font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}}
  .rules{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}}
  .rules > div{{border-top:3px solid var(--petrol);padding-top:14px}}
  .rules h4{{font-size:15px;margin-bottom:6px}}
  .rules p{{font-size:14px;color:var(--muted)}}
  .src{{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--line-l);border:1px solid var(--line-l)}}
  .src > div{{background:#fff;padding:20px 22px}}
  .src h4{{font-size:15px;margin-bottom:8px}}
  .src ul{{margin:0;padding-left:18px;font-size:14px;color:var(--muted)}}
  .src li{{margin:4px 0}}
  .src .no{{margin-top:10px;font-size:13px;color:var(--muted)}}
  .src .no b{{color:var(--ink)}}

  @media (max-width:980px){{
    .grid2,.apps{{grid-template-columns:1fr}}
    .grid3,.prinzip,.posters,.rules,.src{{grid-template-columns:1fr}}
    .grid4{{grid-template-columns:1fr 1fr}}
    .mods{{grid-template-columns:repeat(3,1fr)}}
    .hicons{{grid-template-columns:repeat(4,1fr)}}
    .sw{{grid-template-columns:repeat(3,1fr)}}
    .top ul{{display:none}}
    section{{padding-block:56px}}
  }}
  @media (max-width:520px){{
    .mods,.hicons{{grid-template-columns:repeat(2,1fr)}}
    .sw{{grid-template-columns:repeat(2,1fr)}}
    .type .row{{grid-template-columns:1fr}}
  }}
</style>

<!-- ============================ HERO ============================ -->
<header class="dark dots">
  <div class="wrap">
    <div class="top">
      {logo("#FFFFFF", OCKER, "#FFFFFF", size=34, w1=15, sub=False)}
      <ul><li>Effizienz-Kompass</li><li>Baukasten</li><li>Praxisbeispiele</li><li>Büro</li></ul>
      <span class="meta">Markenwelt · Entwurf 4 · nach Moodboard 24.09.</span>
    </div>
    <div class="hero grid2">
      <div>
        <span class="tag">Büro für Energie- und Ressourceneffizienz</span>
        <h1>
          <span class="claim"><span class="struck">Bis zu 40 % Energie sparen!</span><span class="re">nachgerechnet: 18 %, amortisiert in 2,1 Jahren.</span></span>
        </h1>
        <p class="sub">Wir messen in Ihrem Betrieb, rechnen jede Behauptung nach und bauen daraus einen Maßnahmen-Baukasten, den Ihr Team selbst versteht. Energie und Material, nicht nur Strom.</p>
        <div class="actions"><a class="cta" href="#kompass">Kostenfreies Erstgespräch</a><a class="cta ghost" href="#baukasten">Den Baukasten ansehen</a></div>
      </div>
      <div>{hero_iso()}</div>
    </div>
  </div>
</header>

<!-- ============================ PRINZIP ============================ -->
<section class="light" id="kompass">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Das Signaturelement</span>
      <h2>Behauptung gedruckt. Strich mit dem Marker. Ergebnis von Hand.</h2>
      <p class="muted">Das ist die Marke in einem Bild: Jemand hat das Angebot der Branche gelesen, den Marker genommen und nachgerechnet. Der Strich ist Ocker, die Handschrift ist Kalam, die Zahl hat immer Einheit und Kontext. Das Element funktioniert in Headline, Anzeige, LinkedIn-Post und auf dem Berichtsdeckblatt.</p>
    </div>
    <div class="prinzip">
      <div>
        <span class="k">Beispiel 01 · Amortisation</span>
        <div class="big"><span class="claim"><span class="struck">Rechnet sich sofort.</span><span class="re">Druckluft: 5 Monate. LED: 3,3 Jahre. Beides steht im Bericht.</span></span></div>
        <p class="why">Keine pauschale ROI-Zahl, wie im Briefing verlangt. Die Handschrift liefert die Zahl mit Kontext.</p>
      </div>
      <div>
        <span class="k">Beispiel 02 · Floskel</span>
        <div class="big"><span class="claim"><span class="struck">Ganzheitlich nachhaltig.</span><span class="re">312 MWh Strom, 41 t Stahl, 19 t CO₂. Gemessen, nicht geschätzt.</span></span></div>
        <p class="why">Das Wortfeld aus dem Briefing wird wörtlich durchgestrichen. Was bleibt, hat eine Einheit.</p>
      </div>
      <div>
        <span class="k">Beispiel 03 · Beratersprech</span>
        <div class="big"><span class="claim"><span class="struck">Transformation begleiten.</span><span class="re">12 Maßnahmen, priorisiert. Vier davon unter 6 Monaten.</span></span></div>
        <p class="why">So klingt der Satz, den ein Geschäftsführer nach dem ersten Gespräch weiterverwendet.</p>
      </div>
    </div>
  </div>
</section>

<!-- ============================ BAUKASTEN ============================ -->
<section class="deep dots" id="baukasten">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Das Produkt als Bild</span>
      <h2>Der modulare Effizienz-Baukasten</h2>
      <p class="muted">Jede Leistung und jede Maßnahme ist ein Baustein, gezeichnet wie auf einem Werkstattplan. Der Effizienz-Kompass ist die Grundplatte: zwei Tage vor Ort, zwei Tage Planung, danach setzt der Kunde die Steine in seiner Reihenfolge. Die Höhe eines Steins zeigt, wie viel er bringt; die Schraffur zeigt, was schon umgesetzt ist.</p>
    </div>
    <div class="mods">
      {modules_html()}
    </div>
    <p class="muted" style="margin-top:22px;font-size:14px;max-width:70ch">Die Bausteine ersetzen die klassischen Leistungskacheln der Branche. Auf der Website werden sie zur Konfiguration: Der Kunde klickt seine Steine, die Grundplatte zeigt Tage und Umfang. Im Bericht sind sie die Kapitelmarken.</p>
  </div>
</section>

<!-- ============================ ICONS + FOTO ============================ -->
<section class="dark">
  <div class="wrap grid2" style="align-items:start">
    <div>
      <span class="eyebrow">Icon-Sprache</span>
      <h2 style="font-size:30px;margin-top:10px">Ein Strich, mit der Hand, in Ocker.</h2>
      <p class="muted" style="margin-top:12px;font-size:15px;max-width:48ch">Zwölf Icons für Leistungen und Medien. Bewusst nicht perfekt: leicht gewellte Linien, runde Enden, wie mit dem Filzstift auf den Schaltschrank gezeichnet. Auf hellem Grund werden sie Petrol.</p>
      <div class="hicons" style="margin-top:22px">
        {icons_html()}
      </div>
    </div>
    <div>
      <span class="eyebrow">Fotografie</span>
      <h2 style="font-size:30px;margin-top:10px">Echte Halle, Marker drüber.</h2>
      <p class="muted" style="margin-top:12px;font-size:15px;max-width:48ch">Reportagefotos aus Betrieben, entsättigt in Richtung Petrol. Darüber die Annotation des Ingenieurs: Was wurde gemessen, was wurde gefunden. Das Foto beweist, dass wir da waren; die Handschrift beweist, dass wir gerechnet haben.</p>
      <div class="photo" style="margin-top:22px">
        <svg class="base" viewBox="0 0 600 420" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
          <rect width="600" height="420" fill="#2A3331"/>
          <rect x="0" y="300" width="600" height="120" fill="#232B29"/>
          <g fill="none" stroke="#5A6663" stroke-width="2">
            <rect x="120" y="120" width="170" height="180"/><rect x="140" y="140" width="60" height="70"/><rect x="220" y="140" width="50" height="40"/>
            <circle cx="400" cy="200" r="70"/><circle cx="400" cy="200" r="52"/><rect x="330" y="270" width="140" height="30"/>
            <path d="M290 160 h40 M470 200 h80 M40 300 h520 M60 120 v180 M540 90 v210"/>
          </g>
          <rect width="600" height="420" fill="{PETROL}" fill-opacity=".35"/>
        </svg>
        <svg class="ann" viewBox="0 0 600 420" aria-hidden="true">
          <path d="M330 140 C 320 100, 470 92, 486 150 C 500 200, 470 262, 400 268 C 330 274, 312 220, 322 170 C 326 150, 340 140, 356 136" fill="none" stroke="{OCKER}" stroke-width="3.5" stroke-linecap="round"/>
          <path d="M200 70 Q 270 40 330 120" fill="none" stroke="{OCKER}" stroke-width="2.5" stroke-linecap="round"/>
          <path d="M318 96 l 12 24 -26 -2" fill="none" stroke="{OCKER}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
          <text x="44" y="62" font-family="Kalam, cursive" font-weight="700" font-size="24" fill="{OCKER}">Kompressor 2: Leckage</text>
          <text x="44" y="92" font-family="Kalam, cursive" font-weight="700" font-size="24" fill="{OCKER}">11.200 € / Jahr · 5 Monate</text>
          <path d="M60 330 q 12 8 18 22 q 10 -34 34 -50" fill="none" stroke="{OCKER}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
          <text x="128" y="352" font-family="Kalam, cursive" font-weight="700" font-size="22" fill="{OCKER}">gemessen 12.09., 14:10</text>
        </svg>
        <span class="cap">Platzhalter für Foto: Druckluftstation, Tageslicht, keine Freisteller.</span>
      </div>
    </div>
  </div>
</section>

<!-- ============================ POSTER ============================ -->
<section class="light">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Plakatserie</span>
      <h2>Drei Motive, die auch ohne Text erkannt werden.</h2>
      <p class="muted">Für Büro, Messe und LinkedIn. Sand, Petrol und Ocker im Wechsel, jedes Motiv mit einer handgezeichneten Linie. Kein Foto, kein Windrad, keine Glühbirne.</p>
    </div>
    <div class="posters">
      <div class="poster sand" style="color:{PETROL}">
        <div class="foot"><span>Wendepunkt Ingenieure</span><span>01 · Kurve</span></div>
        <div class="art"><svg viewBox="0 0 200 200" aria-hidden="true"><path d="M18 168 C 60 172, 66 130, 96 104 C 128 76, 128 30, 184 26" fill="none" stroke="{PETROL}" stroke-width="7" stroke-linecap="round"/><circle cx="100" cy="100" r="13" fill="{OCKER}"/><path d="M118 112 q 30 24 52 6" fill="none" stroke="{PETROL}" stroke-width="2.4" stroke-linecap="round"/><text x="132" y="146" font-family="Kalam, cursive" font-weight="700" font-size="17" fill="{PETROL}">hier.</text></svg></div>
        <p class="line">Der Wendepunkt ist der Moment, ab dem die Kurve anders läuft. Wir suchen ihn in Ihrem Betrieb.</p>
      </div>
      <div class="poster" style="background:{PETROL};color:#fff">
        <div class="foot"><span>Wendepunkt Ingenieure</span><span>02 · Baukasten</span></div>
        <div class="art">{poster_iso()}</div>
        <p class="line">Zehn Maßnahmen in vier Tagen. Priorisiert, durchgerechnet, in Ihrer Reihenfolge gebaut.</p>
      </div>
      <div class="poster" style="background:{OCKER};color:{DEEP}">
        <div class="foot"><span>Wendepunkt Ingenieure</span><span>03 · Marker</span></div>
        <div class="art"><svg viewBox="0 0 200 200" aria-hidden="true"><text x="18" y="86" font-family="IBM Plex Sans, sans-serif" font-weight="600" font-size="27" fill="{DEEP}" fill-opacity=".45">behaupten.</text><path d="M12 78 Q 80 64 160 74" fill="none" stroke="{DEEP}" stroke-width="7" stroke-linecap="round"/><text x="16" y="146" font-family="Kalam, cursive" font-weight="700" font-size="30" fill="{DEEP}">nachrechnen.</text><path d="M18 156 q 60 10 150 -4" fill="none" stroke="{DEEP}" stroke-width="3" stroke-linecap="round"/></svg></div>
        <p class="line">Wir rechnen nach, statt zu behaupten. Jede Zahl im Bericht hat eine Einheit und ein Datum.</p>
      </div>
    </div>
  </div>
</section>

<!-- ============================ ANWENDUNG ============================ -->
<section class="mist">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Anwendung</span>
      <h2>Bericht, Karte, Post, Signatur.</h2>
      <p class="muted">Der Bericht ist das wichtigste Stück, weil der Kunde ihn behält. Papierweiß, Plex, Zahlen in Mono. Die Hand kommt genau einmal vor: als Prüfvermerk der beiden Gründer.</p>
    </div>
    <div class="apps">
      <div class="report">
        <div>
          {logo(PETROL, OCKER, PETROL, size=44, w1=15)}
          <span class="eyebrow" style="display:block;margin-top:34px;color:var(--muted)">Effizienz-Kompass · Bericht Nr. 2026-014</span>
          <h3>Gießerei Musterwerk GmbH, Saalfeld</h3>
          <div class="num" style="margin-top:22px">12 Maßnahmen</div>
          <p class="muted" style="font-size:13px;margin-top:6px">64.300 € Invest für die ersten vier · Amortisation ≤ 2,5 Jahre · 19 t CO₂ p. a.</p>
        </div>
        <div class="stamp">{CHECK}<span>nachgerechnet MS / TW</span></div>
        <table>
          <thead><tr><th>Maßnahme</th><th class="n">Invest</th><th class="n">Einsparung p. a.</th><th class="n">Amort.</th></tr></thead>
          <tbody>
            <tr><td>Druckluft-Leckagen beheben</td><td class="n">4.800 €</td><td class="n">11.200 €</td><td class="n">5 Mon.</td></tr>
            <tr><td>Verschnitt Stanzlinie 3</td><td class="n">12.500 €</td><td class="n">9.800 €</td><td class="n">1,3 J.</td></tr>
            <tr><td>Abwärme Härteofen nutzen</td><td class="n">38.000 €</td><td class="n">19.500 €</td><td class="n">2,0 J.</td></tr>
            <tr><td>Pumpen mit Frequenzumrichter</td><td class="n">9.000 €</td><td class="n">3.600 €</td><td class="n">2,5 J.</td></tr>
          </tbody>
        </table>
      </div>
      <div class="col">
        <div class="li">
          <div class="foot"><span>Praxisbeispiel · Folienhersteller</span><span>1080 × 1080</span></div>
          <div class="q"><span class="claim"><span class="struck">„PV rechnet sich immer.“</span><span class="re">240 kWp, 31.000 € p. a.: 6,8 Jahre. Rechnet sich. Aber erst nach Druckluft und Abwärme.</span></span></div>
          <div class="foot">{logo("#FFFFFF", OCKER, "#FFFFFF", size=26, w1=11, sub=False)}<span>wendepunkt-ingenieure.de</span></div>
        </div>
        <div class="grid2" style="gap:12px;align-items:stretch">
          <div class="card" style="background:#fff">
            {logo(PETROL, OCKER, PETROL, size=30, w1=11, sub=False)}
            <div class="who"><b>Michael Schenk</b><br>Ressourceneffizienz<br><span class="m">+49 000 0000000 · ms@wendepunkt-ingenieure.de</span></div>
          </div>
          <div class="card" style="background:{PETROL};border-color:{PETROL};justify-content:center;align-items:center">
            <svg viewBox="0 0 64 64" width="120" height="120" style="position:absolute;right:-22px;bottom:-30px" aria-hidden="true"><path d="M6 52 C 30 52 34 12 58 12" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round"/><circle cx="32" cy="32" r="5.5" fill="{OCKER}"/></svg>
            <span class="hand" style="color:{OCKER};font-size:20px;position:absolute;left:18px;top:18px;transform:rotate(-4deg)">Ruf einfach an.</span>
          </div>
        </div>
        <div class="sig">
          <b>Tobias Wintsche</b> · Energietechnik<br>
          Wendepunkt Ingenieure GbR · Büro für Energie- und Ressourceneffizienz<br>
          <span class="m">+49 000 0000000 · tw@wendepunkt-ingenieure.de · Leipzig / Thüringen</span><br>
          <span class="hand" style="color:{PETROL};font-size:15px">Wir rechnen nach, statt zu behaupten.</span>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ============================ SYSTEM ============================ -->
<section class="light">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Mini-System</span>
      <h2>Farben, Schriften, drei Regeln.</h2>
    </div>
    <div class="sw">
      <div><div class="chip" style="background:{PETROL}"></div><div class="lbl"><b>Petrol</b><code>{PETROL}</code></div></div>
      <div><div class="chip" style="background:{DEEP}"></div><div class="lbl"><b>Tiefe</b><code>{DEEP}</code></div></div>
      <div><div class="chip" style="background:{OCKER}"></div><div class="lbl"><b>Ocker · Marker</b><code>{OCKER}</code></div></div>
      <div><div class="chip" style="background:{PAPER};border-bottom:1px solid var(--line-l)"></div><div class="lbl"><b>Papier</b><code>{PAPER}</code></div></div>
      <div><div class="chip" style="background:{SAND}"></div><div class="lbl"><b>Sand</b><code>{SAND}</code></div></div>
      <div><div class="chip" style="background:{MIST}"></div><div class="lbl"><b>Nebel</b><code>{MIST}</code></div></div>
    </div>
    <div class="type" style="margin-top:24px">
      <div class="row"><span class="k">Headline · Plex Sans 600</span><span style="font-size:30px;font-weight:600;letter-spacing:-.02em;line-height:1.1">Systeme, die Ihr Team noch versteht.</span></div>
      <div class="row"><span class="k">Fließtext · Plex Sans 400</span><span style="font-size:16px">Zwei Tage vor Ort, zwei Tage Planung. Danach liegen mindestens zehn Maßnahmen auf dem Tisch.</span></div>
      <div class="row"><span class="k">Zahl · Plex Mono 500</span><span style="font-family:var(--mono);font-size:30px;font-weight:500;color:{PETROL};line-height:1">312 MWh <span style="font-size:13px;color:var(--muted)">Strom p. a.</span></span></div>
      <div class="row"><span class="k">Hand · Kalam 700</span><span class="hand" style="font-size:28px;color:{PETROL}">nachgerechnet: 18 %, 2,1 Jahre</span></div>
    </div>
    <div class="rules" style="margin-top:32px">
      <div><h4>Die Hand ist selten.</h4><p>Eine Annotation pro Bildschirm, ein Prüfvermerk pro Bericht. Handschrift ist nie Fließtext und nie Navigation. Sie ist der Marker des Ingenieurs, nicht eine zweite Schrift.</p></div>
      <div><h4>Ocker ist Marker, nicht Text.</h4><p>Auf Petrol erreicht Ocker 5,4 : 1 und trägt Handschrift und Icons. Auf Papier ist es nur Strich, Punkt oder Fläche mit dunkler Schrift. Petrol übernimmt Buttons, Kennzahlen und Links.</p></div>
      <div><h4>Dunkel für die Bühne, hell für das Dokument.</h4><p>Hero, Plakat, LinkedIn und Baukasten auf Petrol oder Tiefe mit Punktraster. Bericht, Angebot, Brief und Formular auf Papier. Das Logo läuft auf beidem.</p></div>
    </div>
  </div>
</section>

<!-- ============================ HERKUNFT ============================ -->
<section class="sand">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Herkunft</span>
      <h2>Was aus dem Moodboard übernommen wurde, und was nicht.</h2>
    </div>
    <div class="src">
      <div>
        <h4>ecoworks</h4>
        <ul><li>Dunkler Petrol-Grund mit Punktraster</li><li>Isometrische Bausteine als Produktbild</li><li>Schraffuren als Zustand, nicht als Deko</li><li>Kleine Label in Mono</li></ul>
        <p class="no"><b>Nicht übernommen:</b> das Neongrün. Es liegt zu nah am Energieberater-Grün und wäre eine Kopie.</p>
      </div>
      <div>
        <h4>The Academy for Climate Jobs</h4>
        <ul><li>Durchstreichen und von Hand korrigieren</li><li>Marker-Kreis um das, was zählt</li><li>Handgezeichnete Icons auf dunklem Grund</li><li>Fotos mit Annotation darüber</li></ul>
        <p class="no"><b>Nicht übernommen:</b> Kreisel-Kritzeleien um Gesichter und die Textmarker-Farbe. Bei uns markiert die Hand Zahlen, nicht Menschen.</p>
      </div>
      <div>
        <h4>Claude / Anthropic</h4>
        <ul><li>Warmes Papier und Sand statt Reinweiß</li><li>Plakatserie mit einer Linie pro Motiv</li><li>Ruhige Grotesk, Mono für Zahlen</li><li>Geschäftsausstattung als Gegenstand gedacht</li></ul>
        <p class="no"><b>Nicht übernommen:</b> Terrakotta. Die Farbe gehört Anthropic. Unser Ocker kommt aus dem Logo-Punkt.</p>
      </div>
    </div>
    <p class="muted" style="margin-top:28px;font-size:14px;max-width:72ch">Offen zur Entscheidung: Ob die Handschrift Kalam bleibt oder durch die echte Handschrift von Micha oder Tobias ersetzt wird. Das wäre der ehrlichste Marker und rechtlich sauber. Dafür brauche ich eine Seite mit den Ziffern 0 bis 9, dem Prozentzeichen, „Jahre“, „Monate“ und ein Häkchen, mit dickem Filzstift geschrieben und fotografiert.</p>
  </div>
</section>
'''

out = "/home/user/design-system/markenwelt/index.html"
import os
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, "w").write(html)
print("written", len(html))
