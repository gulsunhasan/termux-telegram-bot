"""Atatürk #2 — Çanakkale 1915. Ses: ElevenLabs (56.08 sn), vidiq_compose ile eklenir."""
import os, sys, json, base64, subprocess
D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D); sys.path.insert(0, D)
from scenes_a import SCENES, W, H
from playwright.sync_api import sync_playwright
def _b(n): return "data:font/ttf;base64," + base64.b64encode(open(f"../son-vagon/fonts/{n}", "rb").read()).decode()
FONTS = f"@font-face{{font-family:Anton;src:url({_b('Anton.ttf')});}}@font-face{{font-family:Oswald;font-weight:200 700;src:url({_b('Oswald.ttf')});}}"
NARR = [
 ("a01","dawn","25 NİSAN<br>1915","Sabah saat 05.30","25 Nisan 1915. Sabah saat beş buçuk."),
 ("a02","map","","Gelibolu, Bigalı köyü","Gelibolu, Bigalı köyü."),
 ("a03","telegram","","34 yaşındaki Yarbay Mustafa Kemal'e acil rapor","Otuz dört yaşındaki Yarbay Mustafa Kemal'e bir rapor geliyor: Düşman Arıburnu'na asker çıkardı."),
 ("a04","map_arrow","19. TÜMEN","Emir beklemiyor. Tepeye koşuyor.","O, 19. Tümen'in komutanı. Emir beklemiyor. Tepeye koşuyor."),
 ("a05","hill","“CEPHANEMİZ<br>BİTTİ!”","Geri çekilen askerler","Karşıdan çekilen askerlerimiz: Cephanemiz bitti diyorlar."),
 ("a06","hill_soldiers","“SÜNGÜ TAKIN,<br>YERE YATIN!”","“Kaçamazsınız.”","Kaçamazsınız diyor. Süngü takın, yere yatın."),
 ("a07","clock10","SAAT 10.00","57. Alay'a tarihî emir","Saat on. 57. Alay'a o tarihî emri veriyor:"),
 ("a08","crimson","“SİZE BEN<br>TAARRUZ<br>EMRETMİYORUM,<br>ÖLMEYİ<br>EMREDİYORUM.”","","Size ben taarruz emretmiyorum, ölmeyi emrediyorum."),
 ("a09","crimson","","“Biz ölünceye kadar geçecek zaman zarfında, başka kuvvetler ve komutanlar yerimizi alabilir.”","Biz ölünceye kadar geçecek zaman zarfında, başka kuvvetler ve komutanlar yerimizi alabilir."),
 ("a10","hill_soldiers","57. ALAY","O gün destan yazdı.","57. Alay o gün destan yazıyor."),
 ("a11","map_conk","10 AĞUSTOS<br>1915","Conkbayırı · Göğsüne şarapnel isabet ediyor","Aylar sonra, 10 Ağustos 1915, Conkbayırı. Bir şarapnel parçası göğsüne isabet ediyor."),
 ("a12","watch","SAAT ONU<br>KURTARDI","Cebindeki saat parçalandı.","Ama cebindeki saat parçalanıyor… ve onu kurtarıyor."),
 ("a13","question","SIRADAKİ<br>BÖLÜM?","Yorumlara yaz 👇","Sıradaki bölüm ne olsun? Samsun mu, Sakarya mı? Yorumlara yaz."),
]
VOICE = 56.08
def _w(t): return len(t) + 9*t.count("…") + 4*sum(t.count(c) for c in ".?:")
tot = sum(_w(x[4]) for x in NARR)
S = [(n, sc, big, sub, round(_w(nar)/tot*VOICE + (0.8 if n == "a13" else 0), 2)) for n, sc, big, sub, nar in NARR]
TOTAL = round(sum(x[4] for x in S), 2)

def page(sc, big, sub, red):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">{SCENES[sc]()}</svg>'
    top = 300 if sc in ("map", "map_arrow", "map_conk", "question", "clock10", "watch", "telegram") else 640
    fs = 104 if big.count("<br>") >= 3 else 132
    ov = '<div class="brand">SEN SEÇ TV · ATATÜRK #2 · ÇANAKKALE</div>'
    if big: ov += f'<div class="big" style="top:{top}px;font-size:{fs}px">{big}</div>'
    if sub: ov += f'<div class="sub">{sub}</div>'
    return f"""<html><head><meta charset="utf-8"><style>{FONTS}
body{{margin:0;width:{W}px;height:{H}px;overflow:hidden;background:#000}}.w{{position:relative;width:{W}px;height:{H}px}}svg{{position:absolute;inset:0}}
.brand{{position:absolute;top:110px;width:100%;text-align:center;color:#e9d9b0;font:500 32px Oswald;letter-spacing:5px}}
.big{{position:absolute;left:50px;right:50px;text-align:center;color:#fff6e0;font-family:Anton;line-height:1.05;letter-spacing:2px;
 -webkit-text-stroke:3px #000;paint-order:stroke fill;text-shadow:0 0 30px rgba(0,0,0,.9),0 6px 0 #000}}
.sub{{position:absolute;bottom:300px;left:70px;right:70px;text-align:center;color:#fff;font:500 52px/1.25 Oswald;background:rgba(0,0,0,.62);padding:18px 26px;border-radius:18px}}
</style></head><body><div class="w">{svg}{ov}</div></body></html>"""

os.makedirs("shots_a2", exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": H})
    for n, sc, big, sub, d in S:
        pg.set_content(page(sc, big, sub, False))
        pg.evaluate("Promise.all([document.fonts.load('400 40px Anton'),document.fonts.load('700 40px Oswald')]).then(()=>document.fonts.ready)")
        pg.wait_for_timeout(120); pg.screenshot(path=f"shots_a2/{n}.png")
    b.close()
FPS = 30; clips = []
for i, (n, sc, big, sub, d) in enumerate(S):
    fr = round(d * FPS)
    zz = f"1+0.07*on/{fr}" if i % 2 == 0 else f"1.07-0.07*on/{fr}"
    vf = f"scale=2160:3840,zoompan=z='{zz}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={fr}:s=1080x1920:fps={FPS},fade=t=in:st=0:d=0.25,format=yuv420p"
    out = f"c_{n}.mp4"
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-loop","1","-i",f"shots_a2/{n}.png","-vf",vf,"-frames:v",str(fr),"-r",str(FPS),"-c:v","libx264","-preset","veryfast","-crf","18",out], check=True)
    clips.append(out)
open("list_a2.txt","w").write("".join(f"file '{c}'\n" for c in clips))
subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i","list_a2.txt","-c","copy","raw_a2.mp4"], check=True)
# telifsiz fon: yavaş, ağırbaşlı minör pad (orta frekans, telefonda duyulur), düşük seviye
music = (f"aevalsrc='(0.06*sin(2*PI*196*t)+0.05*sin(2*PI*233.1*t)+0.05*sin(2*PI*293.7*t)+0.025*sin(2*PI*392*t))*(0.65+0.35*sin(2*PI*0.2*t))"
         f"+0.10*sin(2*PI*98*t)*(0.6+0.4*sin(2*PI*0.5*t))':s=44100:d={TOTAL}")
subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i","raw_a2.mp4","-f","lavfi","-i",music,
    "-filter_complex",f"[1]afade=t=in:d=1,afade=t=out:st={TOTAL-2}:d=2,volume=0.8[a]","-map","0:v","-map","[a]",
    "-c:v","libx264","-preset","veryfast","-crf","23","-maxrate","6M","-bufsize","12M","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart","ataturk_2_fon.mp4"], check=True)
for c in clips: os.remove(c)
os.remove("raw_a2.mp4"); os.remove("list_a2.txt")
print("ok", TOTAL)
