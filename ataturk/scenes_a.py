"""Atatürk serisi sahneleri (SVG, sepya). Gerçek kişi fotoğrafı yok: harita, nesne, silüet."""
import math
W, H = 1080, 1920
DEFS = '''<defs>
<radialGradient id="vig" cx="0.5" cy="0.5" r="0.75"><stop offset="0.5" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.85"/></radialGradient>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b2433"/><stop offset="0.55" stop-color="#6b4a33"/><stop offset="0.75" stop-color="#d98c4a"/><stop offset="1" stop-color="#2a1d14"/></linearGradient>
<linearGradient id="paper" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e9dcc0"/><stop offset="1" stop-color="#c9b48c"/></linearGradient>
<linearGradient id="crim" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a0505"/><stop offset="1" stop-color="#7a0f0f"/></linearGradient>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="3"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.18 0"/></filter>
<filter id="b8"><feGaussianBlur stdDeviation="8"/></filter><filter id="b20"><feGaussianBlur stdDeviation="20"/></filter>
</defs>'''
def fin(): return f'<rect width="{W}" height="{H}" filter="url(#grain)"/><rect width="{W}" height="{H}" fill="url(#vig)"/>'

def officer(cx, base, s=1.0, col="#0d0a07"):
    """Genel subay silüeti (arkadan, yüz yok)."""
    t = lambda x, y: f"{cx+x*s:.0f},{base+y*s:.0f}"
    return (f'<path d="M{t(-60,0)} L{t(-50,-330)} L{t(-95,-560)} Q{t(-90,-640)} {t(-30,-660)} L{t(30,-660)} Q{t(90,-640)} {t(95,-560)} L{t(50,-330)} L{t(60,0)} Z" fill="{col}"/>'
            f'<ellipse cx="{cx}" cy="{base-715*s:.0f}" rx="{48*s:.0f}" ry="{56*s:.0f}" fill="{col}"/>'
            f'<path d="M{t(-55,-740)} Q{t(0,-800)} {t(55,-740)} L{t(52,-760)} Q{t(0,-830)} {t(-52,-760)} Z" fill="{col}"/>'
            f'<path d="M{t(95,-560)} L{t(220,-700)} L{t(232,-688)} L{t(110,-530)} Z" fill="{col}"/>')

def dawn():
    o = [DEFS, f'<rect width="{W}" height="{H}" fill="url(#sky)"/>']
    o.append(f'<circle cx="540" cy="1180" r="120" fill="#ffb066" opacity="0.9" filter="url(#b20)"/>')
    o.append(f'<rect y="1200" width="{W}" height="720" fill="#1a1712"/>')
    for i in range(14):
        o.append(f'<line x1="{80+i*70}" y1="{1230+i*25}" x2="{200+i*70}" y2="{1230+i*25}" stroke="#d98c4a" stroke-width="3" opacity="0.35"/>')
    for x, s in ((180, 1.0), (430, 0.7), (760, 0.85), (950, 0.5)):
        o.append(f'<path d="M{x-90*s},1195 L{x+90*s},1195 L{x+70*s},1215 L{x-70*s},1215 Z" fill="#0b0a08"/>'
                 f'<rect x="{x-12*s}" y="{1110*1-0}" width="{8*s}" height="{85}" fill="#0b0a08" transform="translate(0,{(1-s)*60})"/>'
                 f'<rect x="{x-40*s}" y="{1165}" width="{60*s}" height="30" fill="#0b0a08"/>')
    o.append('<path d="M0,1200 Q200,1120 380,1170 Q520,1080 700,1150 Q880,1060 1080,1130 L1080,1210 L0,1210 Z" fill="#14110d"/>')
    o.append(fin()); return "\n".join(o)

def peninsula(marker="BİGALI", mx=600, my=980, arrow=False):
    o = [DEFS, f'<rect width="{W}" height="{H}" fill="#1d3240"/>']
    for k in range(0, H, 60):
        o.append(f'<line x1="0" y1="{k}" x2="{W}" y2="{k}" stroke="#2b4656" stroke-width="2"/>')
    o.append('<path d="M760,360 C700,520 640,620 600,760 C560,900 480,1040 420,1180 C380,1280 330,1380 300,1480 L360,1500 C420,1420 470,1340 540,1260 C640,1140 700,1000 760,880 C820,760 880,600 960,420 Z" fill="url(#paper)" stroke="#6b5434" stroke-width="6"/>')
    o.append('<path d="M960,420 C1000,600 1000,900 1080,1100 L1080,300 Z" fill="url(#paper)" opacity="0.8"/>')
    o.append('<text x="230" y="980" font-family="Oswald" font-weight="500" font-size="40" fill="#9bb7c6" letter-spacing="6" transform="rotate(-62 230 980)">EGE DENİZİ</text>')
    o.append('<text x="900" y="1300" font-family="Oswald" font-weight="500" font-size="34" fill="#9bb7c6" letter-spacing="4" transform="rotate(-62 900 1300)">ÇANAKKALE BOĞAZI</text>')
    o.append(f'<circle cx="440" cy="1130" r="16" fill="#c0392b"/><text x="160" y="1210" font-family="Oswald" font-weight="700" font-size="44" fill="#ffd2c8" stroke="#000" stroke-width="7" paint-order="stroke fill">ARIBURNU</text>')
    o.append(f'<circle cx="{mx}" cy="{my}" r="22" fill="#0d0a07"/><circle cx="{mx}" cy="{my}" r="44" fill="none" stroke="#c0392b" stroke-width="6"/>')
    o.append(f'<text x="{mx+60}" y="{my+14}" font-family="Oswald" font-weight="700" font-size="50" fill="#fff6e0" stroke="#000" stroke-width="8" paint-order="stroke fill">{marker}</text>')
    if arrow:
        o.append(f'<path d="M{mx},{my} Q{mx-120},{my+40} 470,1110" stroke="#c0392b" stroke-width="12" fill="none" stroke-dasharray="30 18"/>')
        o.append('<polygon points="455,1100 500,1090 480,1135" fill="#c0392b"/>')
    o.append(fin()); return "\n".join(o)

def telegram():
    o = [DEFS, f'<rect width="{W}" height="{H}" fill="#14100b"/>']
    o.append('<g transform="rotate(-4 540 960)"><rect x="110" y="560" width="860" height="760" fill="url(#paper)"/>')
    o.append('<text x="540" y="660" font-family="Oswald" font-weight="700" font-size="56" fill="#3a2a16" text-anchor="middle" letter-spacing="8">RAPOR</text>')
    o.append('<line x1="180" y1="700" x2="900" y2="700" stroke="#3a2a16" stroke-width="4"/>')
    for i, l in enumerate(["25 NİSAN 1915 · 05.30", "DÜŞMAN ARIBURNU'NA", "ASKER ÇIKARDI.", "19. TÜMEN KOMUTANLIĞINA"]):
        o.append(f'<text x="540" y="{800+i*110}" font-family="DejaVu Sans Mono" font-weight="bold" font-size="{44 if i in (1,2) else 34}" fill="#2a1d10" text-anchor="middle">{l}</text>')
    o.append('<circle cx="820" cy="1230" r="60" fill="none" stroke="#9b2a1f" stroke-width="8" opacity="0.7"/></g>')
    o.append(fin()); return "\n".join(o)

def hill(red=False, n_soldiers=0):
    o = [DEFS, f'<rect width="{W}" height="{H}" fill="{"url(#crim)" if red else "url(#sky)"}"/>']
    o.append('<path d="M0,1350 Q300,1100 560,1180 Q800,1250 1080,1050 L1080,1920 L0,1920 Z" fill="#0f0c09"/>')
    o.append(officer(600, 1200, 0.8))
    for i in range(n_soldiers):
        x = 120 + i * 110; y = 1450 + (i % 2) * 30
        o.append(f'<ellipse cx="{x}" cy="{y}" rx="60" ry="18" fill="#000" opacity="0.9"/><line x1="{x+30}" y1="{y-10}" x2="{x+110}" y2="{y-50}" stroke="#7a7a7a" stroke-width="5"/>')
    o.append(fin()); return "\n".join(o)

def clock(h=10, m=0, broken=False, red=False):
    o = [DEFS, f'<rect width="{W}" height="{H}" fill="{"url(#crim)" if red else "#120e0a"}"/>']
    cx, cy, r = 540, 1060, 300
    o.append(f'<circle cx="{cx}" cy="{cy-r-40}" r="40" fill="none" stroke="#b08d4a" stroke-width="14"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r+30}" fill="#b08d4a"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="#efe4c8"/>')
    for k in range(12):
        a = k * math.pi / 6
        o.append(f'<line x1="{cx+math.sin(a)*(r-20):.0f}" y1="{cy-math.cos(a)*(r-20):.0f}" x2="{cx+math.sin(a)*(r-55):.0f}" y2="{cy-math.cos(a)*(r-55):.0f}" stroke="#2a1d10" stroke-width="10"/>')
    ah = (h % 12 + m / 60) * math.pi / 6; am = m * math.pi / 30
    o.append(f'<line x1="{cx}" y1="{cy}" x2="{cx+math.sin(ah)*170:.0f}" y2="{cy-math.cos(ah)*170:.0f}" stroke="#1a120a" stroke-width="18" stroke-linecap="round"/>')
    o.append(f'<line x1="{cx}" y1="{cy}" x2="{cx+math.sin(am)*240:.0f}" y2="{cy-math.cos(am)*240:.0f}" stroke="#1a120a" stroke-width="10" stroke-linecap="round"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="16" fill="#1a120a"/>')
    if broken:
        for a, l in ((20, 260), (75, 200), (140, 280), (210, 230), (290, 270), (330, 180)):
            ar = math.radians(a)
            o.append(f'<polyline points="{cx+40},{cy-30} {cx+40+math.cos(ar)*l*0.5:.0f},{cy-30+math.sin(ar)*l*0.5+15:.0f} {cx+40+math.cos(ar)*l:.0f},{cy-30+math.sin(ar)*l:.0f}" fill="none" stroke="#3a2a16" stroke-width="5"/>')
        o.append(f'<circle cx="{cx+40}" cy="{cy-30}" r="34" fill="#3a2a16" opacity="0.8"/>')
    o.append(fin()); return "\n".join(o)

def crimson():
    o = [DEFS, f'<rect width="{W}" height="{H}" fill="url(#crim)"/>']
    o.append('<path d="M0,1500 Q300,1350 560,1420 Q800,1480 1080,1330 L1080,1920 L0,1920 Z" fill="#0f0505"/>')
    for i in range(18):
        x = 30 + i * 60; y = 1480 - abs(9 - i) * 6
        o.append(f'<rect x="{x}" y="{y-90}" width="22" height="90" rx="10" fill="#0f0505"/><circle cx="{x+11}" cy="{y-105}" r="16" fill="#0f0505"/><line x1="{x+11}" y1="{y-90}" x2="{x+30}" y2="{y-200}" stroke="#0f0505" stroke-width="5"/>')
    o.append(fin()); return "\n".join(o)

def question():
    o = [DEFS, f'<rect width="{W}" height="{H}" fill="#120e0a"/>']
    for x, lab, d in ((70, "SAMSUN", "19 MAYIS 1919"), (590, "SAKARYA", "1921")):
        o.append(f'<rect x="{x}" y="760" width="420" height="640" rx="18" fill="#1f1810" stroke="#b08d4a" stroke-width="6"/>')
        o.append(f'<text x="{x+210}" y="1060" font-family="Anton" font-size="92" fill="#efe4c8" text-anchor="middle">{lab}</text>')
        o.append(f'<text x="{x+210}" y="1140" font-family="Oswald" font-weight="500" font-size="44" fill="#b08d4a" text-anchor="middle">{d}</text>')
    o.append(fin()); return "\n".join(o)

SCENES = {"dawn": dawn, "map": lambda: peninsula(), "map_arrow": lambda: peninsula(arrow=True),
          "telegram": telegram, "hill": lambda: hill(), "hill_soldiers": lambda: hill(n_soldiers=8),
          "clock10": lambda: clock(10, 0), "crimson": crimson, "map_conk": lambda: peninsula("CONKBAYIRI", 560, 1020),
          "watch": lambda: clock(5, 37, broken=True, red=True), "question": question}
