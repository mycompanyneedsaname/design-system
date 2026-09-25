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

# Veröffentlichte Landingpage; das Markensystem verlinkt dorthin.
LANDING = "https://claude.ai/artifact/NRh2JC1PZLoyYuV4VstHeP"

def block(x, y, z, w, d, h, s, stroke, top, left, right, hatch=0, sw=1.6, hatch_face="right"):
    ak = "s" if stroke == OCKER else ""
    P = lambda a, b, c: iso(a, b, c, s)
    T = [P(x, y, z + h), P(x + w, y, z + h), P(x + w, y + d, z + h), P(x, y + d, z + h)]
    L = [P(x, y + d, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x, y + d, z + h)]
    R = [P(x + w, y, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x + w, y, z + h)]
    out = []
    out.append(f'<polygon points="{pts(L)}" fill="{left}" stroke="{stroke}" data-ak="{ak}" stroke-width="{sw}" stroke-linejoin="round"/>')
    out.append(f'<polygon points="{pts(R)}" fill="{right}" stroke="{stroke}" data-ak="{ak}" stroke-width="{sw}" stroke-linejoin="round"/>')
    out.append(f'<polygon points="{pts(T)}" fill="{top}" stroke="{stroke}" data-ak="{ak}" stroke-width="{sw}" stroke-linejoin="round"/>')
    if hatch:
        face = R if hatch_face == "right" else L
        a0, a1, b1, b0 = face[0], face[1], face[2], face[3]
        for i in range(1, hatch):
            t = i / hatch
            p = lerp(a0, a1, t); q = lerp(b0, b1, t)
            out.append(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="{stroke}" data-ak="{ak}" stroke-width="1" stroke-opacity=".45"/>')
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
PETROL = "#0F3B3F"; DEEP = "#071F22"; OCKER = "#C8F04A"; PAPER = "#F7F5F0"; SAND = "#E9E1CF"; INK = "#1A1A18"; MIST = "#EEF0EC"
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
        lab_svg.append(f'<path d="M{ex:.0f} {ey:.0f} Q {(ex+cx)/2:.0f} {(ey+cy)/2 - 10:.0f} {cx:.0f} {cy:.0f}" fill="none" stroke="currentColor" data-ak="s" stroke-width="1.5" stroke-linecap="round" stroke-dasharray="3 3"/>')
        lab_svg.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="3" fill="currentColor" data-ak="f"/>')
        lab_svg.append(f'<text x="{lx:.0f}" y="{ly:.0f}" text-anchor="{anc}" font-family="Kalam, cursive" font-size="19" font-weight="700" fill="currentColor" data-ak="f">{lab}</text>')
    base_lab = f'<text x="{x1-4:.0f}" y="{y1+30:.0f}" text-anchor="end" font-family="Kalam, cursive" font-size="18" font-weight="700" fill="currentColor" data-ak="f">Modularer Effizienz-Baukasten</text>'
    base_arrow = ''
    vb = f"{x0-pad:.0f} {y0-pad:.0f} {x1-x0+2*pad:.0f} {y1-y0+2*pad+10:.0f}"
    return f'<svg viewBox="{vb}" class="iso-hero" role="img" aria-label="Isometrische Bausteine Druckluft, LED, Abwärme und PV auf der Grundplatte des Modularen Effizienz-Baukastens">{body}\n{"".join(lab_svg)}{base_lab}{base_arrow}</svg>'

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
    dak = "f" if dot == OCKER else ""
    ring = f' stroke="{curve}" stroke-width="1.6"' if curve != "#FFFFFF" else ""
    subhtml = f'<div class="zs" style="color:{mono or text}">Büro für Energie- und <br>Ressourceneffizienz</div>' if sub else ""
    return (f'<div class="logo" style="color:{text}"><svg viewBox="0 0 64 64" width="{size}" height="{size}" aria-hidden="true">'
            f'<path d="M6 52 C 30 52 34 12 58 12" fill="none" stroke="{curve}" stroke-width="4.5" stroke-linecap="round"/>'
            f'<circle cx="32" cy="32" r="5.5" fill="{dot}" data-ak="{dak}"{ring}/></svg>'
            f'<div><div class="w1" style="font-size:{w1}px">Wendepunkt</div><div class="w2" style="font-size:{w1}px">Ingenieure</div>{subhtml}</div></div>')

def portrait(v):
    # Platzhalter-Porträt als Duotone-Zeichnung (kein echtes Foto)
    # v=1 Michael: Haare, Brille. v=2 Tobias: Glatze mit Brille (Wunsch 24.09.).
    hair = ('<path d="M38 64 C 36 40, 50 30, 62 31 C 76 31, 86 42, 83 64 C 80 52, 74 46, 62 46 C 50 46, 42 52, 38 64 Z" fill="#0A2C2F"/>' if v == 1 else
            '<path d="M44 48 C 50 42, 72 42, 78 48" fill="none" stroke="#DCE8E9" stroke-width="2" stroke-linecap="round" opacity=".55"/>')
    glasses = '<g fill="none" stroke="#E9E1CF" stroke-width="2"><rect x="44" y="62" width="14" height="10" rx="4"/><rect x="64" y="62" width="14" height="10" rx="4"/><path d="M58 66 h6"/></g>'
    extra = glasses if v == 1 else (glasses + '<path d="M44 84 C 50 98, 72 98, 78 84 C 76 92, 70 96, 61 96 C 52 96, 46 92, 44 84 Z" fill="#0A2C2F" opacity=".55"/>')
    # Fachgebiet-Symbol in der Ecke: Material (Ressourcen) bzw. Strom (Energie)
    sym = ICONS["Material"] if v == 1 else ICONS["Strom"]
    bx = 98 if v == 1 else 22
    badge = (f'<g transform="translate({bx} 20)"><circle r="15" fill="#C8F04A"/>'
             f'<g transform="translate(-11 -11) scale(.55)" fill="none" stroke="{PETROL}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round">{sym}</g></g>')
    return (f'<svg class="pers-img" viewBox="0 0 120 150" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
            f'<rect width="120" height="150" fill="#DCD2BC"/>'
            f'<rect x="{8 if v == 1 else 70}" y="14" width="42" height="56" rx="3" fill="#EFE9DB"/>'
            f'<path d="M0 112 H120" stroke="#C9BDA2" stroke-width="2"/>'
            f'<path d="M4 150 C 8 120, 30 108, 61 108 C 92 108, 114 120, 118 150 Z" fill="{PETROL}"/>'
            f'<path d="M50 108 L 61 124 L 72 108" fill="none" stroke="#C8F04A" stroke-width="3" stroke-linejoin="round"/>'
            f'<rect x="52" y="90" width="18" height="20" fill="#4F7478"/>'
            f'<ellipse cx="61" cy="66" rx="23" ry="28" fill="#6B8E91"/>'
            f'{hair}{extra}{badge}</svg>')

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
 "Kälte": '<path d="M20 5 v 30"/><path d="M7 12.5 l 26 15"/><path d="M7 27.5 l 26 -15"/><path d="M16 8 l 4 4 4 -4"/><path d="M16 32 l 4 -4 4 4"/>',
 "Druckluft": '<path d="M10 14 h 16 a 7 7 0 0 1 0 14 h -16 a 7 7 0 0 1 0 -14 z"/><path d="M14 28 v 5 M22 28 v 5"/><path d="M31 9 q 3 3 0 6"/><path d="M35 6 q 4 6 0 12"/>',
 "Reststoffe": '<path d="M9 13 h 22 l -2 21 h -18 z"/><path d="M6 13 h 28"/><path d="M16 9 h 8"/><path d="M16 19 v 10 M24 19 v 10"/>',
 "Betriebsstoffe": '<path d="M7 20 h 17 l 6 -6 h 4"/><path d="M7 20 v 12 h 17 v -12"/><path d="M13 20 v -5 h 6 v 5"/><path d="M34 21 c 2 3 2.6 5 0 6.5 c -2.6 -1.5 -2 -3.5 0 -6.5 z"/>',
 "Speicher": '<path d="M7 12 h 24 v 18 h -24 z"/><path d="M31 17 h 4 v 8 h -4"/><path d="M12 17 v 8 M18 17 v 8"/>',
}

def pl(m):
    return m.replace('<path ', '<path pathLength="1" ').replace('<circle ', '<circle pathLength="1" ')

def icon(name, color="currentColor", size=44):
    return (f'<svg viewBox="0 0 40 40" width="{size}" height="{size}" fill="none" stroke="{color}" stroke-width="2.2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{pl(ICONS[name])}</svg>')

# Handlungsfelder wie im Hero-Baukasten (zwei Gruppen), dazu das Vorgehen je Stein
FIELDS_E = [("Strom", 2.0, 4), ("Wärme", 2.4, 0), ("Kälte", 1.4, 0), ("Druckluft", 1.8, 5), ("Speicher", 1.2, 4)]
FIELDS_R = [("Material", 1.6, 4), ("Wasser", 1.1, 0), ("Reststoffe", 1.3, 0), ("Betriebsstoffe", 0.9, 4)]
STEPS = ["Messen", "Nachrechnen", "Umsetzen"]
MODULES = FIELDS_E + FIELDS_R + [(n, 1.0, 0) for n in STEPS]

def mod_cards(items):
    return "\n".join(f'<div class="mod"><div class="mod-iso">{module_iso(n, h, hatch)}</div><div class="mod-ic">{icon(n, "currentColor", 30)}</div><b>{n}</b></div>' for n, h, hatch in items)

def modules_html():
    return (f'<div class="modgrp"><span class="grp-l">Energie</span><div class="mods m5">{mod_cards(FIELDS_E)}</div></div>'
            f'<div class="modgrp"><span class="grp-l">Ressourcen</span><div class="mods m4">{mod_cards(FIELDS_R)}</div></div>')

def steps_html():
    arrow = '<span class="st-ar" aria-hidden="true">→</span>'
    return arrow.join(f'<span class="st">{icon(n, "currentColor", 30)}<b>{n}</b></span>' for n in STEPS)

def icons_html():
    return "\n".join(f'<div class="hic">{icon(n, "currentColor", 40)}<span>{n}</span></div>' for n, _, _ in MODULES)

html = f'''<title>Wendepunkt Markenwelt</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&family=Kalam:wght@400;700&display=swap">
<script>document.documentElement.classList.add("js")</script>
<style>
  :root{{
    --petrol:{PETROL}; --deep:{DEEP}; --ocker:{OCKER}; --paper:{PAPER}; --sand:{SAND}; --ink:{INK}; --mist:{MIST};
    --line-l:#D8D3C8; --line-d:rgba(255,255,255,.14); --muted:#4E5A5B;
    --sans:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
    --mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
    --hand:"Kalam","Segoe Print","Bradley Hand",cursive;
    --accent:#C8F04A; --accent-ink:#071F22;
  }}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:16px;line-height:1.55;-webkit-font-smoothing:antialiased}}
  h1,h2,h3,h4{{margin:0;line-height:1.1;text-wrap:balance;font-weight:600;letter-spacing:-.02em}}
  p{{margin:0}}
  a{{color:inherit}}
  a:focus-visible,button:focus-visible{{outline:2px solid var(--petrol);outline-offset:3px}}
  .dark a:focus-visible,.dark button:focus-visible,.deep a:focus-visible,.deep button:focus-visible{{outline-color:var(--accent)}}
  .wrap{{max-width:1200px;margin:0 auto;padding-inline:24px}}
  section{{padding-block:72px}}
  .dark{{background:var(--petrol);color:#fff}}
  .deep{{background:var(--deep);color:#fff}}
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
  .top .logo .zs{{font-size:11px;letter-spacing:.03em;margin-top:5px;opacity:.78;white-space:nowrap}}
  .top .logo .zs br{{display:none}}
  @media (max-width:640px){{.top .logo .zs{{white-space:normal;font-size:10px;min-width:max-content}}.top .logo .zs br{{display:inline}}}}
  .top ul{{display:flex;gap:26px;list-style:none;margin:0;padding:0;font-size:14px}}
  .top .meta{{font-family:var(--mono);font-size:12px;opacity:.7}}
  header.dark{{position:relative;z-index:20}}
  .burger{{width:44px;height:44px;margin-right:-10px;background:transparent;border:0;cursor:pointer;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0}}
  .burger span{{display:block;width:26px;height:2px;background:#fff;border-radius:2px;transition:transform .3s cubic-bezier(.6,0,.2,1),opacity .2s;transform-origin:50% 50%;transform-box:border-box}}
  .burger span+span{{margin-top:6px}}
  .burger[aria-expanded="true"] span:nth-child(1){{transform:translateY(8px) rotate(45deg)}}
  .burger[aria-expanded="true"] span:nth-child(2){{opacity:0;transform:scaleX(.2)}}
  .burger[aria-expanded="true"] span:nth-child(3){{transform:translateY(-8px) rotate(-45deg)}}
  .menu{{position:absolute;left:0;right:0;top:100%;background:var(--deep);color:#fff;border-bottom:1px solid var(--line-d)}}
  .menu[hidden]{{display:none}}
  .menu .wrap{{padding-block:22px 26px;display:flex;justify-content:space-between;align-items:flex-end;gap:24px;flex-wrap:wrap}}
  .menu ul{{list-style:none;margin:0;padding:0}}
  .menu li{{opacity:0;transform:translateY(-8px)}}
  .menu.open li{{animation:menuin .38s cubic-bezier(.2,.8,.2,1) both}}
  .menu.open li:nth-child(2){{animation-delay:.07s}}.menu.open li:nth-child(3){{animation-delay:.14s}}.menu.open li:nth-child(4){{animation-delay:.21s}}
  .menu.open .legal li{{animation-delay:.28s}}
  @keyframes menuin{{to{{opacity:1;transform:none}}}}
  .menu a{{display:flex;align-items:baseline;gap:14px;color:#fff;text-decoration:none;font-size:clamp(20px,2.2vw,26px);font-weight:500;padding:8px 0;letter-spacing:-.01em}}
  .menu a .n{{font-family:var(--mono);font-size:12px;letter-spacing:.1em;color:var(--accent);min-width:2.2em}}
  .menu a:hover,.menu a:focus-visible{{text-decoration:underline;text-underline-offset:6px;text-decoration-thickness:2px;text-decoration-color:var(--accent)}}
  .menu a.mcta{{color:var(--accent)}}
  .menu .legal{{display:flex;gap:20px}}
  .menu .legal a{{font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;font-weight:400;color:rgba(255,255,255,.7);padding:0}}
  @media (prefers-reduced-motion:reduce){{.menu li{{opacity:1;transform:none}}.menu.open li{{animation:none}}.burger span{{transition:none}}}}

  /* hero */
  .hero{{padding-block:48px 72px}}
  .hero .ht{{font-size:clamp(40px,5vw,64px);line-height:1.02;margin-top:22px}}
  .hero .sub{{margin-top:22px;font-size:19px;max-width:46ch}}
  .cta{{display:inline-block;background:var(--ocker);color:var(--deep);font:600 15px/1 var(--sans);padding:15px 20px;border:0;text-decoration:none;white-space:nowrap}}
  .cta.ghost{{background:transparent;color:#fff;border:1px solid var(--line-d)}}
  .actions{{display:flex;gap:14px;align-items:center;margin-top:30px;flex-wrap:wrap}}
  .iso-hero{{width:100%;max-width:560px;height:auto;display:block;margin-inline:auto}}

  /* signature device: Behauptung → nachgerechnet */
    background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 20' preserveAspectRatio='none'%3E%3Cpath d='M2 12 Q 50 4 100 10 T 198 8' fill='none' stroke='%23D9A441' stroke-width='4' stroke-linecap='round'/%3E%3C/svg%3E") no-repeat center / 100% .5em}}
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 20' preserveAspectRatio='none'%3E%3Cpath d='M2 12 Q 50 4 100 10 T 198 8' fill='none' stroke='%230F3B3F' stroke-width='4' stroke-linecap='round'/%3E%3C/svg%3E")}}
  .ring{{position:absolute;left:-10%;top:-28%;width:120%;height:156%;pointer-events:none}}
  .ringed{{position:relative;display:inline-block;padding:0 .12em}}

  /* prinzip */
  .prinzip{{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--line-l);border:1px solid var(--line-l)}}
  .prinzip > div{{background:var(--paper);padding:26px 24px 28px;display:flex;flex-direction:column;justify-content:flex-start;gap:22px}}
  .prinzip .big{{font-size:26px;font-weight:600;letter-spacing:-.02em;line-height:1.15}}
  .prinzip .k{{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}}
  .prinzip .why{{font-size:14px;color:var(--muted)}}

  /* baukasten */
  .modgroups{{display:grid;grid-template-columns:5fr 4fr;gap:28px}}
  .grp-l{{display:block;font:500 11px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:rgba(255,255,255,.6);margin-bottom:10px}}
  .mods{{display:grid;gap:12px}}
  .mods.m5{{grid-template-columns:repeat(5,1fr)}}
  .mods.m4{{grid-template-columns:repeat(4,1fr)}}
  .steps{{display:flex;flex-wrap:wrap;align-items:center;gap:14px 18px;margin-top:28px;padding-top:20px;border-top:1px solid var(--line-d)}}
  .steps .k{{font:500 11px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:rgba(255,255,255,.6);margin-right:8px}}
  .st{{display:inline-flex;align-items:center;gap:10px;color:var(--accent)}}
  .st b{{color:#fff;font-weight:500;font-size:15px}}
  .st-ar{{color:rgba(255,255,255,.5);font-family:var(--mono)}}
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
  .rules{{display:grid;grid-template-columns:repeat(2,1fr);gap:24px 32px}}
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
    .modgroups{{grid-template-columns:1fr}}
    .mods.m5,.mods.m4{{grid-template-columns:repeat(3,1fr)}}
    .hicons{{grid-template-columns:repeat(4,1fr)}}
    .sw{{grid-template-columns:repeat(3,1fr)}}
    section{{padding-block:56px}}
  }}
  @media (max-width:520px){{
    .mods.m5,.mods.m4,.hicons{{grid-template-columns:repeat(2,1fr)}}
    .sw{{grid-template-columns:repeat(2,1fr)}}
    .type .row{{grid-template-columns:1fr}}
  }}

  [data-ak="s"]{{stroke:var(--accent)}}
  [data-ak="f"]{{fill:var(--accent)}}
  .dark .tag,.deep .tag{{color:var(--accent)}}
  .cta{{background:var(--accent);color:var(--accent-ink)}}


  /* configurator */
  .cfg{{display:grid;gap:14px 20px;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);align-items:center}}
  .cfg .chips{{grid-column:1/-1}}
  @media (max-width:640px){{.cfg{{grid-template-columns:1fr}}}}
  .cfg svg{{width:100%;height:auto;display:block}}
  .blk{{transform-box:fill-box;transform-origin:center}}
  .blk.new{{animation:rise .45s cubic-bezier(.2,.8,.2,1) both}}
  .js #plate:not(.built) .blk.stone{{opacity:0}}
  .js #plate.on:not(.built) .blk.stone{{animation:rise2 .5s cubic-bezier(.2,.8,.2,1) both}}
  @keyframes rise2{{from{{transform:translateY(-22px);opacity:0}}to{{transform:none;opacity:1}}}}
  #plate .blk.stone{{transition:opacity .25s}}
  .js #plate.built .blk.stone.new{{animation:rise2 .45s cubic-bezier(.2,.8,.2,1) both}}
  .chips .chip{{cursor:pointer}}
  .chips .chip svg{{width:15px;height:15px;margin-right:7px;vertical-align:-3px}}
  .chips .chip .ck{{opacity:0}}
  .chips .chip[aria-pressed="true"]{{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}}
  .chips .chip[aria-pressed="true"] .ck{{opacity:1}}
  .bk-calc{{font-family:var(--mono);font-size:12.5px;line-height:1.35;border-top:1px solid rgba(255,255,255,.35);padding-top:10px}}
  .bc-head{{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:rgba(255,255,255,.6);margin-bottom:8px}}
  .bc-rows{{list-style:none;margin:0;padding:0}}
  .bc-rows li{{display:grid;grid-template-columns:auto 1fr auto;gap:0 10px;padding:4px 0;border-bottom:1px dashed rgba(255,255,255,.22);align-items:baseline;transition:opacity .2s}}
  .bc-rows li.ph{{visibility:hidden}}
  .bc-rows .bc-f{{color:#fff;font-weight:500}}
  .bc-rows .bc-m{{color:rgba(255,255,255,.7);font-family:var(--sans);font-size:13px}}
  .bc-rows b{{font-weight:500;color:#fff;text-align:right;font-variant-numeric:tabular-nums}}
    .bc-sum{{display:flex;justify-content:space-between;align-items:baseline;padding-top:10px;color:#fff;font-size:12px;letter-spacing:.06em;text-transform:uppercase}}
  .bc-sum b{{font-family:var(--sans);font-weight:600;font-size:34px;line-height:1;color:var(--accent);letter-spacing:-.02em;font-variant-numeric:tabular-nums}}
  .bc-sum b.tick{{animation:pop .35s cubic-bezier(.2,.9,.3,1.3)}}
  @keyframes pop{{from{{transform:translateY(4px);opacity:.4}}}}
  .bc-foot sup,.bc-sum sup{{font-size:.7em;vertical-align:top;margin-right:2px}}
  .bc-foot{{margin:8px 0 0;font-family:var(--sans);font-size:11px;line-height:1.4;color:rgba(255,255,255,.6)}}
  .bk-calc{{min-width:0}}
  @keyframes rise{{from{{transform:translateY(-22px);opacity:0}}}}
  .slot{{stroke-dasharray:4 4;opacity:.45}}
  .chips{{display:flex;flex-wrap:wrap;gap:8px}}
  .chips button{{font:500 12px/1 var(--mono);letter-spacing:.06em;text-transform:uppercase;padding:9px 12px;border:1px solid var(--line-d);border-radius:10px;background:transparent;color:#fff;cursor:pointer;display:inline-flex;gap:8px;align-items:center}}
  .chips button svg{{width:16px;height:16px}}
  .chips button[aria-pressed="true"]{{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}}
  .chips .chip{{font:500 12px/1 var(--mono);letter-spacing:.06em;text-transform:uppercase;padding:8px 11px;border:1px solid var(--line-d);border-radius:10px;color:rgba(255,255,255,.85);background:transparent;cursor:default;transition:background .15s,color .15s}}
  .tally{{display:flex;gap:26px;flex-wrap:wrap;font-family:var(--mono);font-size:13px;border-top:1px solid var(--line-d);padding-top:12px}}
  .tally b{{display:block;font-size:24px;font-weight:500;color:var(--accent);line-height:1.1}}
  .tally span{{opacity:.75}}
  .hero .ht{{font-size:clamp(44px,5.4vw,72px);line-height:.98}}
  .hero .grid2{{grid-template-columns:.9fr 1.1fr;gap:56px;align-items:start}}
  .hic svg path,.hic svg circle{{stroke-dasharray:1;stroke-dashoffset:0}}
  .hic:hover svg path,.hic:hover svg circle{{animation:draw .8s ease-out both}}
  @keyframes draw{{from{{stroke-dashoffset:1}}to{{stroke-dashoffset:0}}}}
  .poster{{transition:transform .25s ease}}
  .poster:hover{{transform:translateY(-6px)}}
  .prinzip .big{{font-size:30px}}

  /* Korrektur nach DIN 16511: Behauptung gestrichen, Wert am Rand */
  .korr{{display:block}}
  .korr .alt{{color:rgba(255,255,255,.5);-webkit-box-decoration-break:clone;box-decoration-break:clone;
    background:linear-gradient(var(--accent),var(--accent)) no-repeat 0 58% / 0% 2px;animation:strike .8s .3s cubic-bezier(.6,0,.2,1) forwards}}
  .korr .km{{display:inline-grid;place-items:center;width:1.5em;height:1.5em;border:1.5px solid var(--accent);border-radius:50%;
    font:500 11px/1 var(--mono);color:var(--accent);vertical-align:.9em;margin-left:.4em;letter-spacing:0}}
  .korr .neu{{display:flex;gap:10px;align-items:baseline;margin-top:.55em;padding-top:.55em;border-top:1px solid var(--accent);
    font-family:var(--mono);font-weight:500;font-size:max(13px,.42em);line-height:1.4;letter-spacing:0;color:var(--accent);opacity:0;animation:fade .5s .95s ease-out forwards}}
  .korr .neu .km{{vertical-align:0;margin:0;flex:none;transform:translateY(-1px)}}
  .light .korr .alt{{color:rgba(26,26,24,.42);background-image:linear-gradient(var(--petrol),var(--petrol))}}
  .light .korr .km{{border-color:var(--petrol);color:var(--petrol)}}
  .light .korr .neu{{color:var(--petrol);border-color:var(--petrol)}}
  @keyframes strike{{to{{background-size:100% 2px}}}}
  @keyframes fade{{to{{opacity:1}}}}
  @media (prefers-reduced-motion:reduce){{.korr .alt{{animation:none;background-size:100% 2px}}.korr .neu{{animation:none;opacity:1}}.blk.new{{animation:none}}.js #plate .blk.stone{{opacity:1;animation:none}}}}

  /* Baukasten-Erklärung */
  .expl{{border:1px solid var(--line-d);padding:16px 18px;display:grid;gap:8px}}
  .expl .h{{display:flex;justify-content:space-between;gap:12px;align-items:baseline}}
  .expl .h b{{font-size:17px;font-weight:600}}
  .expl .h span{{font-family:var(--mono);font-size:12px;color:var(--accent)}}
  .expl p{{font-size:14.5px;color:rgba(255,255,255,.85)}}
  .expl ul{{margin:0;padding:0;list-style:none;display:flex;flex-wrap:wrap;gap:6px 18px;font-family:var(--mono);font-size:12px;color:rgba(255,255,255,.75)}}
  .expl li::before{{content:"+ ";color:var(--accent)}}
  .hero .ht .l2{{display:block;font-weight:400;font-size:.46em;line-height:1.2;letter-spacing:-.01em;margin-top:.45em;color:rgba(255,255,255,.72);max-width:22ch}}

  .glyph .flow{{stroke-dasharray:.1 .07;animation:flow 1.6s linear infinite}}
  @keyframes flow{{to{{stroke-dashoffset:-.34}}}}
  @media (prefers-reduced-motion:reduce){{.glyph .flow{{animation:none}}}}
  .hero .ht .pre{{display:block;font-family:var(--mono);font-weight:500;font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);margin-bottom:.9em}}

  .wp-band{{padding-block:88px}}
  .wp-grid{{display:grid;grid-template-columns:.9fr 1.1fr;gap:48px;align-items:center}}
  .wp-h{{font-size:clamp(30px,3.6vw,48px);color:{PETROL};margin-top:0;max-width:18ch}}
  .wp-p{{font-size:clamp(20px,2vw,26px);line-height:1.35;color:{PETROL};margin-top:22px;max-width:30ch}}
  .wp-art{{width:100%;height:auto;display:block}}
  @media (min-width:981px){{.wp-right{{padding-top:24px}}}}
  .bk-cta{{margin-top:auto;padding-top:8px;padding-bottom:0;text-align:left}}
  .bk-l{{display:flex;flex-direction:column}}
  .wp-proof{{display:flex;gap:12px;align-items:baseline;margin-top:24px;max-width:none;color:{PETROL};font-size:16px;line-height:1.4;opacity:.9}}
  .wp-proof .num{{font-family:var(--mono);font-weight:500;font-size:21px;line-height:1;letter-spacing:-.02em;flex:none}}
  .wp-mnotes{{display:none;list-style:none;margin:14px 0 0;padding:0;font-family:var(--hand);font-weight:700;font-size:18px;line-height:1.3;color:{PETROL}}}
  .wp-mnotes li{{display:grid;grid-template-columns:64px 1fr;gap:10px;padding-block:5px}}
  .wp-mnotes .k{{font-family:var(--mono);font-weight:500;font-size:11px;letter-spacing:.1em;text-transform:uppercase;opacity:.7;padding-top:5px}}
  .tl-m{{display:none;text-align:center;margin:36px 0 0;font-family:var(--hand);font-weight:700;font-size:22px;color:{PETROL}}}
  .tl-m .lab{{display:block;font-family:var(--mono);font-weight:500;font-size:12px;letter-spacing:.1em;text-transform:uppercase;margin-bottom:4px;opacity:.75}}
  .bk-how{{text-align:left;max-width:36ch;margin:26px 0 26px;font-size:18px;line-height:1.45;color:rgba(255,255,255,.82)}}
  .bk-how b{{color:#fff;font-weight:600}}
  .bk-contact{{margin:18px 0 0;font-size:15px;color:rgba(255,255,255,.7)}}
  .bk-contact a{{color:#fff;text-decoration:underline;text-underline-offset:3px}}
  .site-foot{{padding-block:22px;font-family:var(--mono);font-size:12px;letter-spacing:.04em;color:rgba(255,255,255,.7)}}
  .site-foot .wrap{{display:flex;justify-content:flex-end;gap:12px 24px;flex-wrap:wrap}}
  .site-foot nav{{display:flex;gap:20px}}
  .site-foot .fsig{{display:inline-flex;align-items:center;gap:10px}}
  .site-foot a{{color:#fff;text-decoration:none}}
  .site-foot a:hover{{text-decoration:underline}}
  .bk-stack .ht{{font-size:clamp(34px,3.6vw,48px);line-height:1.04}}
  @media (max-width:640px){{.wp-art .wp-note{{display:none}}.wp-mnotes{{display:block}}}}
  @media (max-width:980px){{.tl-m{{display:block}}.team-sec{{padding-bottom:48px}}}}
  .bk-stack{{display:grid;grid-template-columns:.8fr 1.2fr;gap:48px;align-items:stretch;text-align:left;padding-top:8px;padding-bottom:24px}}
  @media (max-width:980px){{.bk-stack{{grid-template-columns:1fr;gap:28px}}.bk-l{{display:contents}}.bk-stack .ht{{order:1}}.bk-stack .bk-how{{order:2;margin:0}}.bk-stack .cfg{{order:3}}.bk-stack .bk-cta{{order:4}}}}
  .bk-stack .ht{{margin-top:0}}
  .bk-stack .ht .l2{{max-width:none}}
  .bk-stack .ht{{max-width:22ch}}
  .bk-stack .cfg{{max-width:none;margin:0}}
  .bk-stack .chips{{justify-content:flex-start}}
  .bk-stack .hnote{{position:static;transform:rotate(-1.5deg);transform-origin:center;max-width:34ch;text-wrap:balance;text-align:center;font-size:21px;margin:0 auto 6px}}
  .bk-stack .hnote svg{{display:none}}
  
  .bk-stack #plate{{max-width:none;margin:0}}
  .bk-cta .wp-cta{{border-color:#C8F04A}}
  .cta-wrap{{position:relative;display:inline-block}}
  .cta-arrow{{display:none;position:absolute;left:58%;top:-96px;width:120px;height:90px;overflow:visible;pointer-events:none}}
  @media (min-width:981px){{.cta-arrow{{display:block}}}}
  .js .cta-arrow .ca-line{{stroke-dasharray:1;stroke-dashoffset:1}}
  .js .cta-arrow .ca-head{{opacity:0}}
  .js .cta-arrow.on .ca-line{{stroke-dashoffset:0}}
  .js .cta-arrow.on .ca-head{{opacity:1}}
  @media (prefers-reduced-motion:no-preference){{.cta-arrow .ca-line{{transition:stroke-dashoffset .8s cubic-bezier(.6,0,.2,1) .2s}}.cta-arrow .ca-head{{transition:opacity .3s ease-out .9s}}}}
  .wp-act{{display:flex;justify-content:center;padding-left:14%;margin-top:6px}}
  @media (max-width:980px){{.wp-act{{padding-left:0}}}}
  .wp-curve{{stroke-dasharray:1;stroke-dashoffset:0}}
  @media (prefers-reduced-motion:no-preference){{
    .wp-curve{{animation:wpdraw 1.6s .2s cubic-bezier(.6,0,.2,1) both}}
    .wp-dot{{transform-box:fill-box;transform-origin:center;animation:wppop .5s 1.1s cubic-bezier(.2,.9,.3,1.4) both}}
    .wp-note{{animation:fade .5s 1.6s ease-out both}}
  }}
  @keyframes wpdraw{{from{{stroke-dashoffset:1}}}}
  @keyframes wppop{{from{{transform:scale(0)}}}}
  @media (max-width:980px){{.wp-grid{{grid-template-columns:1fr}}.wp-band{{padding-block:56px}}}}
  .wp-band{{--accent:#C8F04A;--accent-ink:{PETROL}}}
  .wp-cta{{display:inline-flex;align-items:center;gap:14px;background:var(--accent);color:{PETROL};border:2px solid {PETROL};
    font:600 16px/1 var(--sans);padding:16px 24px;border-radius:12px;text-decoration:none;transition:transform .2s ease,box-shadow .2s ease}}
  .wp-cta:hover,.wp-cta:focus-visible{{transform:translate(-3px,-3px);box-shadow:3px 3px 0 {PETROL}}}
  .chips .grp{{flex-basis:100%;font:500 11px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:rgba(255,255,255,.6);margin-top:6px}}
  .chips .grp:first-child{{margin-top:0}}
  .cfg{{position:relative}}
  .hnote{{position:absolute;left:0;top:-6px;max-width:300px;color:var(--accent);font-family:var(--hand);font-weight:700;font-size:20px;line-height:1.18;transform:rotate(-3deg);transform-origin:left top;pointer-events:none;z-index:1}}
  .hnote svg{{display:block;width:78px;height:auto;margin:6px 0 0 36px}}
  .hnote.pop{{animation:fade .45s ease-out both}}
  .sig-hand{{margin-top:28px;color:var(--accent);display:grid;gap:2px;max-width:260px}}
  .hand-name{{font-family:var(--hand);font-weight:700;font-size:30px;line-height:1;transform:rotate(-2deg);transform-origin:left}}
  .sig-hand svg{{width:210px;height:12px;display:block}}
  .sig-cap{{font-family:var(--mono);font-size:11.5px;letter-spacing:.04em;color:rgba(255,255,255,.7);margin-top:6px}}
  @media (max-width:980px){{.hnote{{position:static;transform:rotate(-2deg);margin-bottom:6px}}.hnote svg{{display:none}}}}
  /* Startseite: Wendepunkt als Einstieg, Team, Referenzen */
  .wp-pre{{display:inline-block;position:relative;background:{PETROL};color:#fff;font:500 clamp(16px,1.5vw,19px)/1.3 var(--sans);padding:12px 20px 12px 44px;border-radius:12px;margin-bottom:26px}}
  .wp-pre::before{{content:"";position:absolute;left:20px;top:50%;width:12px;height:12px;margin-top:-6px;border-radius:50%;background:#C8F04A}}
  .wp-band .wp-h{{font-size:clamp(34px,4.2vw,56px);line-height:1.04;max-width:15ch}}
  #start .wp-grid{{grid-template-columns:1fr 1fr}}
  @media (max-width:980px){{#start .wp-grid{{grid-template-columns:1fr}}}}
  .top ul a{{color:inherit;text-decoration:none}}
  .top ul a:hover{{text-decoration:underline;text-underline-offset:4px}}
  .team{{display:grid;grid-template-columns:1fr 1fr;gap:40px}}
  .pers-l{{display:grid;gap:10px}}
  .pers-n{{margin:0;display:flex;gap:6px;align-items:flex-start;color:{PETROL};font-family:var(--hand);font-weight:700;font-size:18px;line-height:1.15;transform:rotate(-3deg);transform-origin:left top}}
  .pers-n svg{{flex:none;width:30px;height:auto;margin-top:-4px}}
  .team-link{{display:block;width:100%;height:auto;margin-top:4px;overflow:visible}}
  .js .team-link .tl-curve{{stroke-dasharray:1;stroke-dashoffset:1}}
  .js .team-link .tl-dot{{transform:scale(0);transform-box:fill-box;transform-origin:center}}
  .js .team-link .tl-fade{{opacity:0}}
  .js .team-link.on .tl-curve{{stroke-dashoffset:0}}
  .js .team-link.on .tl-dot{{transform:scale(1)}}
  .js .team-link.on .tl-fade{{opacity:1}}
  @media (prefers-reduced-motion:no-preference){{
    .team-link .tl-curve{{transition:stroke-dashoffset 1.4s cubic-bezier(.6,0,.2,1)}}
    .team-link .tl-dot{{transition:transform .5s cubic-bezier(.2,.9,.3,1.4) .9s}}
    .team-link .tl-fade{{transition:opacity .5s ease-out 1.3s}}
  }}
  .team-sec{{padding-bottom:0}}
  #baukasten{{padding-top:0}}
  .bk-link{{display:block;width:100%;height:auto;overflow:visible;margin-bottom:-8px}}
  .js .bk-link .tl-curve{{stroke-dasharray:1;stroke-dashoffset:1}}
  .js .bk-link .tl-dot{{transform:scale(.6);opacity:0;transform-box:fill-box;transform-origin:center}}
  .js .bk-link .tl-fade{{opacity:0}}
  .js .bk-link.on .tl-curve{{stroke-dashoffset:0}}
  .js .bk-link.on .tl-dot{{transform:scale(1);opacity:1}}
  .js .bk-link.on .tl-fade{{opacity:1}}
  @media (prefers-reduced-motion:no-preference){{
    .bk-link .tl-curve{{transition:stroke-dashoffset .9s linear}}
    .bk-link .tl-dot{{transition:transform .6s cubic-bezier(.2,.9,.3,1.2) .8s,opacity .4s ease-out .8s}}
    .bk-link .tl-fade{{transition:opacity .5s ease-out .9s}}
  }}
  @media (max-width:980px){{.team-link,.bk-link{{display:none}}.team-sec{{padding-bottom:56px}}#baukasten{{padding-top:56px}}}}
  .pers{{display:grid;grid-template-columns:150px 1fr;gap:24px;align-items:start}}
  @media (min-width:981px){{.team .pers:first-child{{grid-template-columns:1fr 150px}}.team .pers:first-child .pers-l{{order:2}}.team .pers:first-child>div:not(.pers-l){{text-align:right}}.team .pers:first-child p{{margin-left:auto}}}}
  .pers-ph{{aspect-ratio:4/5;background:var(--sand);border-radius:12px;position:relative;overflow:hidden}}
  .pers-img{{width:100%;height:100%;display:block}}
  .pers-ph .ini{{font:500 34px/1 var(--mono);color:{PETROL};opacity:.35}}
  .pers-ph .ph-note{{position:absolute;right:8px;top:8px;font-family:var(--mono);font-size:9.5px;letter-spacing:.06em;text-transform:uppercase;background:rgba(247,245,240,.85);color:{PETROL};padding:3px 6px;border-radius:6px}}
  .pers-role{{display:inline-block;font-family:var(--sans);font-weight:600;font-size:19px;letter-spacing:-.01em;color:{PETROL};border-bottom:3px solid #C8F04A;padding-bottom:1px;line-height:1.2}}
  .pers h3{{font-size:24px;margin-top:4px;color:{PETROL}}}
  .pers p{{margin-top:10px;font-size:15.5px;max-width:44ch}}
  .pers .pers-q{{font-family:var(--hand);font-weight:700;font-size:22px;line-height:1.2;color:{PETROL};transform:rotate(-2deg);transform-origin:left;margin-top:14px}}
  /* Lime-Textmarker: wird gezogen, sobald die Stelle sichtbar ist */
  .hl,.pers .pers-q span{{color:inherit;background:linear-gradient(#C8F04A,#C8F04A) no-repeat 0 80% / 100% 54%;-webkit-box-decoration-break:clone;box-decoration-break:clone;padding:0 .15em}}
  .js .hl:not(.on),.js .pers .pers-q span:not(.on){{background-size:0% 54%}}
  @media (prefers-reduced-motion:no-preference){{.hl,.pers .pers-q span{{transition:background-size .9s cubic-bezier(.6,0,.2,1) .25s}}}}
  .ref-band{{padding-block:56px}}
  .ref-head{{display:flex;gap:18px;align-items:baseline;flex-wrap:wrap;margin-bottom:20px}}
  .ref-head h2{{font-size:clamp(22px,2.4vw,30px);color:{PETROL}}}
  .refs{{list-style:none;margin:0;padding:0;border-top:1px solid var(--line-l)}}
  .refs li{{display:grid;grid-template-columns:1.3fr .6fr 1fr 1fr;gap:16px;align-items:baseline;padding:14px 0;border-bottom:1px solid var(--line-l);font-size:15px}}
  .refs .r-who{{font-weight:600;color:{PETROL}}}
  .refs .r-f{{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}}
  .refs .r-num{{font-family:var(--mono);font-weight:500;color:{PETROL};text-align:right}}
  .ref-note{{margin-top:12px;font-size:13px;color:var(--muted)}}
  .comp{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}}
  .comp-c{{background:#fff;border:1px solid var(--line-l);border-radius:12px;padding:18px;display:flex;flex-direction:column}}
  .comp-s{{min-height:176px;display:flex;align-items:center;justify-content:center;margin-bottom:16px}}
  .comp-c .wp-cta{{white-space:normal;text-align:left;font-size:15px}}
  .comp-c .bc-sum b{{white-space:nowrap}}
  .comp-c h4{{margin:0 0 6px;font-size:16px;color:{PETROL}}}
  .comp-c p{{margin:0;font-size:14px;line-height:1.5;color:var(--muted)}}
  @media (max-width:980px){{ .comp{{grid-template-columns:1fr 1fr}} }}
  @media (max-width:560px){{ .comp{{grid-template-columns:1fr}} }}
  .sys-div{{background:var(--deep);color:rgba(255,255,255,.75);font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;padding-block:18px}}
  .sys-div .wrap{{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}}
  .sys-div span:first-child{{color:#fff}}
  @media (max-width:980px){{.team{{grid-template-columns:1fr}}.refs li{{grid-template-columns:1fr 1fr;gap:4px 16px}}.refs .r-num{{text-align:left}}}}
  @media (max-width:520px){{.pers{{grid-template-columns:96px 1fr;gap:16px}}}}
</style>

<!-- ============================ KOPF ============================ -->
<header class="dark">
  <div class="wrap">
    <div class="top">
      {logo("#FFFFFF", OCKER, "#FFFFFF", size=34, w1=15, sub=False)}
      <button class="burger" id="burger" type="button" aria-expanded="false" aria-controls="menu" aria-label="Menü öffnen"><span></span><span></span><span></span></button>
    </div>
  </div>
  <nav class="menu" id="menu" aria-label="Seitenmenü" hidden>
    <div class="wrap">
      <ul>
        <li><a href="#start"><span class="n">01</span>Der Wendepunkt</a></li>
        <li><a href="#team"><span class="n">02</span>Wir nehmen es persönlich</a></li>
        <li><a href="#baukasten"><span class="n">03</span>Der Modulare Effizienz-Baukasten</a></li>
        <li><a href="#kontakt" class="mcta"><span class="n">04</span>Kostenfreies Erstgespräch</a></li>
      </ul>
      <ul class="legal">
        <li><a href="#impressum">Impressum</a></li>
        <li><a href="#datenschutz">Datenschutz</a></li>
      </ul>
    </div>
  </nav>
</header>

<!-- ============================ 1 · WENDEPUNKT (Start) ============================ -->
<section class="sand wp-band" id="start" aria-label="Der Wendepunkt">
  <div class="wrap wp-grid">
    <div>
      <h1 class="wp-h">Der Wendepunkt ist der Moment, ab dem es anders läuft.</h1>
      <p class="wp-p">Wir sind ein Büro für <mark class="hl">Energie- und Ressourceneffizienz</mark> und suchen ihn gemeinsam mit Ihnen. In rund <strong>150 Betrieben</strong> des verarbeitenden Gewerbes haben wir das schon getan.</p>
    </div>
    <div class="wp-right">
    <svg class="wp-art" viewBox="0 0 600 320" role="img" aria-label="Eine Kurve mit markiertem Wendepunkt. Davor: steigende Betriebskosten, CO₂-Ausstoß &amp; Rohstoff-Knappheit. Danach: sinkende Betriebskosten, Flexibilität &amp; Resilienz. Am Wendepunkt: hier.">
      <path class="wp-curve" pathLength="1" d="M20 262 C 150 270, 190 200, 260 150 C 330 100, 360 36, 500 30" fill="none" stroke="{PETROL}" stroke-width="12" stroke-linecap="round"/>
      <circle class="wp-dot" cx="260" cy="150" r="21" fill="currentColor" data-ak="f" stroke="{PETROL}" stroke-width="3"/>
      <rect class="wp-note" x="295" y="289" width="80" height="17" fill="#C8F04A"/>
      <g class="wp-note" font-family="Kalam, cursive" font-weight="700" font-size="24" fill="{PETROL}">
        <text x="24" y="44">steigende Betriebskosten,</text>
        <text x="24" y="78">CO₂-Ausstoß &amp;</text>
        <text x="24" y="112">Rohstoff-Knappheit</text>
        <text x="592" y="156" text-anchor="end">sinkende Betriebskosten,</text>
        <text x="592" y="190" text-anchor="end">Flexibilität &amp;</text>
        <text x="592" y="224" text-anchor="end">Resilienz</text>
        <text x="300" y="306" font-size="34">hier.</text>
      </g>
      <g class="wp-note" fill="none" stroke="{PETROL}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
        <path d="M70 128 C 60 160, 72 196, 104 226"/><path d="M88 220 L 106 229 L 104 209"/>
        <path d="M560 128 C 568 96, 556 66, 524 46"/><path d="M526 66 L 522 45 L 543 45"/>
        <path d="M272 176 C 276 214, 286 246, 298 272"/>
      </g>
    </svg>
    <ul class="wp-mnotes" aria-hidden="true">
      <li><span class="k">davor</span>steigende Betriebskosten, CO₂-Ausstoß &amp; Rohstoff-Knappheit</li>
      <li><span class="k">hier</span><span><mark class="hl">der Wendepunkt.</mark></span></li>
      <li><span class="k">danach</span>sinkende Betriebskosten, Flexibilität &amp; Resilienz</li>
    </ul>
    </div>
  </div>
</section>

<!-- ============================ 2 · TEAM ============================ -->
<section class="light team-sec" id="team">
  <div class="wrap">
    <div class="sec-head">
      <h2>Wir nehmen es <mark class="hl">persönlich</mark>.</h2>
    </div>
    <div class="team">
      <article class="pers">
        <div class="pers-l"><div class="pers-ph">{portrait(1)}</div></div>
        <div>
          <div class="pers-role">Ressourceneffizienz</div>
          <h3>Michael Schenk</h3>
          <p>Michael hat die meisten dieser Betriebe selbst besucht und fast überall schon in der ersten Stunde Ansatzpunkte gefunden. Seine Stärke: Technik und Wirtschaftlichkeit so zu <strong>erklären</strong>, dass jeder im Betrieb versteht, <strong>warum sich eine Maßnahme lohnt</strong>.</p>
        </div>
      </article>
      <article class="pers">
        <div class="pers-l"><div class="pers-ph">{portrait(2)}</div></div>
        <div>
          <div class="pers-role">Energieeffizienz</div>
          <h3>Tobias Wintsche</h3>
          <p>Für Tobias ist das Ganze nur so gut wie seine Einzelteile. In einer Welt voller Übertechnisierung <strong>findet er die elegante, einfache Lösung</strong>, die auch dann noch jemand versteht, wenn unsere Arbeit vollendet ist.</p>
        </div>
      </article>
    </div>
    <svg class="team-link" viewBox="0 0 1000 200" role="img" aria-label="Zwei Ströme, Ressourcen und Energie, fließen zusammen in Ihren Betrieb.">
      <path class="tl-curve" pathLength="1" d="M241 8 C 241 110, 500 80, 500 200" fill="none" stroke="{PETROL}" stroke-width="3.5" stroke-linecap="round"/>
      <path class="tl-curve" pathLength="1" d="M759 8 C 759 110, 500 80, 500 200" fill="none" stroke="{PETROL}" stroke-width="3.5" stroke-linecap="round"/>
      <g class="tl-fade">
        <rect x="511" y="174" width="262" height="14" fill="#C8F04A"/>
        <text x="516" y="186" font-family="Kalam, cursive" font-weight="700" font-size="22" fill="{PETROL}">beides zusammen gedacht.</text>
      </g>
    </svg>
    <p class="tl-m"><mark class="hl">beides zusammen gedacht.</mark></p>
  </div>
</section>

<!-- ============================ 3 · BAUKASTEN ============================ -->
<section class="dark" id="baukasten">
  <div class="wrap">
    <svg class="bk-link" viewBox="0 0 1000 64" aria-hidden="true">
      <path class="tl-curve" pathLength="1" d="M500 0 L 500 26 C 500 46, 480 50, 40 50" fill="none" stroke="#C8F04A" stroke-width="3.5" stroke-linecap="round"/>
      <circle class="tl-dot" cx="20" cy="50" r="7" fill="#C8F04A"/>
    </svg>
    <div class="hero bk-stack">
      <div class="bk-l">
        <h2 class="ht"><span class="pre">Unser Versprechen:</span>Der Modulare Effizienz-Baukasten.<span class="l2">Weniger Verbrauch, mehr Spielraum.</span></h2>
        <p class="bk-how">Für jede Maßnahme: <b>messen</b>, <b>nachrechnen</b>, <b>umsetzen</b>. Wir entscheiden gemeinsam, welche wir angehen.</p>
        <div class="bk-cta" id="kontakt">
          <span class="cta-wrap"><a class="wp-cta" href="mailto:kontakt@wendepunkt-ingenieure.de?subject=Kostenfreies%20Erstgespr%C3%A4ch">Kostenfreies Erstgespräch vereinbaren</a>
          <svg class="cta-arrow" viewBox="0 0 120 90" aria-hidden="true"><path class="ca-line" pathLength="1" d="M112 6 C 108 44, 80 66, 30 78" fill="none" stroke="#C8F04A" stroke-width="3" stroke-linecap="round"/><path class="ca-head" d="M46 64 L 28 78 L 50 86" fill="none" stroke="#C8F04A" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
        </div>
      </div>
      <div class="cfg" id="cfg">
        <div id="plate" style="color:var(--accent)"></div>
        <div class="bk-calc" id="bk-calc" aria-live="polite">
          <div class="bc-head">Beispielmaßnahmen</div>
          <ul class="bc-rows" id="bc-rows"></ul>
          <div class="bc-sum"><span>Zusammen<sup>*</sup></span><b id="bc-total">−0 %</b></div>
          <div class="bc-foot"><sup>*</sup>Richtwerte aus unseren Projekten, bezogen auf Energie- und Materialkosten pro Jahr.</div>
        </div>
        <div class="chips" id="chips" aria-label="Maßnahmen wählen"></div>
      </div>
    </div>
  </div>
</section>

<footer class="deep site-foot">
  <div class="wrap">
    <span class="fsig"><svg viewBox="0 0 64 64" width="22" height="22" aria-hidden="true"><path d="M6 52 C 30 52 34 12 58 12" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round"/><circle cx="32" cy="32" r="5.5" fill="#C8F04A"/></svg>Wendepunkt Ingenieure GbR · Eisenach / Leipzig</span>
  </div>
</footer>

<!-- ============================ MARKENSYSTEM ============================ -->
<div class="sys-div"><div class="wrap"><span>Ab hier: Markensystem</span><span>Signaturelement · Bausteine · Icons · Plakate · Anwendung · Farben und Schriften · Komponenten</span></div></div>

<!-- ============================ PRINZIP ============================ -->
<section class="light" id="kompass">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Das Signaturelement</span>
      <h2>Behauptung gestrichen. Wert am Rand.</h2>
      <p class="muted">Das Signaturelement ist ein Korrekturzeichen, wie es Lektoren und Prüfingenieure nach DIN 16511 setzen: Die Behauptung wird mit einer feinen Linie gestrichen, ein nummeriertes Zeichen verweist auf den Rand, dort steht der nachgerechnete Wert mit Einheit. Präzise statt laut. Es funktioniert in Anzeige, LinkedIn-Post und Bericht. Für das, was zählt, gibt es daneben den Lime-Textmarker (siehe Startseite).</p>
    </div>
    <div class="prinzip">
      <div>
        <span class="k">Beispiel 01 · Amortisation</span>
        <div class="big"><span class="korr"><span class="alt">Rechnet sich</span> <span style="white-space:nowrap"><span class="alt">sofort.</span><span class="km">1</span></span><span class="neu"><span class="km">1</span>Druckluft 5 Monate · Beleuchtung 3,3 Jahre</span></span></div>
        <p class="why">Keine pauschale ROI-Zahl, wie im Briefing verlangt. Der Rand liefert die Zahl mit Kontext.</p>
      </div>
      <div>
        <span class="k">Beispiel 02 · Floskel</span>
        <div class="big"><span class="korr"><span class="alt">Ganzheitlich</span> <span style="white-space:nowrap"><span class="alt">nachhaltig.</span><span class="km">1</span></span><span class="neu"><span class="km">1</span>312 MWh Strom · 41 t Stahl · 19 t CO₂ · gemessen</span></span></div>
        <p class="why">Das Wortfeld aus dem Briefing wird wörtlich durchgestrichen. Was bleibt, hat eine Einheit.</p>
      </div>
      <div>
        <span class="k">Beispiel 03 · Beratersprech</span>
        <div class="big"><span class="korr"><span class="alt">Transformation</span> <span style="white-space:nowrap"><span class="alt">begleiten.</span><span class="km">1</span></span><span class="neu"><span class="km">1</span>12 Maßnahmen · 4 davon unter 6 Monaten</span></span></div>
        <p class="why">So klingt der Satz, den ein Geschäftsführer nach dem ersten Gespräch weiterverwendet.</p>
      </div>
    </div>
  </div>
</section>

<!-- ============================ BAUKASTEN ============================ -->
<section class="deep" id="bausteine">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Das Produkt als Bild</span>
      <h2>Der modulare Effizienz-Baukasten</h2>
      <p class="muted">Jedes Handlungsfeld ist ein Baustein, gezeichnet wie auf einem Werkstattplan. Neun Felder in zwei Gruppen, genau wie im Baukasten auf der Landingpage: Energie mit Strom, Wärme, Kälte, Druckluft und Speicher, Ressourcen mit Material, Wasser, Reststoffen und Betriebsstoffen. Auf der Landingpage ist der Baukasten ein Rechner: Wer ein Feld wählt, setzt den Stein auf die Platte und sieht daneben eine Beispielmaßnahme mit Einsparung in Prozent; die Summe steht groß in Lime. Im Text heißt der Stein immer Maßnahme.</p>
    </div>
    <div class="modgroups">
      {modules_html()}
    </div>
    <div class="steps"><span class="k">Für jede Maßnahme</span>{steps_html()}</div>
    <p class="muted" style="margin-top:22px;font-size:14px;max-width:70ch">Die Bausteine ersetzen die klassischen Leistungskacheln der Branche. Auf der Landingpage sind sie der Rechner, im Bericht die Kapitelmarken. Wir entscheiden gemeinsam, welche Maßnahmen wir angehen.</p>
  </div>
</section>

<!-- ============================ ICONS + FOTO ============================ -->
<section class="dark">
  <div class="wrap grid2" style="align-items:start">
    <div>
      <span class="eyebrow">Icon-Sprache</span>
      <h2 style="font-size:30px;margin-top:10px">Ein Strich, mit der Hand, in Lime.</h2>
      <p class="muted" style="margin-top:12px;font-size:15px;max-width:48ch">Zwölf Icons: neun Handlungsfelder und drei Schritte. Bewusst nicht perfekt: leicht gewellte Linien, runde Enden, wie mit dem Filzstift auf den Schaltschrank gezeichnet. Auf hellem Grund werden sie Petrol. Zwei davon stehen als Lime-Punkt in den Porträts: Material für Ressourceneffizienz, Strom für Energieeffizienz.</p>
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
          <path d="M330 140 C 320 100, 470 92, 486 150 C 500 200, 470 262, 400 268 C 330 274, 312 220, 322 170 C 326 150, 340 140, 356 136" fill="none" stroke="currentColor" data-ak="s" stroke-width="3.5" stroke-linecap="round"/>
          <path d="M200 70 Q 270 40 330 120" fill="none" stroke="currentColor" data-ak="s" stroke-width="2.5" stroke-linecap="round"/>
          <path d="M318 96 l 12 24 -26 -2" fill="none" stroke="currentColor" data-ak="s" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
          <text x="44" y="62" font-family="Kalam, cursive" font-weight="700" font-size="24" fill="currentColor" data-ak="f">Kompressor 2: Leckage</text>
          <text x="44" y="92" font-family="Kalam, cursive" font-weight="700" font-size="24" fill="currentColor" data-ak="f">11.200 € / Jahr · 5 Monate</text>
          <path d="M60 330 q 12 8 18 22 q 10 -34 34 -50" fill="none" stroke="currentColor" data-ak="s" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
          <text x="128" y="352" font-family="Kalam, cursive" font-weight="700" font-size="22" fill="currentColor" data-ak="f">gemessen 12.09., 14:10</text>
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
      <p class="muted">Für Büro, Messe und LinkedIn. Sand, Petrol und Lime im Wechsel, jedes Motiv mit einer handgezeichneten Linie. Kein Foto, kein Windrad, keine Glühbirne.</p>
    </div>
    <div class="posters">
      <div class="poster sand" style="color:{PETROL}">
        <div class="foot"><span>Wendepunkt Ingenieure</span><span>01 · Kurve</span></div>
        <div class="art"><svg viewBox="0 0 200 200" aria-hidden="true"><path d="M18 168 C 60 172, 66 130, 96 104 C 128 76, 128 30, 184 26" fill="none" stroke="{PETROL}" stroke-width="7" stroke-linecap="round"/><circle cx="100" cy="100" r="13" fill="currentColor" data-ak="f"/><path d="M118 112 q 30 24 52 6" fill="none" stroke="{PETROL}" stroke-width="2.4" stroke-linecap="round"/><text x="132" y="146" font-family="Kalam, cursive" font-weight="700" font-size="17" fill="{PETROL}">hier.</text></svg></div>
        <p class="line">Der Wendepunkt ist der Moment, ab dem es anders läuft. Wir sind ein Büro für Energie- und Ressourceneffizienz und suchen ihn gemeinsam mit Ihnen.</p>
      </div>
      <div class="poster" style="background:{PETROL};color:#fff">
        <div class="foot"><span>Wendepunkt Ingenieure</span><span>02 · Baukasten</span></div>
        <div class="art">{poster_iso()}</div>
        <p class="line">Der Modulare Effizienz-Baukasten. Weniger Verbrauch, mehr Spielraum.</p>
      </div>
      <div class="poster" style="background:var(--accent);color:var(--accent-ink)">
        <div class="foot"><span>Wendepunkt Ingenieure</span><span>03 · Korrektur</span></div>
        <div class="art"><svg viewBox="0 0 200 200" aria-hidden="true">
          <text x="14" y="84" font-family="IBM Plex Sans, sans-serif" font-weight="600" font-size="30" fill="{DEEP}" fill-opacity=".5">behaupten.</text>
          <line x1="12" y1="75" x2="164" y2="75" stroke="{DEEP}" stroke-width="2"/>
          <circle cx="180" cy="62" r="9" fill="none" stroke="{DEEP}" stroke-width="1.6"/><text x="180" y="66" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="11" fill="{DEEP}">1</text>
          <line x1="12" y1="112" x2="190" y2="112" stroke="{DEEP}" stroke-width="1"/>
          <circle cx="22" cy="140" r="9" fill="none" stroke="{DEEP}" stroke-width="1.6"/><text x="22" y="144" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="11" fill="{DEEP}">1</text>
          <text x="40" y="148" font-family="IBM Plex Sans, sans-serif" font-weight="600" font-size="27" fill="{DEEP}" textLength="152" lengthAdjust="spacingAndGlyphs">nachrechnen.</text></svg></div>
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
      <p class="muted">Der Bericht ist das wichtigste Stück, weil der Kunde ihn behält. Papierweiß, Plex, Zahlen in Mono. Die Hand kommt sparsam vor: als Prüfvermerk der beiden Gründer und als kurze Notiz auf Karte und Signatur.</p>
    </div>
    <div class="apps">
      <div class="report">
        <div>
          {logo(PETROL, OCKER, PETROL, size=44, w1=15)}
          <span class="eyebrow" style="display:block;margin-top:34px;color:var(--muted)">Modularer Effizienz-Baukasten · Bericht Nr. 2026-014</span>
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
          <div class="q"><span class="korr"><span class="alt">„PV rechnet sich</span> <span style="white-space:nowrap"><span class="alt">immer.“</span><span class="km">1</span></span><span class="neu"><span class="km">1</span>240 kWp · 31.000 € p. a. · 6,8 Jahre · erst nach Druckluft und Abwärme</span></span></div>
          <div class="foot">{logo("#FFFFFF", OCKER, "#FFFFFF", size=26, w1=11, sub=False)}<span>wendepunkt-ingenieure.de</span></div>
        </div>
        <div class="grid2" style="gap:12px;align-items:stretch">
          <div class="card" style="background:#fff">
            {logo(PETROL, OCKER, PETROL, size=30, w1=11, sub=False)}
            <div class="who"><b>Michael Schenk</b><br>Ressourceneffizienz<br><span class="m">+49 000 0000000 · ms@wendepunkt-ingenieure.de</span></div>
          </div>
          <div class="card" style="background:{PETROL};border-color:{PETROL};justify-content:center;align-items:center">
            <svg viewBox="0 0 64 64" width="120" height="120" style="position:absolute;right:-22px;bottom:-30px" aria-hidden="true"><path d="M6 52 C 30 52 34 12 58 12" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round"/><circle cx="32" cy="32" r="5.5" fill="currentColor" data-ak="f"/></svg>
            <span class="hand" style="color:var(--accent);font-size:20px;position:absolute;left:18px;top:18px;transform:rotate(-4deg)">Ruf einfach an.</span>
          </div>
        </div>
        <div class="sig">
          <b>Tobias Wintsche</b> · Energieeffizienz<br>
          Wendepunkt Ingenieure GbR · Büro für Energie- und Ressourceneffizienz<br>
          <span class="m">+49 000 0000000 · tw@wendepunkt-ingenieure.de · Eisenach / Leipzig</span><br>
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
      <h2>Farben, Schriften, vier Regeln.</h2>
    </div>
    <div class="sw">
      <div><div class="chip" style="background:{PETROL}"></div><div class="lbl"><b>Petrol</b><code>{PETROL}</code></div></div>
      <div><div class="chip" style="background:{DEEP}"></div><div class="lbl"><b>Tiefe</b><code>{DEEP}</code></div></div>
      <div><div class="chip" style="background:var(--accent)"></div><div class="lbl"><b>Lime</b><code>{OCKER}</code></div></div>
      <div><div class="chip" style="background:{PAPER};border-bottom:1px solid var(--line-l)"></div><div class="lbl"><b>Papier</b><code>{PAPER}</code></div></div>
      <div><div class="chip" style="background:{SAND}"></div><div class="lbl"><b>Sand</b><code>{SAND}</code></div></div>
      <div><div class="chip" style="background:{MIST}"></div><div class="lbl"><b>Nebel</b><code>{MIST}</code></div></div>
    </div>
    <div class="type" style="margin-top:24px">
      <div class="row"><span class="k">Headline · Plex Sans 600</span><span style="font-size:30px;font-weight:600;letter-spacing:-.02em;line-height:1.1">Der Wendepunkt ist der Moment, ab dem es anders läuft.</span></div>
      <div class="row"><span class="k">Fließtext · Plex Sans 400</span><span style="font-size:16px">In rund <strong>150 Betrieben</strong> des verarbeitenden Gewerbes haben wir das schon getan.</span></div>
      <div class="row"><span class="k">Zahl · Plex Mono 500</span><span style="font-family:var(--mono);font-size:30px;font-weight:500;color:{PETROL};line-height:1">312 MWh <span style="font-size:13px;color:var(--muted)">Strom p. a.</span></span></div>
      <div class="row"><span class="k">Korrektur · Plex Mono</span><span class="light" style="font-size:26px;font-weight:600;letter-spacing:-.02em"><span class="korr"><span class="alt">Bis zu 40 %</span> <span style="white-space:nowrap"><span class="alt">sparen.</span><span class="km">1</span></span><span class="neu"><span class="km">1</span>18 % · amortisiert in 2,1 Jahren</span></span></span></div>
      <div class="row"><span class="k">Textmarker · Lime-Fläche</span><span style="font-size:26px;font-weight:600;letter-spacing:-.02em;color:{PETROL}">Wir nehmen es <mark class="hl">persönlich</mark>.</span></div>
      <div class="row"><span class="k">Fachgebiet · Plex Sans 600</span><span><span class="pers-role">Ressourceneffizienz</span></span></div>
      <div class="row"><span class="k">Notiz · Kalam 700</span><span class="hand" style="font-size:22px;color:{PETROL}">gemessen 12.09., 14:10</span></div>
    </div>
    <div class="rules" style="margin-top:32px">
      <div><h4>Zwei Marker, zwei Aufgaben.</h4><p>Der Lime-Textmarker hebt hervor, was zählt: ein Wort, höchstens eine Zeile. Das Korrekturzeichen nach DIN 16511 widerlegt eine Behauptung mit der Zahl am Rand. Nie beides im selben Satz.</p></div>
      <div><h4>Lime ist Fläche, nicht Schrift.</h4><p>Auf Petrol trägt Lime Handschrift, Icons, Linien und die Summe im Rechner (9,3 : 1). Auf Papier und Sand nur als Textmarker, Punkt, Unterstrich oder Button-Fläche, immer mit Petrol-Schrift darauf.</p></div>
      <div><h4>Hell zum Kennenlernen, dunkel fürs Produkt.</h4><p>Einstieg und Team auf Sand und Papier. Baukasten, Plakat und LinkedIn auf Petrol. Bericht, Angebot und Brief auf Papier. Kein Punktraster, keine Schatten.</p></div>
      <div><h4>Handschrift heißt: wir persönlich.</h4><p>Notizen an der Kurve, die Zeile „beides zusammen gedacht.“ und der Pfeil zum Erstgespräch in Handschrift, heute Kalam, später die echte von Michael und Tobias. Nie für Headlines oder Fließtext, keine Notiz am Baukasten.</p></div>
    </div>
  </div>
</section>

<!-- ============================ KOMPONENTEN ============================ -->
<section class="mist">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Komponenten</span>
      <h2>Vier Teile, die die Landingpage trägt.</h2>
      <p class="muted">So wie sie auf der Landingpage stehen. Wer ein Angebot, einen Brief oder eine neue Seite baut, nimmt diese Teile und erfindet keine neuen.</p>
    </div>
    <div class="comp">
      <div class="comp-c">
        <div class="comp-s"><a class="wp-cta" href="{LANDING}" target="_top">Kostenfreies Erstgespräch vereinbaren</a></div>
        <h4>Erstgespräch-Button</h4>
        <p>Lime-Fläche, Petrol-Schrift, 2-px-Rahmen, 10 bis 12 px Radius, ohne Icon. Nur einer pro Seite, ganz unten im Baukasten. Dort zeigt ein handgezeichneter Lime-Pfeil darauf.</p>
      </div>
      <div class="comp-c">
        <div class="comp-s" style="flex-direction:column;align-items:flex-start;justify-content:center;gap:8px"><span class="pers-role">Energieeffizienz</span><span style="font-size:26px;font-weight:600;letter-spacing:-.02em;color:{PETROL}">Tobias Wintsche</span></div>
        <h4>Fachgebiet über dem Namen</h4>
        <p>Plex Sans 600 in Petrol mit 3-px-Lime-Unterstrich, direkt über dem Namen. Nicht klein in Mono, nicht mit Punkt neben dem Namen.</p>
      </div>
      <div class="comp-c">
        <div class="comp-s"><div class="pers-ph" style="width:132px">{portrait(1)}</div></div>
        <h4>Porträt mit Symbol</h4>
        <p>Foto im Hochformat 4 : 5, 12 px Radius. In der Ecke ein Lime-Kreis mit dem Symbol des Fachgebiets: Material bei Michael, Strom bei Tobias. Bis die Fotos da sind, stehen gezeichnete Duotone-Porträts.</p>
      </div>
      <div class="comp-c">
        <div class="comp-s" style="background:{PETROL};border-radius:12px;padding:18px 20px;flex-direction:column;align-items:stretch;justify-content:center"><div class="bc-sum" style="border-top:1px solid rgba(255,255,255,.25)"><span>Zusammen<sup>*</sup></span><b>−22 %</b></div><p style="margin:10px 0 0;font-size:11px;color:rgba(255,255,255,.7)"><sup>*</sup>Richtwerte aus unseren Projekten, bezogen auf Energie- und Materialkosten pro Jahr.</p></div>
        <h4>Summe im Rechner</h4>
        <p>Die einzige große Zahl der Seite, in Lime auf Petrol, mit Stern und Fußnote. Einzelwerte stehen pro Maßnahme darüber, die Summe wächst beim Auswählen.</p>
      </div>
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
        <ul><li>Dunkler Petrol-Grund (das Punktraster haben wir weggelassen)</li><li>Isometrische Bausteine als Produktbild</li><li>Schraffuren als Zustand, nicht als Deko</li><li>Kleine Label in Mono</li></ul>
        <p class="no"><b>Entschieden:</b> das Neongrün, bei uns als Lime #C8F04A. Nur als Marker und Fläche, nie als Schrift auf hellem Grund.</p>
      </div>
      <div>
        <h4>The Academy for Climate Jobs</h4>
        <ul><li>Durchstreichen und korrigieren, bei uns als Korrekturzeichen nach DIN 16511</li><li>Textmarker für das, was zählt, bei uns in Lime</li><li>Handgezeichnete Icons auf dunklem Grund</li><li>Fotos mit Annotation darüber</li></ul>
        <p class="no"><b>Nicht übernommen:</b> Kreisel-Kritzeleien um Gesichter. Bei uns markiert die Hand Zahlen und Kernaussagen, nicht Menschen.</p>
      </div>
      <div>
        <h4>Claude / Anthropic</h4>
        <ul><li>Warmes Papier und Sand statt Reinweiß</li><li>Plakatserie mit einer Linie pro Motiv</li><li>Ruhige Grotesk, Mono für Zahlen</li><li>Geschäftsausstattung als Gegenstand gedacht</li></ul>
        <p class="no"><b>Nicht übernommen:</b> Terrakotta. Die Farbe gehört Anthropic.</p>
      </div>
    </div>
    <p class="muted" style="margin-top:28px;font-size:14px;max-width:72ch">Offen zur Entscheidung: Ob die Notiz-Handschrift Kalam bleibt oder durch die echte Handschrift von Michael oder Tobias ersetzt wird. Das wäre der ehrlichste Marker und rechtlich sauber. Dafür brauche ich eine Seite mit den Ziffern 0 bis 9, dem Prozentzeichen, „Jahre“, „Monate“ und ein Häkchen, mit dickem Filzstift geschrieben und fotografiert.</p>
  </div>
</section>

<script>
(function(){{
  var bg=document.getElementById('burger'), mn=document.getElementById('menu');
  function setMenu(open){{ if(!bg||!mn) return; bg.setAttribute('aria-expanded',open?'true':'false'); bg.setAttribute('aria-label',open?'Menü schließen':'Menü öffnen'); if(open){{mn.hidden=false; void mn.offsetWidth; mn.classList.add('open');}} else {{mn.classList.remove('open'); mn.hidden=true;}} }}
  if(bg&&mn){{
    bg.addEventListener('click',function(){{ setMenu(bg.getAttribute('aria-expanded')!=='true'); }});
    mn.addEventListener('click',function(e){{ if(e.target.closest('a')) setMenu(false); }});
    document.addEventListener('keydown',function(e){{ if(e.key==='Escape') setMenu(false); }});
    document.addEventListener('click',function(e){{ if(!mn.hidden && !e.target.closest('header')) setMenu(false); }});
  }}
  var art=document.querySelector('.wp-art'), mq=window.matchMedia('(max-width:640px)');
  function crop(){{ if(art) art.setAttribute('viewBox', mq.matches ? '0 10 520 272' : '0 0 600 320'); }}
  crop(); if(mq.addEventListener) mq.addEventListener('change',crop);
  var els=document.querySelectorAll('.hl,.pers .pers-q span,.team-link,.bk-link,.cta-arrow');
  if(!('IntersectionObserver' in window)){{Array.prototype.forEach.call(els,function(e){{e.classList.add('on');}});return;}}
  var io=new IntersectionObserver(function(es){{es.forEach(function(en){{if(en.isIntersecting){{en.target.classList.add('on');io.unobserve(en.target);}}}});}},{{threshold:.6}});
  Array.prototype.forEach.call(els,function(e){{io.observe(e);}});
}})();
</script>
<script>
(function(){{
  var C30=Math.cos(Math.PI/6), S30=0.5, S=34;
  function iso(x,y,z){{return [(x-y)*C30*S,(x+y)*S30*S-z*S];}}
  function P(pts){{return pts.map(function(p){{return p[0].toFixed(1)+','+p[1].toFixed(1)}}).join(' ');}}
  var G={{
    strom:'<path d="M.56 .1 L.28 .56 H.5 L.42 .9 L.74 .42 H.52 Z"/>',
    waerme:'<path class="flow" pathLength="1" d="M.2 .85 C.35 .65 .05 .45 .2 .15 M.5 .85 C.65 .65 .35 .45 .5 .15 M.8 .85 C.95 .65 .65 .45 .8 .15"/>',
    kaelte:'<path d="M.5 .12 V.88 M.17 .31 L.83 .69 M.17 .69 L.83 .31 M.42 .18 L.5 .26 L.58 .18 M.42 .82 L.5 .74 L.58 .82"/>',
    druckluft:'<ellipse cx=".36" cy=".5" rx=".2" ry=".2"/><circle cx=".36" cy=".5" r=".07"/><path class="flow" pathLength="1" d="M.56 .5 H.92"/>',
    material:'<path d="M.14 .2 H.66 V.5 H.14 Z M.28 .36 H.8 V.66 H.28 Z"/><path class="flow" pathLength="1" d="M.1 .86 H.9"/>',
    wasser:'<path d="M.5 .12 C.63 .32 .72 .44 .72 .56 A .22 .22 0 0 1 .28 .56 C.28 .44 .37 .32 .5 .12 Z"/><path class="flow" pathLength="1" d="M.08 .9 C.3 .8 .7 1 .92 .9"/>',
    reststoffe:'<path d="M.2 .3 H.8 L.72 .86 H.28 Z M.14 .3 H.86"/><path class="flow" pathLength="1" d="M.62 .12 C.9 .12 .9 .3 .8 .3"/>',
    betriebsstoffe:'<ellipse cx=".5" cy=".24" rx=".26" ry=".1"/><path d="M.24 .24 V.78 A .26 .1 0 0 0 .76 .78 V.24 M.24 .44 A .26 .1 0 0 0 .76 .44 M.24 .62 A .26 .1 0 0 0 .76 .62"/>',
    speicher:'<path d="M.14 .3 H.8 V.7 H.14 Z M.8 .42 H.9 V.58 H.8"/><path d="M.28 .38 V.62 M.41 .38 V.62 M.54 .38 V.62"/>',
    pv:'<path d="M.12 .14 H.88 V.86 H.12 Z M.12 .38 H.88 M.12 .62 H.88 M.37 .14 V.86 M.63 .14 V.86"/>'
  }};
  var PR={{strom:'Antriebe',waerme:'Härteofen',kaelte:'Kältemaschine',druckluft:'Kompressor',material:'Stanzlinie',wasser:'Spülbad',reststoffe:'Ausschuss',betriebsstoffe:'Kühlschmierstoff',speicher:'Lastspitze',pv:'Dachfläche'}};
  function unit(a,b){{var dx=b[0]-a[0],dy=b[1]-a[1],l=Math.hypot(dx,dy);return [dx/l,dy/l];}}
  function rpath(pts,r){{
    var n=pts.length, A=[], B=[];
    for(var i=0;i<n;i++){{var p=pts[i],pr=pts[(i+n-1)%n],nx=pts[(i+1)%n];
      var u1=unit(p,pr),u2=unit(p,nx),l1=Math.hypot(pr[0]-p[0],pr[1]-p[1]),l2=Math.hypot(nx[0]-p[0],nx[1]-p[1]),rr=Math.min(r,l1*.35,l2*.35);
      A.push([p[0]+u1[0]*rr,p[1]+u1[1]*rr]); B.push([p[0]+u2[0]*rr,p[1]+u2[1]*rr]);}}
    var f=function(q){{return q[0].toFixed(1)+' '+q[1].toFixed(1);}};
    var d='M'+f(B[0]);
    for(var j=1;j<=n;j++){{var k=j%n; d+=' L'+f(A[k])+' Q'+f(pts[k])+' '+f(B[k]);}}
    return d+' Z';
  }}
  var cid=0;
  function block(x,y,z,w,d,h,hatch,cls,title,id){{
    var T=[iso(x,y,z+h),iso(x+w,y,z+h),iso(x+w,y+d,z+h),iso(x,y+d,z+h)];
    var L=[iso(x,y+d,z),iso(x+w,y+d,z),iso(x+w,y+d,z+h),iso(x,y+d,z+h)];
    var R=[iso(x+w,y,z),iso(x+w,y+d,z),iso(x+w,y+d,z+h),iso(x+w,y,z+h)];
    var sil=[T[0],T[1],R[0],R[1],L[0],T[3]], rad=h<.5?6:11, sp=rpath(sil,rad), k='bc'+(cid++);
    var o='<g class="blk '+(cls||'')+'"'+(id?' data-id="'+id+'"':'')+'>'+(title?'<title>'+title+'</title>':'');
    o+='<clipPath id="'+k+'"><path d="'+sp+'"/></clipPath><g clip-path="url(#'+k+')">';
    o+='<polygon points="'+P(L)+'" fill="#0B3236"/><polygon points="'+P(R)+'" fill="#0E393D"/><polygon points="'+P(T)+'" fill="#14474C"/>';
    for(var i=1;i<hatch;i++){{var t=i/hatch;var a=[R[0][0]+(R[1][0]-R[0][0])*t,R[0][1]+(R[1][1]-R[0][1])*t];var b=[R[3][0]+(R[2][0]-R[3][0])*t,R[3][1]+(R[2][1]-R[3][1])*t];
      o+='<line x1="'+a[0].toFixed(1)+'" y1="'+a[1].toFixed(1)+'" x2="'+b[0].toFixed(1)+'" y2="'+b[1].toFixed(1)+'" stroke="currentColor" stroke-width="1" stroke-opacity=".4"/>';}}
    var c=T[2], e1=T[1], e2=T[3], e3=R[1];
    var sh=function(p,q){{var u=unit(p,q);return [p[0]+u[0]*2,p[1]+u[1]*2];}};
    o+='<path d="M'+P([sh(c,e1)])+' L'+P([sh(e1,c)])+' M'+P([sh(c,e2)])+' L'+P([sh(e2,c)])+' M'+P([sh(c,e3)])+' L'+P([sh(e3,c)])+'" fill="none" stroke="currentColor" stroke-width="1.4" stroke-opacity=".75" stroke-linecap="round"/>';
    if(id&&G[id]){{
      var ax=T[1][0]-T[0][0], ay=T[1][1]-T[0][1], cx=T[3][0]-T[0][0], cy=T[3][1]-T[0][1];
      o+='<g transform="matrix('+[ax,ay,cx,cy,T[0][0],T[0][1]].map(function(v){{return v.toFixed(2);}}).join(' ')+')" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="glyph">'+G[id].replace(/<(path|circle|ellipse)/g,'<$1 vector-effect="non-scaling-stroke"')+'</g>';
    }}
    if(id&&PR[id]){{
      var u=unit(L[0],L[1]), v=unit(L[3],L[0]), len=Math.hypot(L[1][0]-L[0][0],L[1][1]-L[0][1]), fs=7.5, lab=PR[id].toUpperCase();
      var est=lab.length*(fs*.6+.3), room=len-14, fit=est>room?' textLength="'+room.toFixed(1)+'" lengthAdjust="spacingAndGlyphs"':'';
      o+='<g transform="matrix('+[u[0],u[1],v[0],v[1],L[0][0],L[0][1]].map(function(n){{return n.toFixed(3);}}).join(' ')+')"><text x="'+(len/2).toFixed(1)+'" y="-8" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="'+fs+'" letter-spacing=".3" fill="currentColor" fill-opacity=".9"'+fit+'>'+lab+'</text></g>';
    }}
    o+='</g><path d="'+sp+'" fill="none" stroke="currentColor" stroke-width="1.6"/>';
    return o+'</g>';
  }}
  var F=[
    {{g:'Energie',id:'strom',n:'Strom',h:2.4,hatch:4}},{{g:'Energie',id:'waerme',n:'Wärme',h:3.2,hatch:6}},{{g:'Energie',id:'kaelte',n:'Kälte',h:1.8,hatch:0}},
    {{g:'Energie',id:'druckluft',n:'Druckluft',h:2.6,hatch:5}},{{g:'Energie',id:'speicher',n:'Speicher',h:1.6,hatch:4}},{{g:'Ressourcen',id:'material',n:'Material',h:2.9,hatch:0}},{{g:'Ressourcen',id:'wasser',n:'Wasser',h:1.5,hatch:0}},
    {{g:'Ressourcen',id:'reststoffe',n:'Reststoffe',h:1.3,hatch:4}},{{g:'Ressourcen',id:'betriebsstoffe',n:'Betriebsstoffe',h:1.2,hatch:0}}];
  var last='strom', why=document.getElementById('why');
  function explain(){{}}
  var sel={{strom:1,waerme:1,druckluft:1,material:1}}, fresh={{}};
  var EX={{strom:['Eigenbedarf erneuerbar decken',6],waerme:['Abwärme aus dem Ofen nutzen',8],kaelte:['Kältemaschinen bedarfsgerecht nutzen',3],druckluft:['Leckagen abdichten',4],speicher:['Lastspitzen kappen',3],material:['Verschnitt reduzieren',5],wasser:['Spülbad im Kreis führen',2],reststoffe:['Ausschuss senken',3],betriebsstoffe:['Kühlschmierstoff pflegen',2]}};
  var slot=1.7, gap=.35, cols=3, rows=Math.ceil(F.length/cols), px=cols*slot+(cols+1)*gap, py=rows*slot+(rows+1)*gap, pz=.32;
  var plateEl=document.getElementById('plate'), chips=document.getElementById('chips');
  function render(){{
    cid=0;
    var parts=[];
    parts.push(block(0,0,0,px,py,pz,0,'','Modularer Effizienz-Baukasten'));
    var items=[];
    F.forEach(function(f,i){{var gx=i%cols, gy=Math.floor(i/cols); var x=gap+gx*(slot+gap), y=gap+gy*(slot+gap); items.push({{f:f,x:x,y:y}});}});
    items.forEach(function(it){{
      if(!sel[it.f.id]){{var q=[iso(it.x,it.y,pz),iso(it.x+slot,it.y,pz),iso(it.x+slot,it.y+slot,pz),iso(it.x,it.y+slot,pz)];
        parts.push('<path class="slot" d="'+rpath(q,8)+'" fill="none" stroke="currentColor" stroke-width="1"/>');}}
    }});
    items.sort(function(a,b){{return (a.x+a.y)-(b.x+b.y);}}).forEach(function(it){{
      if(sel[it.f.id]) parts.push(block(it.x,it.y,pz,slot,slot,it.f.h,it.f.hatch,'stone'+(fresh[it.f.id]?' new':''),it.f.n+' · '+PR[it.f.id],it.f.id));
    }});
    var c=iso(px,py,0), l=iso(0,py,0), r=iso(px,0,0), t=iso(0,0,3.8);
    var x0=l[0]-30, x1=r[0]+30, y0=t[1]-20, y1=c[1]+14;
    plateEl.innerHTML='<svg viewBox="'+x0.toFixed(0)+' '+y0.toFixed(0)+' '+(x1-x0).toFixed(0)+' '+(y1-y0).toFixed(0)+'" role="img" aria-label="Isometrischer Effizienz-Baukasten">'+parts.join('')+'</svg>';
    fresh={{}};
    Array.prototype.forEach.call(plateEl.querySelectorAll('.blk.stone'),function(g,i){{g.style.animationDelay=plateEl.classList.contains('built')?'0s':(0.12+i*0.11)+'s';}});
    Array.prototype.forEach.call(chips.querySelectorAll('.chip'),function(b){{b.setAttribute('aria-pressed',sel[b.dataset.id]?'true':'false');}});
    calc();
  }}
  var rowsEl=document.getElementById('bc-rows'), totEl=document.getElementById('bc-total');
  function calc(){{
    if(!rowsEl) return;
    var sum=0, h='';
    var n=0;
    F.forEach(function(f){{ if(!EX[f.id]||!sel[f.id]) return; n++; sum+=EX[f.id][1];
      h+='<li><span class="bc-f">'+f.n+'</span><span class="bc-m">'+EX[f.id][0]+'</span><b>−'+EX[f.id][1]+' %</b></li>'; }});
    for(var k=n;k<F.length;k++) h+='<li class="ph" aria-hidden="true"><span class="bc-f">&nbsp;</span><span class="bc-m">&nbsp;</span><b>&nbsp;</b></li>';
    rowsEl.innerHTML=h;
    totEl.textContent='−'+sum+' %';
    totEl.classList.remove('tick'); void totEl.offsetWidth; totEl.classList.add('tick');
  }}
  var NOTE={{strom:'Strom: erst den Lastgang, dann die Technik.',waerme:'Wärme: oft hilft schon ein Abgleich.',kaelte:'Kälte: läuft die Maschine nachts durch?',druckluft:'Druckluft: wir hören erst nach Leckagen.',speicher:'Speicher: nur, wenn die Lastspitze es hergibt.',material:'Material: im Verschnitt steckt oft mehr als im Strom.',wasser:'Wasser: geht das im Kreis?',reststoffe:'Reststoffe: Ausschuss ist bezahltes Material.',betriebsstoffe:'Betriebsstoffe: Öle und Gase zählen mit.'}};
  var hn=document.getElementById('hnote'), ht=document.getElementById('hnote-t');
  function note(id){{ if(!ht||!NOTE[id]) return; ht.textContent=NOTE[id]; hn.classList.remove('pop'); void hn.offsetWidth; hn.classList.add('pop'); }}
  var curG='';
  F.forEach(function(f){{
    if(f.g!==curG){{curG=f.g; var lb=document.createElement('span'); lb.className='grp'; lb.textContent=f.g; chips.appendChild(lb);}}
    var b=document.createElement('button');b.type='button';b.className='chip';b.dataset.id=f.id;
    b.innerHTML='<svg viewBox="0 0 16 16" aria-hidden="true"><rect x="2" y="2" width="12" height="12" rx="4" fill="none" stroke="currentColor" stroke-width="1.5"/><path class="ck" d="M4.5 8.5 L7 11 L11.5 5.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'+f.n;
    b.addEventListener('click',function(){{ plateEl.classList.add('on'); plateEl.classList.add('built'); if(sel[f.id]){{delete sel[f.id];}} else {{sel[f.id]=1;fresh[f.id]=1;}} render(); }});
    chips.appendChild(b);}});
  if('IntersectionObserver' in window){{
    var cio=new IntersectionObserver(function(es){{es.forEach(function(en){{if(en.isIntersecting){{plateEl.classList.add('on');cio.unobserve(en.target);setTimeout(function(){{plateEl.classList.add('built');}},1800);}}}});}},{{threshold:.4}});
    cio.observe(plateEl);
  }} else {{plateEl.classList.add('on');plateEl.classList.add('built');}}
  render();

}})();
</script>
'''

# Aufteilen: Landingpage (index.html) und Markensystem (markensystem.html).
# Veröffentlichte Landingpage; das Menü im Markensystem verlinkt dorthin.
import os
M_SYS = "<!-- ============================ MARKENSYSTEM ============================ -->"
M_END = "\n<script>\n(function(){\n  var bg="
M_HEAD = "<!-- ============================ 1 · WENDEPUNKT (Start) ============================ -->"
i_sys, i_end, i_head = html.index(M_SYS), html.index(M_END), html.index(M_HEAD)
head, landing, system, scripts = html[:i_head], html[i_head:i_sys], html[i_sys:i_end], html[i_end:]
observer = scripts[:scripts.index("</script>") + len("</script>")]

landing_html = head.replace('<title>Wendepunkt Markenwelt</title>', '<title>Wendepunkt Landingpage</title>') + landing + scripts
system_html = (head.replace("<title>Wendepunkt Markenwelt</title>", "<title>Wendepunkt Markensystem</title>")
               .replace('href="#start"', 'href="' + LANDING + '" target="_top"').replace('href="#team"', 'href="' + LANDING + '" target="_top"')
               .replace('href="#baukasten"', 'href="' + LANDING + '" target="_top"').replace('href="#kontakt" class="mcta"', 'href="' + LANDING + '" target="_top" class="mcta"')
               + system.replace("Ab hier: Markensystem", "Markensystem") + observer + "\n")

d = "/home/user/design-system/markenwelt/"
os.makedirs(d, exist_ok=True)
for name, doc in (("index.html", landing_html), ("markensystem.html", system_html)):
    open(d + name, "w").write(doc)
    print("written", name, len(doc))

# ---------- Marken-Paket für Claude Design (brand/) ----------
# Stilvorlage und Leitfaden ohne React-Komponenten. Werte kommen aus den
# Konstanten oben, damit Seite und Paket nicht auseinanderlaufen.
B = "/home/user/design-system/brand/"
os.makedirs(B + "docs", exist_ok=True)
brand_css = f"""/* Wendepunkt Ingenieure · Marken-Stilvorlage (generiert aus markenwelt/build.py) */
@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&family=Kalam:wght@400;700&display=swap");

:root {{
  /* Farben */
  --wp-petrol: {PETROL};
  --wp-deep: {DEEP};
  --wp-lime: {OCKER};
  --wp-paper: {PAPER};
  --wp-sand: {SAND};
  --wp-mist: {MIST};
  --wp-ink: {INK};
  --wp-muted: #4E5A5B;
  --wp-line-light: #D8D3C8;
  --wp-line-dark: rgba(255,255,255,.14);
  /* Schriften */
  --wp-sans: "IBM Plex Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
  --wp-mono: "IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
  --wp-hand: "Kalam", "Segoe Print", "Bradley Hand", cursive;
  /* Form */
  --wp-radius: 12px;
  --wp-radius-sm: 10px;
  --wp-maxw: 1200px;
}}

/* Grundlage */
.wp-body {{ margin: 0; background: var(--wp-paper); color: var(--wp-ink); font-family: var(--wp-sans); font-size: 16px; line-height: 1.55; -webkit-font-smoothing: antialiased; }}
.wp-wrap {{ max-width: var(--wp-maxw); margin: 0 auto; padding-inline: 24px; }}
.wp-section {{ padding-block: 72px; }}

/* Flächen: hell zum Kennenlernen, dunkel fürs Produkt */
.wp-paper {{ background: var(--wp-paper); color: var(--wp-ink); }}
.wp-sand {{ background: var(--wp-sand); color: var(--wp-ink); }}
.wp-mist {{ background: var(--wp-mist); color: var(--wp-ink); }}
.wp-petrol {{ background: var(--wp-petrol); color: #fff; }}
.wp-deep {{ background: var(--wp-deep); color: #fff; }}

/* Typografie */
.wp-h1 {{ font-family: var(--wp-sans); font-weight: 600; font-size: clamp(34px, 5vw, 56px); line-height: 1.05; letter-spacing: -.02em; text-wrap: balance; margin: 0; }}
.wp-h2 {{ font-family: var(--wp-sans); font-weight: 600; font-size: clamp(28px, 3.6vw, 40px); line-height: 1.1; letter-spacing: -.02em; text-wrap: balance; margin: 0; }}
.wp-h3 {{ font-family: var(--wp-sans); font-weight: 600; font-size: 26px; line-height: 1.15; letter-spacing: -.02em; margin: 0; }}
.wp-lead {{ font-size: 19px; line-height: 1.5; max-width: 52ch; }}
.wp-eyebrow {{ font-family: var(--wp-mono); font-size: 12px; letter-spacing: .1em; text-transform: uppercase; opacity: .75; }}
.wp-num {{ font-family: var(--wp-mono); font-weight: 500; font-variant-numeric: tabular-nums; }}
.wp-hand {{ font-family: var(--wp-hand); font-weight: 700; line-height: 1.15; }}
.wp-muted {{ color: var(--wp-muted); }}

/* Lime-Textmarker: hebt hervor, was zählt (ein Wort, höchstens eine Zeile) */
.wp-hl {{ color: inherit; background: linear-gradient(var(--wp-lime), var(--wp-lime)) no-repeat 0 80% / 100% 54%; -webkit-box-decoration-break: clone; box-decoration-break: clone; padding: 0 .15em; }}

/* Fachgebiet über dem Namen */
.wp-role {{ display: inline-block; font-family: var(--wp-sans); font-weight: 600; font-size: 19px; letter-spacing: -.01em; color: var(--wp-petrol); border-bottom: 3px solid var(--wp-lime); padding-bottom: 1px; line-height: 1.2; }}
.wp-petrol .wp-role, .wp-deep .wp-role {{ color: #fff; }}

/* Erstgespräch-Button: Lime-Fläche, Petrol-Schrift und -Rahmen, runde Ecken, keine Pille */
.wp-cta {{ display: inline-flex; align-items: center; gap: 14px; background: var(--wp-lime); color: var(--wp-petrol); border: 2px solid var(--wp-petrol); font: 600 16px/1 var(--wp-sans); padding: 16px 24px; border-radius: var(--wp-radius); text-decoration: none; cursor: pointer; transition: transform .2s ease, box-shadow .2s ease; }}
.wp-cta:hover, .wp-cta:focus-visible {{ transform: translate(-3px, -3px); box-shadow: 3px 3px 0 var(--wp-petrol); }}
.wp-petrol .wp-cta, .wp-deep .wp-cta {{ border-color: var(--wp-lime); }}
.wp-link {{ color: inherit; text-decoration: underline; text-decoration-color: var(--wp-lime); text-decoration-thickness: 2px; text-underline-offset: 3px; }}

/* Korrekturzeichen nach DIN 16511: Behauptung gestrichen, Wert am Rand */
.wp-korr {{ display: block; }}
.wp-korr .wp-alt {{ color: rgba(26,26,24,.42); background: linear-gradient(var(--wp-petrol), var(--wp-petrol)) no-repeat 0 58% / 100% 2px; -webkit-box-decoration-break: clone; box-decoration-break: clone; }}
.wp-korr .wp-km {{ display: inline-grid; place-items: center; width: 1.5em; height: 1.5em; border: 1.5px solid var(--wp-petrol); border-radius: 50%; font: 500 11px/1 var(--wp-mono); color: var(--wp-petrol); vertical-align: .9em; margin-left: .4em; letter-spacing: 0; }}
.wp-korr .wp-neu {{ display: flex; gap: 10px; align-items: baseline; margin-top: .55em; padding-top: .55em; border-top: 1px solid var(--wp-petrol); font-family: var(--wp-mono); font-weight: 500; font-size: max(13px, .42em); line-height: 1.4; letter-spacing: 0; color: var(--wp-petrol); }}
.wp-korr .wp-neu .wp-km {{ vertical-align: 0; margin: 0; flex: none; }}
.wp-petrol .wp-korr .wp-alt, .wp-deep .wp-korr .wp-alt {{ color: rgba(255,255,255,.5); background-image: linear-gradient(var(--wp-lime), var(--wp-lime)); }}
.wp-petrol .wp-korr .wp-km, .wp-deep .wp-korr .wp-km {{ border-color: var(--wp-lime); color: var(--wp-lime); }}
.wp-petrol .wp-korr .wp-neu, .wp-deep .wp-korr .wp-neu {{ border-color: var(--wp-lime); color: var(--wp-lime); }}

/* Summe (große Zahl in Lime, nur auf Petrol) */
.wp-sum {{ display: flex; justify-content: space-between; align-items: baseline; padding-top: 10px; border-top: 1px solid rgba(255,255,255,.25); font-size: 12px; letter-spacing: .06em; text-transform: uppercase; color: #fff; }}
.wp-sum b {{ font-family: var(--wp-sans); font-weight: 600; font-size: 34px; line-height: 1; color: var(--wp-lime); letter-spacing: -.02em; font-variant-numeric: tabular-nums; white-space: nowrap; }}
.wp-foot {{ font-size: 11px; line-height: 1.45; opacity: .7; }}

/* Karte: Linie statt Schatten */
.wp-card {{ background: #fff; border: 1px solid var(--wp-line-light); border-radius: var(--wp-radius); padding: 20px; }}
.wp-petrol .wp-card, .wp-deep .wp-card {{ background: transparent; border-color: var(--wp-line-dark); }}

/* Logo (Markup siehe guidelines/docs/logo.md) */
.wp-logo {{ display: inline-flex; align-items: center; gap: 12px; }}
.wp-logo .wp-w1 {{ font: 600 22px/1.05 var(--wp-sans); letter-spacing: -.01em; }}
.wp-logo .wp-w2 {{ font: 400 22px/1.05 var(--wp-sans); letter-spacing: -.01em; }}

/* Icons (Markup siehe guidelines/docs/icons.md) */
.wp-icon {{ width: 32px; height: 32px; fill: none; stroke: currentColor; stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; }}
.wp-badge {{ display: inline-grid; place-items: center; width: 34px; height: 34px; border-radius: 50%; background: var(--wp-lime); color: var(--wp-petrol); }}
.wp-badge .wp-icon {{ width: 20px; height: 20px; stroke-width: 3; }}
"""
open(B + "styles.css", "w").write(brand_css)

# Icons als Leitfaden (nur die freigegebenen: neun Felder, drei Schritte)
ICON_SET = ["Strom", "Wärme", "Kälte", "Druckluft", "Speicher", "Material", "Wasser", "Reststoffe", "Betriebsstoffe", "Messen", "Nachrechnen", "Umsetzen"]
icons_md = ["# Icons", "", "Zwölf handgezeichnete Linien-Icons: neun Handlungsfelder und drei Schritte. Immer `viewBox=\"0 0 40 40\"`, Klasse `wp-icon` (Linie 2,2, runde Enden, keine Füllung). Farbe über `color`: Lime auf Petrol, Petrol auf hellem Grund. Keine anderen Icon-Sets, keine Windräder, Glühbirnen, Blätter, Weltkugeln, kein PV-Symbol.", "", "Im Porträt steht das Fachgebiet als Lime-Kreis `wp-badge`: Material für Ressourceneffizienz (Michael), Strom für Energieeffizienz (Tobias).", ""]
for n in ICON_SET:
    icons_md += [f"## {n}", "", "```html", f'<svg class="wp-icon" viewBox="0 0 40 40" aria-hidden="true">{ICONS[n]}</svg>', "```", ""]
open(B + "docs/icons.md", "w").write("\n".join(icons_md))
print("written brand/")
