import sys, json, os
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(__file__))
from scenes import SCENES, W, H
EP = os.environ.get('EP', '1')

D = os.path.dirname(os.path.abspath(__file__))
F = f"file://{D}/node_modules/@fontsource"
import base64
def _b(n): return "data:font/ttf;base64,"+base64.b64encode(open(f"{D}/fonts/{n}","rb").read()).decode()
FONTS = f"""
@font-face{{font-family:Anton;src:url({_b("Anton.ttf")});}}
@font-face{{font-family:Oswald;font-weight:200 700;src:url({_b("Oswald.ttf")});}}
"""

def page_html(scene, big="", badge="", sub="", badge_red=False, top=None):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{SCENES[scene]()}</svg>'
    ov = ""
    if badge:
        bg = "#d4121a" if badge_red else "rgba(0,0,0,.72)"
        ov += f'<div class="badge" style="background:{bg}"><span class="dot"></span>{badge}</div>'
    ov += f'<div class="brand">SEN SEÇ TV · SON VAGON #{EP}</div>'
    if big:
        ov += f'<div class="big" style="top:{top}px">{big}</div>' if top else f'<div class="big">{big}</div>'
    if sub:
        ov += f'<div class="sub">{sub}</div>'
    return f"""<html><head><meta charset="utf-8"><style>{FONTS}
body{{margin:0;width:{W}px;height:{H}px;overflow:hidden;background:#000}}
.wrap{{position:relative;width:{W}px;height:{H}px}}
svg{{position:absolute;inset:0}}
.badge{{position:absolute;top:150px;left:50%;transform:translateX(-50%);color:#fff;font:700 54px Oswald;letter-spacing:3px;
 padding:14px 38px;border-radius:60px;border:3px solid rgba(255,255,255,.85);white-space:nowrap;display:flex;align-items:center;gap:18px}}
.dot{{width:22px;height:22px;border-radius:50%;background:#ff3b3b;box-shadow:0 0 18px #ff3b3b}}
.brand{{position:absolute;top:80px;width:100%;text-align:center;color:rgba(255,255,255,.75);font:500 30px Oswald;letter-spacing:6px}}
.big{{position:absolute;top:760px;left:60px;right:60px;text-align:center;color:#fff;font:400 132px/1.05 Anton;letter-spacing:2px;
 text-shadow:0 0 30px rgba(0,0,0,.9),0 6px 0 #000,0 0 60px rgba(0,0,0,.8);-webkit-text-stroke:3px #000;paint-order:stroke fill}}
.sub{{position:absolute;bottom:300px;left:70px;right:70px;text-align:center;color:#fff;font:500 50px/1.25 Oswald;
 background:rgba(0,0,0,.62);padding:18px 26px;border-radius:18px}}
</style></head><body><div class="wrap">{svg}{ov}</div></body></html>"""

def render(jobs, outdir):
    os.makedirs(outdir, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        for j in jobs:
            pg.set_content(page_html(j["scene"], j.get("big", ""), j.get("badge", ""), j.get("sub", ""), j.get("red", False), j.get("top")))
            pg.evaluate("Promise.all([document.fonts.load('400 40px Anton'),document.fonts.load('700 40px Oswald'),document.fonts.load('500 40px Oswald')]).then(()=>document.fonts.ready)")
            pg.wait_for_timeout(150)
            pg.screenshot(path=os.path.join(outdir, j["name"] + ".png"))
        b.close()

if __name__ == "__main__":
    jobs = json.load(open(sys.argv[1]))
    render(jobs, sys.argv[2])
