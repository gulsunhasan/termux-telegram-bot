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

def kabin(pal="kirmizi", with_yolcu=False):
    """Makinist kabini: ön cam, tünel rayları, kumanda paneli, boş koltuk."""
    p = PAL[pal]
    red = pal == "kirmizi"
    o = [defs(p), f'<rect width="{W}" height="{H}" fill="{"#100303" if red else "#0a1119"}"/>']
    # ön cam (tünel)
    o.append(f'<path d="M60,260 L1020,260 L980,980 L100,980 Z" fill="#020304" stroke="{p["pole"]}" stroke-width="14"/>')
    vx, vy = 540, 560
    o.append(f'<circle cx="{vx}" cy="{vy}" r="60" fill="{"#ff3a1a" if red else "#9fd3ff"}" opacity="0.35" filter="url(#blur20)"/>')
    for i in range(-5, 6):
        o.append(f'<line x1="{vx}" y1="{vy}" x2="{vx + i*190}" y2="980" stroke="#1a1f26" stroke-width="2"/>')
    for x2 in (360, 720):
        o.append(f'<line x1="{vx + (x2-540)*0.02}" y1="{vy}" x2="{x2}" y2="980" stroke="#8a96a3" stroke-width="7"/>')
    for k in range(1, 9):
        y = vy + (980 - vy) * (k / 9) ** 1.8
        hw = (y - vy) / (980 - vy) * 260
        o.append(f'<line x1="{vx-hw}" y1="{y:.0f}" x2="{vx+hw}" y2="{y:.0f}" stroke="#2b2f36" stroke-width="{2+k}"/>')
    # tünel duvar lambaları
    for k in range(1, 7):
        t = (k / 7) ** 1.6
        for sx in (-1, 1):
            x = vx + sx * (40 + t * 430); y = vy - 40 + t * 120
            o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{3+t*14:.0f}" fill="{"#ff5a3a" if red else "#ffd98a"}" opacity="0.8"/>')
    o.append('<path d="M60,260 L1020,260 L980,980 L100,980 Z" fill="#fff" opacity="0.04"/>')
    o.append('<line x1="120" y1="300" x2="420" y2="940" stroke="#fff" stroke-width="10" opacity="0.05"/>')
    # panel
    o.append(f'<path d="M0,960 L1080,960 L1080,1920 L0,1920 Z" fill="{"#1c0707" if red else "#141c26"}"/>')
    o.append(f'<path d="M0,960 L1080,960 L1000,1120 L80,1120 Z" fill="{"#2c0b0b" if red else "#1f2b38"}"/>')
    # ekranlar
    for x, txt in ((150, "YÖN: GERİ"), (600, "OTOMATİK")):
        o.append(f'<rect x="{x}" y="1000" width="330" height="100" rx="8" fill="#020a04" stroke="#333" stroke-width="4"/>')
        o.append(f'<text x="{x+165}" y="1068" font-family="DejaVu Sans Mono" font-weight="bold" font-size="40" fill="{"#ff4a3a" if red else "#38ff7a"}" text-anchor="middle">{txt}</text>')
    # düğmeler
    for i in range(8):
        c = ["#ff3030", "#ffb020", "#30d060", "#3080ff"][i % 4]
        o.append(f'<circle cx="{170 + i*105}" cy="1180" r="22" fill="{c}" opacity="0.9"/>')
    # kumanda kolu
    o.append('<rect x="760" y="1220" width="40" height="200" rx="18" fill="#555"/><circle cx="780" cy="1215" r="42" fill="#d22"/>')
    # boş koltuk
    o.append(f'<path d="M300,1300 Q300,1240 360,1240 L560,1240 Q620,1240 620,1300 L620,1700 L300,1700 Z" fill="{p["seat2"]}"/>')
    o.append(f'<path d="M260,1640 L660,1640 L640,1760 L280,1760 Z" fill="{p["seat"]}"/>')
    o.append('<rect x="440" y="1760" width="40" height="160" fill="#222"/>')
    if with_yolcu:
        o.append(yolcu(780, 1920, 0.78, back=True))
    if red:
        o.append(f'<circle cx="{CX}" cy="130" r="150" fill="#ff1a1a" filter="url(#blur20)" opacity="0.6"/>')
        o.append(f'<rect x="{CX-60}" y="90" width="120" height="40" rx="10" fill="#ff3030"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="{p["amb"]}"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')
    return "\n".join(o)

def ekran():
    """Kabin ekranı yakın plan."""
    p = PAL["mavi"]
    o = [defs(p), f'<rect width="{W}" height="{H}" fill="#070b10"/>']
    o.append('<rect x="60" y="560" width="960" height="560" rx="30" fill="#0c1218" stroke="#3a4a5a" stroke-width="12"/>')
    o.append('<rect x="100" y="600" width="880" height="480" rx="10" fill="#010803"/>')
    for yy in range(606, 1076, 10):
        o.append(f'<line x1="104" y1="{yy}" x2="976" y2="{yy}" stroke="#000" stroke-width="3" opacity="0.5"/>')
    lines = [("OTOMATİK MOD", "#38ff7a", 60, 700), ("YÖN: ◀◀ GERİ", "#ff5a3a", 66, 820), ("HEDEF: ??????", "#38ff7a", 56, 930), ("SÜRÜCÜ: YOK", "#38ff7a", 44, 1030)]
    for t, c, fs, y in lines:
        o.append(f'<text x="540" y="{y}" font-family="DejaVu Sans Mono" font-weight="bold" font-size="{fs}" fill="{c}" text-anchor="middle" letter-spacing="3">{t}</text>')
    o.append('<rect x="100" y="600" width="880" height="480" fill="#38ff7a" opacity="0.05" filter="url(#blur20)"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')
    return "\n".join(o)

def telsiz(red=False):
    """Telsiz ahizesi yakın plan, kanal ekranı, ses dalgası."""
    p = PAL["kirmizi" if red else "mavi"]
    o = [defs(p), f'<rect width="{W}" height="{H}" fill="{"#120404" if red else "#0a1017"}"/>']
    o.append('<path d="M540,330 Q700,300 700,420" stroke="#222" stroke-width="18" fill="none"/>')
    o.append('<rect x="300" y="420" width="480" height="1180" rx="80" fill="#1b1e22" stroke="#3a3f46" stroke-width="10"/>')
    o.append('<rect x="370" y="520" width="340" height="170" rx="14" fill="#1a1000"/>')
    o.append(f'<text x="540" y="590" font-family="DejaVu Sans Mono" font-weight="bold" font-size="40" fill="#ffa21a" text-anchor="middle">KANAL 7</text>')
    o.append(f'<text x="540" y="655" font-family="DejaVu Sans Mono" font-weight="bold" font-size="34" fill="#ffa21a" text-anchor="middle">◉ ALIYOR</text>')
    for r in range(0, 9):
        for c in range(0, 6):
            o.append(f'<circle cx="{400 + c*56}" cy="{800 + r*56}" r="14" fill="#08090a"/>')
    o.append('<rect x="250" y="900" width="60" height="260" rx="20" fill="#2a2e33"/>')
    col = "#ff3b3b" if red else "#7fc8ff"
    import math
    for side in (-1, 1):
        pts = " ".join(f"{540 + side*(330 + k*12):.0f},{1100 + math.sin(k*1.3)*(40+k*6) * (1 if k%2 else -1):.0f}" for k in range(16))
        o.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="6" opacity="0.8"/>')
    o.append(f'<circle cx="540" cy="580" r="220" fill="#ffa21a" opacity="0.08" filter="url(#blur20)"/>')
    if red:
        o.append(f'<circle cx="{CX}" cy="150" r="160" fill="#ff1a1a" filter="url(#blur20)" opacity="0.6"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')
    return "\n".join(o)

def secim2():
    """2. bölüm seçimi: A acil fren kolu, B telsiz."""
    p = PAL["kirmizi"]
    o = [defs(p), f'<rect width="{W}" height="{H}" fill="#120404"/>']
    for x, lab in ((70, "A"), (590, "B")):
        o.append(f'<rect x="{x}" y="420" width="420" height="1080" rx="18" fill="#1e0707" stroke="#5a1a1a" stroke-width="8"/>')
        o.append(f'<circle cx="{x+210}" cy="1340" r="95" fill="#000" opacity="0.6"/>')
        o.append(f'<text x="{x+210}" y="1385" font-family="Anton" font-size="140" fill="#fff" text-anchor="middle">{lab}</text>')
    # A: acil fren
    x = 70
    o.append(f'<rect x="{x+90}" y="560" width="240" height="120" rx="10" fill="#ffd400"/>')
    o.append(f'<text x="{x+210}" y="606" font-family="Oswald" font-weight="700" font-size="36" fill="#000" text-anchor="middle">ACİL</text>')
    o.append(f'<text x="{x+210}" y="656" font-family="Oswald" font-weight="700" font-size="36" fill="#000" text-anchor="middle">FREN</text>')
    o.append(f'<rect x="{x+185}" y="720" width="50" height="330" rx="22" fill="#888"/>')
    o.append(f'<rect x="{x+110}" y="1010" width="200" height="90" rx="40" fill="#e01010"/>')
    o.append(f'<circle cx="{x+210}" cy="1060" r="160" fill="#ff2020" opacity="0.15" filter="url(#blur20)"/>')
    # B: telsiz
    x = 590
    o.append(f'<rect x="{x+130}" y="560" width="160" height="460" rx="40" fill="#1b1e22" stroke="#444" stroke-width="6"/>')
    o.append(f'<rect x="{x+150}" y="600" width="120" height="70" rx="8" fill="#1a1000"/>')
    o.append(f'<text x="{x+210}" y="648" font-family="DejaVu Sans Mono" font-weight="bold" font-size="30" fill="#ffa21a" text-anchor="middle">CH 7</text>')
    for r in range(5):
        for c in range(3):
            o.append(f'<circle cx="{x+170+c*40}" cy="{730+r*48}" r="10" fill="#000"/>')
    o.append(f'<path d="M{x+300},640 q40,60 0,120 M{x+330},610 q70,90 0,180" stroke="#ffa21a" stroke-width="7" fill="none" opacity="0.8"/>')
    o.append(f'<circle cx="{CX}" cy="180" r="160" fill="#ff1a1a" filter="url(#blur20)" opacity="0.7"/>')
    o.append(f'<rect x="{CX-70}" y="140" width="140" height="44" rx="10" fill="#ff3030"/>')
    o.append(yolcu(CX, 1890, 0.62, back=True))
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
    "kabin_kirmizi": lambda: kabin("kirmizi"),
    "kabin_mavi": lambda: kabin("mavi"),
    "kabin_yolcu": lambda: kabin("mavi", True),
    "kabin_yolcu_kirmizi": lambda: kabin("kirmizi", True),
    "ekran": ekran,
    "telsiz": lambda: telsiz(False),
    "telsiz_kirmizi": lambda: telsiz(True),
    "secim2": secim2,
}

def peron_yolcu():
    """3. bölüm: tren camından peron, perondaki tek yolcu (yüzü karanlık, bize dönük)."""
    p = PAL["mavi"]
    o = [defs(p), f'<rect width="{W}" height="{H}" fill="#06090d"/>']
    # peron duvarı + tabela
    o.append('<rect x="0" y="240" width="1080" height="1100" fill="#16212c"/>')
    for x in range(0, 1080, 90):
        o.append(f'<rect x="{x}" y="240" width="88" height="1100" fill="#1b2835" opacity="0.6"/>')
    o.append('<rect x="240" y="330" width="600" height="110" rx="8" fill="#0a1a4a"/>')
    o.append('<text x="540" y="405" font-family="DejaVu Sans Mono" font-weight="bold" font-size="50" fill="#fff" text-anchor="middle">00:47  ◀ 1 SAAT</text>')
    # tavan lambası koni
    o.append('<path d="M540,240 L300,1500 L780,1500 Z" fill="#cfe8ff" opacity="0.10"/>')
    o.append('<ellipse cx="540" cy="1480" rx="260" ry="40" fill="#cfe8ff" opacity="0.18" filter="url(#blur20)"/>')
    o.append('<rect x="0" y="1340" width="1080" height="580" fill="#0e151c"/>')
    o.append('<rect x="0" y="1340" width="1080" height="26" fill="#e8c200"/>')
    o.append(yolcu(540, 1500, 0.95, back=False))
    # vagon camı çerçevesi
    o.append('<path d="M0,0 H1080 V1920 H0 Z M120,200 V1700 H960 V200 Z" fill="#0b1118" fill-rule="evenodd"/>')
    o.append('<rect x="120" y="200" width="840" height="1500" rx="30" fill="none" stroke="#c8d3dc" stroke-width="12" opacity="0.6"/>')
    o.append('<line x1="200" y1="260" x2="520" y2="1640" stroke="#fff" stroke-width="14" opacity="0.05"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="{p["amb"]}"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')
    return "\n".join(o)

def secim3():
    """3. bölüm seçimi: A açık kapı / peron ışığı, B kilit."""
    p = PAL["kirmizi"]
    o = [defs(p), f'<rect width="{W}" height="{H}" fill="#120404"/>']
    for x, lab in ((70, "A"), (590, "B")):
        o.append(f'<rect x="{x}" y="420" width="420" height="1080" rx="18" fill="#1e0707" stroke="#5a1a1a" stroke-width="8"/>')
        o.append(f'<circle cx="{x+210}" cy="1340" r="95" fill="#000" opacity="0.6"/>')
        o.append(f'<text x="{x+210}" y="1385" font-family="Anton" font-size="140" fill="#fff" text-anchor="middle">{lab}</text>')
    x = 70  # A: aralık kapı, dışarıdan soğuk ışık + küçük yolcu silüeti
    o.append(f'<rect x="{x+60}" y="520" width="300" height="640" fill="#0a1220"/>')
    o.append(f'<rect x="{x+150}" y="520" width="120" height="640" fill="#cfe8ff" opacity="0.55" filter="url(#blur8)"/>')
    o.append(f'<rect x="{x+60}" y="520" width="90" height="640" fill="#2a0c0c"/><rect x="{x+270}" y="520" width="90" height="640" fill="#2a0c0c"/>')
    o.append(f'<g opacity="0.85">{yolcu(x+210, 1110, 0.42)}</g>')
    x = 590  # B: kilit
    o.append(f'<path d="M{x+130},760 v-80 a80,80 0 0 1 160,0 v80" stroke="#bbb" stroke-width="34" fill="none"/>')
    o.append(f'<rect x="{x+100}" y="760" width="220" height="200" rx="24" fill="#d8a020"/>')
    o.append(f'<circle cx="{x+210}" cy="840" r="22" fill="#3a2a00"/><rect x="{x+200}" y="845" width="20" height="60" fill="#3a2a00"/>')
    o.append(f'<circle cx="{x+210}" cy="860" r="170" fill="#ffb020" opacity="0.10" filter="url(#blur20)"/>')
    o.append(f'<circle cx="{CX}" cy="180" r="160" fill="#ff1a1a" filter="url(#blur20)" opacity="0.7"/>')
    o.append(f'<rect x="{CX-70}" y="140" width="140" height="44" rx="10" fill="#ff3030"/>')
    o.append(yolcu(CX, 1890, 0.62, back=True))
    o.append(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')
    return "\n".join(o)

SCENES["peron_yolcu"] = peron_yolcu
SCENES["secim3"] = secim3
