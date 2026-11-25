"""Son Vagon sahne çizimleri (SVG). Tekrar kullanılabilir arka planlar + Yolcu maskotu."""
W, H = 1080, 1920
CX, CY = 540, 900

def P(x, y, z):
    return (CX + x * 640 / z, CY - y * 1000 / z)

def poly(pts, fill, extra=""):
    s = " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
    return f'<polygon points="{s}" fill="{fill}" {extra}/>'

PAL = {
    "mavi": dict(wall="#1c2a3a", wall2="#2b4058", floor="#151d27", floor2="#2a3644", ceil="#d9e6f2",
                 seat="#1f6fb8", seat2="#14538c", light="#eaf6ff", glow="#9fd3ff", win="#05080d",
                 pole="#c8d3dc", end="#24364a", amb="rgba(120,180,255,0.10)"),
    "kirmizi": dict(wall="#1a0606", wall2="#3a0b0b", floor="#0c0303", floor2="#2a0707", ceil="#2a0a0a",
                    seat="#5a1010", seat2="#3a0909", light="#ff2a2a", glow="#ff3b3b", win="#020000",
                    pole="#7a2a2a", end="#2a0808", amb="rgba(255,30,30,0.18)"),
}

def defs(p):
    return f'''<defs>
<linearGradient id="fl" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{p['floor2']}"/><stop offset="1" stop-color="{p['floor']}"/></linearGradient>
<linearGradient id="wl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{p['wall2']}"/><stop offset="1" stop-color="{p['wall']}"/></linearGradient>
<linearGradient id="wr" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="{p['wall2']}"/><stop offset="1" stop-color="{p['wall']}"/></linearGradient>
<linearGradient id="win" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b1420"/><stop offset="1" stop-color="{p['win']}"/></linearGradient>
<radialGradient id="fog" cx="0.5" cy="0.47" r="0.6"><stop offset="0" stop-color="#000" stop-opacity="0.85"/><stop offset="0.25" stop-color="#000" stop-opacity="0.35"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
<radialGradient id="vig" cx="0.5" cy="0.5" r="0.75"><stop offset="0.55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.85"/></radialGradient>
<linearGradient id="hood" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff9a3c"/><stop offset="0.6" stop-color="#f26a12"/><stop offset="1" stop-color="#b8460a"/></linearGradient>
<radialGradient id="void" cx="0.5" cy="0.45" r="0.6"><stop offset="0" stop-color="#000"/><stop offset="0.8" stop-color="#050505"/><stop offset="1" stop-color="#2a1205"/></radialGradient>
<filter id="blur8"><feGaussianBlur stdDeviation="8"/></filter>
<filter id="blur20"><feGaussianBlur stdDeviation="20"/></filter>
</defs>'''

def car(pal="mavi", lights_on=True):
    p = PAL[pal]
    Z0, Z1 = 0.9, 12
    o = [defs(p)]
    o.append(f'<rect width="{W}" height="{H}" fill="#000"/>')
    # duvarlar, zemin, tavan
    o.append(poly([P(-1, -1, Z0), P(1, -1, Z0), P(1, -1, Z1), P(-1, -1, Z1)], "url(#fl)"))
    o.append(poly([P(-1, 1, Z0), P(1, 1, Z0), P(1, 1, Z1), P(-1, 1, Z1)], p['ceil'] if lights_on else p['ceil']))
    o.append(poly([P(-1, -1, Z0), P(-1, 1, Z0), P(-1, 1, Z1), P(-1, -1, Z1)], "url(#wl)"))
    o.append(poly([P(1, -1, Z0), P(1, 1, Z0), P(1, 1, Z1), P(1, -1, Z1)], "url(#wr)"))
    # zemin şeridi
    for z in range(1, 12):
        o.append(poly([P(-0.05, -1, z), P(0.05, -1, z), P(0.05, -1, z + 0.5), P(-0.05, -1, z + 0.5)], "rgba(255,255,255,0.05)"))
    # pencereler
    for za, zb in [(1.6, 3.0), (3.6, 5.0), (5.6, 7.0), (7.6, 9.0), (9.6, 11.0)]:
        for sx in (-1, 1):
            o.append(poly([P(sx, 0.05, za), P(sx, 0.62, za), P(sx, 0.62, zb), P(sx, 0.05, zb)], "url(#win)",
                          f'stroke="{p["pole"]}" stroke-opacity="0.5" stroke-width="3"'))
            # tünel ışık çizgisi
            o.append(poly([P(sx, 0.30, za), P(sx, 0.33, za), P(sx, 0.36, zb), P(sx, 0.33, zb)], p['glow'], 'opacity="0.25"'))
    # koltuklar
    for sx in (-1, 1):
        for za, zb in [(1.3, 4.6), (5.4, 8.6), (9.3, 11.6)]:
            o.append(poly([P(sx, -0.45, za), P(sx, 0.0, za), P(sx, 0.0, zb), P(sx, -0.45, zb)], p['seat2']))
            o.append(poly([P(sx, -0.45, za), P(sx * 0.68, -0.45, za), P(sx * 0.68, -0.45, zb), P(sx, -0.45, zb)], p['seat']))
            o.append(poly([P(sx * 0.68, -0.45, za), P(sx * 0.68, -1, za), P(sx * 0.68, -1, zb), P(sx * 0.68, -0.45, zb)], "rgba(0,0,0,0.45)"))
    # uç duvar + kapı
    o.append(poly([P(-1, -1, Z1), P(1, -1, Z1), P(1, 1, Z1), P(-1, 1, Z1)], p['end']))
    o.append(poly([P(-0.32, -1, Z1), P(0.32, -1, Z1), P(0.32, 0.62, Z1), P(-0.32, 0.62, Z1)], "#0e141b" if pal == "mavi" else "#140303",
                  f'stroke="{p["pole"]}" stroke-width="2"'))
    o.append(poly([P(-0.2, -0.05, Z1), P(0.2, -0.05, Z1), P(0.2, 0.45, Z1), P(-0.2, 0.45, Z1)], "#000"))
    o.append(f'<rect width="{W}" height="{H}" fill="url(#fog)" opacity="{0.55 if lights_on else 0.8}"/>')
    # tavan ışıkları
    for sx in (-0.4, 0.4):
        for z in [1.2, 2.6, 4.0, 5.4, 6.8, 8.2, 9.6, 11.0]:
            pts = [P(sx - 0.07, 0.99, z), P(sx + 0.07, 0.99, z), P(sx + 0.07, 0.99, z + 0.9), P(sx - 0.07, 0.99, z + 0.9)]
            if lights_on or pal == "kirmizi":
                o.append(poly(pts, p['glow'], 'filter="url(#blur8)" opacity="0.8"'))
                o.append(poly(pts, p['light']))
            else:
                o.append(poly(pts, "#333"))
    # direkler
    for sx in (-0.6, 0.6):
        for z in [1.8, 3.8, 6.0, 8.5, 11.0]:
            x1, y1 = P(sx, -1, z); x2, y2 = P(sx, 1, z)
            w = max(2, 26 / z)
            o.append(f'<rect x="{x1 - w/2:.1f}" y="{y2:.1f}" width="{w:.1f}" height="{y1 - y2:.1f}" fill="{p["pole"]}" rx="{w/2:.1f}"/>')
            o.append(f'<rect x="{x1 - w/2 + w*0.2:.1f}" y="{y2:.1f}" width="{w*0.18:.1f}" height="{y1 - y2:.1f}" fill="#fff" opacity="0.35"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="{p["amb"]}"/>')
    if pal == "kirmizi":
        o.append(f'<circle cx="{CX}" cy="120" r="140" fill="#ff1a1a" filter="url(#blur20)" opacity="0.55"/>')
        o.append(f'<rect x="{CX-60}" y="70" width="120" height="40" rx="10" fill="#ff3030"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')
    return "\n".join(o)

def yolcu(cx, base, s=1.0, back=False):
    """Turuncu kapüşonlu Yolcu. cx: merkez x, base: ayak hizası, s: ölçek. Yüz yok: kapüşon içi karanlık."""
    def t(x, y):
        return f"{cx + x*s:.1f},{base + y*s:.1f}"
    o = []
    o.append(f'<ellipse cx="{cx}" cy="{base+6*s}" rx="{150*s}" ry="{22*s}" fill="#000" opacity="0.55" filter="url(#blur8)"/>')
    # bacaklar
    o.append(f'<path d="M{t(-70,-380)} L{t(-80,-30)} L{t(-20,-30)} L{t(-5,-330)} L{t(5,-330)} L{t(20,-30)} L{t(80,-30)} L{t(70,-380)} Z" fill="#1d2129"/>')
    # ayakkabılar
    o.append(f'<rect x="{cx-100*s:.1f}" y="{base-38*s:.1f}" width="{85*s:.1f}" height="{38*s:.1f}" rx="{16*s:.1f}" fill="#e9e9e9"/>')
    o.append(f'<rect x="{cx+15*s:.1f}" y="{base-38*s:.1f}" width="{85*s:.1f}" height="{38*s:.1f}" rx="{16*s:.1f}" fill="#e9e9e9"/>')
    # gövde (hoodie)
    o.append(f'<path d="M{t(-120,-400)} Q{t(-135,-640)} {t(-60,-700)} L{t(60,-700)} Q{t(135,-640)} {t(120,-400)} Q{t(0,-380)} {t(-120,-400)} Z" fill="url(#hood)"/>')
    # kollar
    o.append(f'<path d="M{t(-110,-680)} Q{t(-175,-560)} {t(-150,-420)} L{t(-110,-420)} Q{t(-120,-560)} {t(-80,-640)} Z" fill="#d9590e"/>')
    o.append(f'<path d="M{t(110,-680)} Q{t(175,-560)} {t(150,-420)} L{t(110,-420)} Q{t(120,-560)} {t(80,-640)} Z" fill="#d9590e"/>')
    if not back:
        o.append(f'<path d="M{t(-55,-480)} L{t(55,-480)} L{t(45,-420)} L{t(-45,-420)} Z" fill="#c5520c" opacity="0.8"/>')  # cep
        o.append(f'<line x1="{cx-14*s}" y1="{base-690*s}" x2="{cx-18*s}" y2="{base-600*s}" stroke="#fff" stroke-width="{4*s}" opacity="0.8"/>')
        o.append(f'<line x1="{cx+14*s}" y1="{base-690*s}" x2="{cx+18*s}" y2="{base-600*s}" stroke="#fff" stroke-width="{4*s}" opacity="0.8"/>')
    # kapüşon
    o.append(f'<ellipse cx="{cx}" cy="{base-790*s}" rx="{92*s}" ry="{108*s}" fill="url(#hood)"/>')
    if back:
        o.append(f'<path d="M{t(0,-895)} Q{t(20,-790)} {t(0,-690)}" stroke="#b8460a" stroke-width="{5*s}" fill="none"/>')
    else:
        o.append(f'<ellipse cx="{cx}" cy="{base-775*s}" rx="{62*s}" ry="{78*s}" fill="url(#void)"/>')
    # rim light
    o.append(f'<ellipse cx="{cx-40*s}" cy="{base-840*s}" rx="{30*s}" ry="{50*s}" fill="#ffd0a0" opacity="0.25" filter="url(#blur8)"/>')
    return "\n".join(o)

def doors(alarm=True):
    p = PAL["kirmizi"]
    o = [defs(p), f'<rect width="{W}" height="{H}" fill="#120404"/>']
    o.append(f'<rect y="1500" width="{W}" height="420" fill="#0a0202"/>')
    for i, (x, lab, name) in enumerate([(70, "A", "MAKİNİST"), (590, "B", "ARKA VAGON")]):
        o.append(f'<rect x="{x}" y="420" width="420" height="1080" rx="14" fill="#1e0707" stroke="#5a1a1a" stroke-width="8"/>')
        if lab == "A":
            # ışık sızıntısı
            o.append(f'<rect x="{x-10}" y="1480" width="440" height="40" fill="#fff4d0" filter="url(#blur20)" opacity="0.9"/>')
            o.append(f'<rect x="{x+400}" y="440" width="18" height="1050" fill="#fff4d0" filter="url(#blur8)" opacity="0.7"/>')
            o.append(f'<rect x="{x+404}" y="440" width="6" height="1050" fill="#fffbe8"/>')
            o.append(f'<rect x="{x+60}" y="560" width="300" height="70" rx="6" fill="#3a0e0e"/>')
            o.append(f'<text x="{x+210}" y="608" font-family="Oswald" font-weight="700" font-size="40" fill="#ffb3b3" text-anchor="middle">{name}</text>')
            o.append(f'<circle cx="{x+360}" cy="1000" r="26" fill="#888"/><rect x="{x+330}" y="1050" width="60" height="40" rx="6" fill="#ff3030"/>')
        else:
            o.append(f'<rect x="{x+80}" y="540" width="260" height="380" rx="10" fill="#050000" stroke="#5a1a1a" stroke-width="6"/>')
            o.append(f'<rect x="{x+80}" y="540" width="260" height="380" rx="10" fill="#ff0000" opacity="0.10"/>')
            # cama dayalı el izi (iz, figür yok)
            o.append(f'<g opacity="0.35" fill="#ffdddd"><ellipse cx="{x+215}" cy="800" rx="38" ry="46"/>' +
                     "".join(f'<rect x="{x+182+k*18}" y="{720 - (6 if k in (1,2) else 0)}" width="12" height="60" rx="6"/>' for k in range(4)) + '</g>')
            o.append(f'<rect x="{x+60}" y="980" width="300" height="70" rx="6" fill="#3a0e0e"/>')
            o.append(f'<text x="{x+210}" y="1028" font-family="Oswald" font-weight="700" font-size="40" fill="#ffb3b3" text-anchor="middle">{name}</text>')
            o.append(f'<rect x="{x+180}" y="1120" width="60" height="140" rx="12" fill="#666"/>')
        o.append(f'<circle cx="{x+210}" cy="1340" r="95" fill="#000" opacity="0.6"/>')
        o.append(f'<text x="{x+210}" y="1385" font-family="Anton" font-size="140" fill="#fff" text-anchor="middle">{lab}</text>')
    if alarm:
        o.append(f'<circle cx="{CX}" cy="180" r="160" fill="#ff1a1a" filter="url(#blur20)" opacity="0.7"/>')
        o.append(f'<rect x="{CX-70}" y="140" width="140" height="44" rx="10" fill="#ff3030"/>')
    o.append(yolcu(CX, 1890, 0.62, back=True))
    o.append(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')
    return "\n".join(o)

def anons():
    p = PAL["mavi"]
    o = [defs(p), f'<rect width="{W}" height="{H}" fill="#0b1118"/>']
    o.append(f'<rect x="60" y="640" width="960" height="300" rx="24" fill="#05070a" stroke="#3a4a5a" stroke-width="10"/>')
    o.append(f'<rect x="90" y="670" width="900" height="240" rx="10" fill="#120800"/>')
    for yy in range(680, 900, 12):
        o.append(f'<line x1="95" y1="{yy}" x2="985" y2="{yy}" stroke="#000" stroke-width="3" opacity="0.6"/>')
    o.append('<text x="540" y="770" font-family="DejaVu Sans Mono" font-weight="bold" font-size="54" fill="#ff8a1a" text-anchor="middle" letter-spacing="4">SAYIN YOLCU,</text>')
    o.append('<text x="540" y="860" font-family="DejaVu Sans Mono" font-weight="bold" font-size="44" fill="#ff8a1a" text-anchor="middle" letter-spacing="2">YERİNİZDEN KALKMAYIN</text>')
    o.append('<rect x="90" y="670" width="900" height="240" fill="#ff8a1a" opacity="0.06" filter="url(#blur20)"/>')
    # hoparlör
    o.append('<circle cx="540" cy="1260" r="190" fill="#151c24" stroke="#3a4a5a" stroke-width="10"/>')
    for r in range(30, 180, 26):
        o.append(f'<circle cx="540" cy="1260" r="{r}" fill="none" stroke="#000" stroke-width="9"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')
    return "\n".join(o)

def station():
    """Son durak: kapalı tren kapıları, peron tabelası."""
    p = PAL["kirmizi"]
    o = [defs(p), f'<rect width="{W}" height="{H}" fill="#0d0303"/>']
    o.append(f'<rect x="0" y="300" width="{W}" height="140" fill="#1b0a0a"/>')
    o.append('<rect x="240" y="320" width="600" height="100" rx="8" fill="#0a1a4a"/>')
    o.append('<text x="540" y="392" font-family="Oswald" font-weight="700" font-size="60" fill="#fff" text-anchor="middle">SON DURAK</text>')
    o.append('<rect x="140" y="520" width="800" height="1300" rx="20" fill="#2a0c0c" stroke="#5a1a1a" stroke-width="10"/>')
    o.append('<rect x="535" y="520" width="10" height="1300" fill="#000"/>')
    for x in (200, 600):
        o.append(f'<rect x="{x}" y="620" width="280" height="520" rx="16" fill="#030000" stroke="#5a1a1a" stroke-width="8"/>')
        o.append(f'<rect x="{x}" y="620" width="280" height="520" rx="16" fill="#ff2020" opacity="0.08"/>')
    o.append('<rect x="440" y="1250" width="200" height="70" rx="10" fill="#300"/>')
    o.append('<text x="540" y="1300" font-family="Oswald" font-weight="700" font-size="40" fill="#ff4040" text-anchor="middle">KİLİTLİ</text>')
    o.append(f'<circle cx="{CX}" cy="150" r="170" fill="#ff1a1a" filter="url(#blur20)" opacity="0.6"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')
    return "\n".join(o)

SCENES = {
    "vagon_mavi": lambda: car("mavi"),
    "vagon_kirmizi": lambda: car("kirmizi", lights_on=False),
    "yolcu_mavi": lambda: car("mavi") + yolcu(CX + 40, 1850, 0.95),
    "yolcu_kirmizi": lambda: car("kirmizi", False) + yolcu(CX + 40, 1850, 0.95),
    "anons": anons,
    "durak": station,
    "kapilar": doors,
}
