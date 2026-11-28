"""SEN SEÇ ikilem v2 — daha güçlü kanca + iki tema. Kullanım: python3 build_ikilem2.py config.json
config: {"out":"ikilem_2.mp4","tema":"gunluk"|"gerilim","ust":"KÜÇÜK ETİKET","rounds":[["A metni","A alt","B metni","B alt"],...5],"soru":"Hangisi en zordu?"}
Yenilikler: intro kartı yok (1. kare = 1. soru, kanca), A sonra B kayarak gelir, 4 sn geri sayım, her turda 'ding',
son kartta yorum sorusu, 24-25 sn (izlenme oranı için kısa), döngüye uygun bitiş."""
import os, sys, json, subprocess, base64
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
cfg = json.load(open(sys.argv[1])); W, H, FPS = 1080, 1920, 30
T = {"gunluk": dict(bg="#0b0b12", a="linear-gradient(160deg,#ff4d4d,#b3121b)", b="linear-gradient(160deg,#3b8cff,#1240a8)", acc="#ffd400", veya="#fff", vtxt="#111"),
     "gerilim": dict(bg="radial-gradient(circle at 50% 45%,#1a0d10,#000 75%)", a="linear-gradient(160deg,#8e0c14,#2a0306)", b="linear-gradient(160deg,#0f4c5c,#031418)", acc="#ff2a2a", veya="#111", vtxt="#ff3b3b")}[cfg.get("tema","gunluk")]
def _b(n): return "data:font/ttf;base64," + base64.b64encode(open(f"fonts/{n}", "rb").read()).decode()
CSS = f"""@font-face{{font-family:Anton;src:url({_b('Anton.ttf')});}}@font-face{{font-family:Oswald;font-weight:200 700;src:url({_b('Oswald.ttf')});}}
body{{margin:0;width:{W}px;height:{H}px;overflow:hidden;background:{T['bg']};color:#fff}}
.top{{position:absolute;top:60px;width:100%;text-align:center;font:400 64px Anton;letter-spacing:2px;text-shadow:0 5px 0 #000}}
.tag{{position:absolute;top:150px;left:50%;transform:translateX(-50%);background:{T['acc']};color:#000;font:700 40px Oswald;letter-spacing:3px;padding:8px 30px;border-radius:50px;white-space:nowrap}}
.panel{{position:absolute;left:50px;right:50px;height:620px;border-radius:40px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,.6);border:4px solid rgba(255,255,255,.15)}}
.a{{top:250px;background:{T['a']}}} .b{{top:990px;background:{T['b']}}}
.lab{{position:absolute;top:26px;left:30px;width:110px;height:110px;border-radius:50%;background:rgba(0,0,0,.4);font:400 84px/110px Anton;text-align:center}}
.opt{{font:400 112px/1.02 Anton;padding:0 50px;text-shadow:0 6px 0 rgba(0,0,0,.4)}} .sub{{margin-top:20px;font:500 48px Oswald}}
.veya{{position:absolute;top:870px;left:50%;transform:translateX(-50%);width:220px;height:220px;border-radius:50%;background:{T['veya']};color:{T['vtxt']};font:400 70px/220px Anton;text-align:center;border:10px solid #000;z-index:3}}
.cnt{{position:absolute;top:1650px;left:50%;transform:translateX(-50%);width:150px;height:150px;border-radius:50%;background:{T['acc']}}}
.ghost{{opacity:.0}}
.big{{position:absolute;top:470px;left:60px;right:60px;text-align:center;font:400 150px/1.02 Anton;text-shadow:0 8px 0 #000}}
.mid{{position:absolute;top:1000px;left:70px;right:70px;text-align:center;font:500 60px/1.3 Oswald}}"""
R = cfg["rounds"]; N = len(R)
def page(i, show_b):
    a, sa, b, sb = R[i]
    top = "5 ZOR SEÇİM · 4 SANİYEN VAR" if i == 0 else f"{i+1} / {N}"
    bcls = "panel b" if show_b else "panel b ghost"
    return (f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body><div class='top'>{top}</div>"
            + (f"<div class='tag'>{cfg.get('ust','SEN SEÇ TV')}</div>" if i == 0 else "")
            + f"<div class='panel a'><div class='lab'>A</div><div class='opt'>{a}</div><div class='sub'>{sa}</div></div>"
            + (f"<div class='veya'>VEYA</div>" if show_b else "")
            + f"<div class='{bcls}'><div class='lab'>B</div><div class='opt'>{b}</div><div class='sub'>{sb}</div></div>"
            + ("<div class='cnt'></div>" if show_b else "") + "</body></html>")
outro = (f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body><div class='big'>SEN NE<br>SEÇTİN?</div>"
         f"<div class='mid'>Yorumlara yaz:<br><span style='font:400 110px Anton;color:{T['acc']};letter-spacing:8px'>A B B A B</span><br>{cfg.get('soru','Hangisi en zordu?')} 👇</div></body></html>")
os.makedirs("tmp2", exist_ok=True)
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={"width": W, "height": H})
    def shot(h, path): pg.set_content(h); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(150); pg.screenshot(path=path)
    for i in range(N): shot(page(i, False), f"tmp2/r{i}a.png"); shot(page(i, True), f"tmp2/r{i}b.png")
    shot(outro, "tmp2/out.png"); br.close()
PRE, RD, OUT = 0.5, 4.0, 2.6   # A tek başına 0.5 sn, sonra B gelir + 4 sn sayaç
clips = []
def clip(img, d, extra="", name=None):
    fr = round(d * FPS); out = f"tmp2/{name}.mp4"
    vf = f"scale=2160:3840,zoompan=z='1+0.03*on/{fr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={fr}:s=1080x1920:fps={FPS}{extra},format=yuv420p"
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-loop","1","-i",img,"-vf",vf,"-frames:v",str(fr),"-r",str(FPS),"-c:v","libx264","-preset","veryfast","-crf","18",out],check=True)
    clips.append(out)
for i in range(N):
    clip(f"tmp2/r{i}a.png", PRE, name=f"c{i}a")
    clip(f"tmp2/r{i}b.png", RD, extra=(f",drawtext=fontfile=fonts/Anton.ttf:text='%{{eif\\:ceil({RD}-t)\\:d}}':fontsize=96:fontcolor=black:x=(w-tw)/2:y=1725-th/2"), name=f"c{i}b")
clip("tmp2/out.png", OUT, name="cout")
open("tmp2/list.txt","w").write("".join(f"file '{os.path.basename(c)}'\n" for c in clips))
subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i","tmp2/list.txt","-c","copy","tmp2/raw.mp4"],check=True)
TOTAL = N*(PRE+RD)+OUT; starts=[i*(PRE+RD) for i in range(N)]
whoosh = "+".join(f"if(between(t,{s+PRE},{s+PRE+0.25}),0.25*sin(2*PI*(300+2400*(t-{s+PRE}))*t)*exp(-10*(t-{s+PRE})),0)" for s in starts)
ding = "+".join(f"if(between(t,{s},{s+0.6}),(0.32*sin(2*PI*880*t)+0.18*sin(2*PI*1320*t))*exp(-7*(t-{s})),0)" for s in starts+[TOTAL-OUT])
tick = "+".join(f"if(between(t,{s+PRE},{s+PRE+RD}),0.26*sin(2*PI*1900*t)*exp(-60*mod(t-{s+PRE},1))*lt(mod(t-{s+PRE},1),0.08),0)" for s in starts)
if cfg.get("tema") == "gerilim":
    base = "0.30*sin(2*PI*50*t)*(exp(-14*mod(t,0.85))+0.8*exp(-14*mod(t-0.22,0.85))*gt(mod(t,0.85),0.22))+0.06*sin(2*PI*110*t)*(0.6+0.4*sin(2*PI*0.15*t))"
else:
    base = "(0.05*sin(2*PI*261.6*t)+0.04*sin(2*PI*329.6*t)+0.04*sin(2*PI*392*t))*(0.7+0.3*sin(2*PI*0.2*t))+0.22*sin(2*PI*55*t)*exp(-9*mod(t,0.5))"
subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","lavfi","-i",f"aevalsrc='{base}+{whoosh}+{ding}+{tick}':s=44100:d={TOTAL}",
                "-af",f"afade=t=out:st={TOTAL-0.8}:d=0.8,volume=0.9","-ac","2","-c:a","aac","-b:a","160k","tmp2/m.m4a"],check=True)
subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i","tmp2/raw.mp4","-i","tmp2/m.m4a","-c:v","libx264","-preset","veryfast","-crf","23",
                "-maxrate","6M","-bufsize","12M","-pix_fmt","yuv420p","-c:a","copy","-shortest","-movflags","+faststart",cfg["out"]],check=True)
subprocess.run(["rm","-rf","tmp2"]); print("ok", cfg["out"], TOTAL)
