"""SEN SEÇ | Hangisini Seçerdin? #1 — ikilem formatı (ekran yazısı + sentetik müzik, kredisiz). Çalıştır: python3 build_ikilem1.py"""
import os, subprocess, base64
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
W, H, FPS = 1080, 1920, 30
def _b(n): return "data:font/ttf;base64," + base64.b64encode(open(f"fonts/{n}", "rb").read()).decode()
CSS = f"""@font-face{{font-family:Anton;src:url({_b('Anton.ttf')});}}
@font-face{{font-family:Oswald;font-weight:200 700;src:url({_b('Oswald.ttf')});}}
body{{margin:0;width:{W}px;height:{H}px;overflow:hidden;background:#0b0b12;font-family:Oswald;color:#fff}}
.brand{{position:absolute;top:70px;width:100%;text-align:center;font:500 32px Oswald;letter-spacing:6px;color:rgba(255,255,255,.8)}}
.tag{{position:absolute;top:130px;left:50%;transform:translateX(-50%);background:#ffd400;color:#000;font:700 46px Oswald;letter-spacing:3px;padding:10px 34px;border-radius:50px;white-space:nowrap}}
.panel{{position:absolute;left:50px;right:50px;height:640px;border-radius:40px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,.5)}}
.a{{top:250px;background:linear-gradient(160deg,#ff4d4d,#b3121b)}}
.b{{top:1000px;background:linear-gradient(160deg,#3b8cff,#1240a8)}}
.lab{{position:absolute;top:28px;left:34px;width:110px;height:110px;border-radius:50%;background:rgba(0,0,0,.35);font:400 84px/110px Anton;text-align:center}}
.opt{{font:400 118px/1.02 Anton;padding:0 60px;text-shadow:0 6px 0 rgba(0,0,0,.35)}}
.sub{{margin-top:22px;font:500 50px Oswald;opacity:.95}}
.veya{{position:absolute;top:880px;left:50%;transform:translateX(-50%);width:230px;height:230px;border-radius:50%;background:#fff;color:#111;font:400 72px/230px Anton;text-align:center;border:10px solid #0b0b12;z-index:3}}
.cnt{{position:absolute;top:1680px;left:50%;transform:translateX(-50%);width:150px;height:150px;border-radius:50%;background:#ffd400}}
.foot{{position:absolute;bottom:60px;width:100%;text-align:center;font:500 40px Oswald;color:rgba(255,255,255,.75)}}
.big{{position:absolute;top:520px;left:60px;right:60px;text-align:center;font:400 170px/1.02 Anton;text-shadow:0 8px 0 #000}}
.mid{{position:absolute;top:1180px;left:80px;right:80px;text-align:center;font:500 62px/1.3 Oswald}}
"""
ROUNDS = [
 ("KARA CUMA ÖZEL", "%90 İNDİRİM", "ama sadece 60 saniyen var", "%30 İNDİRİM", "bütün gün senin"),
 ("2 / 5", "HER GÜN<br>1.000 TL", "ömür boyu", "BUGÜN<br>1 MİLYON TL", "tek seferlik"),
 ("3 / 5", "1 AY<br>TELEFONSUZ", "hiç ekran yok", "1 AY<br>TATLISIZ", "tek lokma bile yok"),
 ("4 / 5", "GEÇMİŞE<br>DÖN", "1 kez, 10 dakikalığına", "GELECEĞİ<br>GÖR", "1 kez, 10 saniyeliğine"),
 ("5 / 5", "DÜŞÜNCELERİ<br>DUY", "herkesin, her an", "GÖRÜNMEZ<br>OL", "istediğin zaman"),
]
INTRO, RD, OUTRO = 1.8, 4.6, 3.6
def html(body): return f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body><div class='brand'>SEN SEÇ TV · HANGİSİNİ SEÇERDİN?</div>{body}</body></html>"
pages = {"intro": html("<div class='big'>5 ZOR<br>SEÇİM</div><div class='mid'>Süre çok kısa.<br>Düşünmeden seç!</div><div class='foot'>Seçimlerini yorumlara yaz 👇</div>")}
for i, (tag, a, sa, b, sb) in enumerate(ROUNDS):
    pages[f"r{i+1}"] = html(f"<div class='tag'>{tag}</div><div class='panel a'><div class='lab'>A</div><div class='opt'>{a}</div><div class='sub'>{sa}</div></div>"
                            f"<div class='veya'>VEYA</div><div class='panel b'><div class='lab'>B</div><div class='opt'>{b}</div><div class='sub'>{sb}</div></div><div class='cnt'></div>")
pages["outro"] = html("<div class='big' style='top:420px;font-size:150px'>SEN NE<br>SEÇTİN?</div><div class='mid' style='top:900px'>Yorumlara yaz:<br><span style='font:400 110px Anton;color:#ffd400;letter-spacing:8px'>A B B A B</span><br>Senin gibi seçen var mı, bak 👀</div><div class='foot'>Takip et: her gün yeni seçim</div>")
os.makedirs("shots1", exist_ok=True)
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={"width": W, "height": H})
    for k, h in pages.items():
        pg.set_content(h); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(200)
        pg.screenshot(path=f"shots1/{k}.png")
    br.close()
seq = [("intro", INTRO)] + [(f"r{i+1}", RD) for i in range(5)] + [("outro", OUTRO)]
clips = []
for k, d in seq:
    fr = round(d * FPS)
    vf = f"scale=2160:3840,zoompan=z='1+0.035*on/{fr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={fr}:s=1080x1920:fps={FPS}"
    if k.startswith("r"):
        vf += (f",drawtext=fontfile=fonts/Anton.ttf:text='%{{eif\\:ceil({d-0.6}-t)\\:d}}':enable='lt(t,{d-0.6})':fontsize=96:fontcolor=black:x=(w-tw)/2:y=1755-th/2"
               f",drawtext=fontfile=fonts/Anton.ttf:text='!':enable='gte(t,{d-0.6})':fontsize=96:fontcolor=black:x=(w-tw)/2:y=1755-th/2")
    vf += ",format=yuv420p"
    out = f"c_{k}.mp4"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-loop", "1", "-i", f"shots1/{k}.png", "-vf", vf,
                    "-frames:v", str(fr), "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", out], check=True)
    clips.append(out)
open("list1.txt", "w").write("".join(f"file '{c}'\n" for c in clips))
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", "list1.txt", "-c", "copy", "raw1.mp4"], check=True)
TOTAL = INTRO + 5 * RD + OUTRO
starts = [INTRO + i * RD for i in range(5)]
ding = "+".join(f"if(between(t,{s},{s+0.6}),(0.35*sin(2*PI*880*t)+0.2*sin(2*PI*1320*t))*exp(-7*(t-{s})),0)" for s in starts + [TOTAL - OUTRO])
tick = "+".join(f"if(between(t,{s},{s+RD-0.6}),0.28*sin(2*PI*1900*t)*exp(-60*mod(t-{s},1))*lt(mod(t-{s},1),0.08),0)" for s in starts)
beat = f"0.22*sin(2*PI*55*t)*exp(-9*mod(t,0.5))"
pad = "(0.05*sin(2*PI*261.6*t)+0.04*sin(2*PI*329.6*t)+0.04*sin(2*PI*392*t))*(0.7+0.3*sin(2*PI*0.2*t))"
expr = f"{pad}+{beat}+{ding}+{tick}"
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i", f"aevalsrc='{expr}':s=44100:d={TOTAL}",
                "-af", f"afade=t=in:d=0.1,afade=t=out:st={TOTAL-1.2}:d=1.2,volume=0.9", "-ac", "2", "-c:a", "aac", "-b:a", "160k", "music1.m4a"], check=True)
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", "raw1.mp4", "-i", "music1.m4a", "-c:v", "libx264", "-preset", "veryfast",
                "-crf", "23", "-maxrate", "6M", "-bufsize", "12M", "-pix_fmt", "yuv420p", "-c:a", "copy", "-shortest", "-movflags", "+faststart", "ikilem_1.mp4"], check=True)
print("ok", TOTAL)
