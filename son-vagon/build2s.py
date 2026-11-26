"""Son Vagon #2 — sessiz POV (ekran yazısı + sentetik ses). Çalıştır: python3 build2.py"""
import json, subprocess, os
D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
os.environ["EP"] = "2"
FPS = 30
# (ad, sahne, süre, büyük yazı, alt yazı, rozet, kırmızı, top, zoom)
S = [
 ("e01","kabin_kirmizi",2.6,"KABİNDE<br>KİMSE YOK.","Makinist kabininin kapısını açtın.","SON DURAK",True,1150,"in"),
 ("e02","kapilar",2.8,"KİLİTLİ<br>DEĞİLMİŞ.","Kapı sadece aralıkmış. Sanki seni bekliyormuş.","SON DURAK",True,360,"left"),
 ("e03","kabin_mavi",3.0,"KOLTUK<br>HÂLÂ SICAK.","Biri birkaç saniye önce buradaydı.","SON DURAK",True,1150,"in"),
 ("e04","ekran",3.4,"","Ekranda tek bir satır yanıp sönüyor…","SÜRÜCÜ: YOK",True,None,"in"),
 ("e05","kabin_yolcu",3.2,"TREN<br>GERİ GİDİYOR.","Kapılar kapanıyor. Tren tünele geri gidiyor.","3 DURAK KALDI",False,1150,"out"),
 ("e06","vagon_mavi",3.0,"VURUŞLAR<br>KESİLDİ.","Arka vagon artık sessiz. Fazla sessiz.","3 DURAK KALDI",False,None,"in"),
 ("e07","telsiz",3.2,"TELSİZ<br>CIZIRDIYOR.","“Arka kapıyı… sakın… açma…”","2 KALDI",False,None,"in"),
 ("e08","telsiz_kirmizi",3.0,"SESİ<br>TANIDIK.","Çünkü bu ses… senin sesin.","2 KALDI",True,None,"in"),
 ("e09","kabin_yolcu_kirmizi",3.0,"TAK. TAK. TAK.","Vuruşlar şimdi kabin kapısında.","SON DURAK",True,1200,"in"),
 ("e10","secim2",2.4,"İKİ SEÇENEK.","","SON DURAK",True,360,"out"),
 ("e11","secim2",3.6,"A: ACİL<br>FREN","Treni durdur, karanlık tünelde in.","SON DURAK",True,360,"left"),
 ("e12","secim2",3.6,"B: TELSİZE<br>CEVAP VER","Kendi sesinle konuş.","SON DURAK",True,360,"right"),
 ("e13","secim2",5.2,"A MI, B Mİ?<br><span style='font-size:72px'>YORUMLARA YAZ</span>","En çok oy alan seçim yarın 3. bölümde.","SEN SEÇ",True,360,"out"),
]
NARR = {
 "e01":"Makinist kabininin kapısını açtın. Kabinde kimse yok.",
 "e02":"Kapı kilitli değilmiş… sadece aralıkmış. Sanki seni bekliyormuş.",
 "e03":"Koltuk hâlâ sıcak. Biri birkaç saniye önce buradaydı.",
 "e04":"Ekranda tek bir satır yanıp sönüyor: Sürücü yok.",
 "e05":"Kapılar kapanıyor. Tren… tünele geri gidiyor.",
 "e06":"Arka vagondaki vuruşlar kesildi. Fazla sessiz.",
 "e07":"Telsiz cızırdıyor: Arka kapıyı… sakın… açma.",
 "e08":"Sesi tanıdık geliyor. Çünkü bu ses… senin sesin.",
 "e09":"Tak. Tak. Tak. Vuruşlar artık kabin kapısında.",
 "e10":"İki seçeneğin var.",
 "e11":"A: Acil freni çek. Treni durdur, karanlık tünelde in.",
 "e12":"B: Telsize cevap ver. Kendi sesinle konuş.",
 "e13":"Sen hangisini seçerdin? Yorumlara A ya da B yaz. En çok oy alan seçim, yarın üçüncü bölümde.",
}
VOICE = 50.0  # ElevenLabs Celil, saniye
def _w(t): return len(t) + 9*t.count("…") + 4*sum(t.count(c) for c in ".?:")
_tot = sum(_w(v) for v in NARR.values())
S = [(n, sc, round(_w(NARR[n]) / _tot * VOICE + (0.8 if n == "e13" else 0), 2), *rest) for n, sc, d, *rest in S]
TOTAL = round(sum(x[2] for x in S), 2)
jobs = [dict(name=n, scene=sc, big=b, sub=sb, badge=bd, red=r, top=tp) for n, sc, d, b, sb, bd, r, tp, z in S]
json.dump(jobs, open("shots2.json", "w"))
subprocess.run(["python3", "render.py", "shots2.json", "shots2"], check=True)

clips = []
for n, sc, dur, b, sb, bd, r, tp, z in S:
    fr = round(dur * FPS)
    if z == "in": zx, zy, zz = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)", f"1+0.08*on/{fr}"
    elif z == "out": zx, zy, zz = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)", f"1.08-0.08*on/{fr}"
    elif z == "left": zx, zy, zz = "iw*0.30-(iw/zoom/2)", "ih*0.5-(ih/zoom/2)", f"1.0+0.06*on/{fr}"
    else: zx, zy, zz = "iw*0.70-(iw/zoom/2)", "ih*0.5-(ih/zoom/2)", f"1.0+0.06*on/{fr}"
    vf = f"scale=2160:3840,zoompan=z='{zz}':x='max(0,min(iw-iw/zoom,{zx}))':y='max(0,min(ih-ih/zoom,{zy}))':d={fr}:s=1080x1920:fps={FPS}"
    if r: vf += ",eq=brightness='0.06*sin(2*PI*t*1.6)'"
    if n == "e01": vf += ",fade=t=in:st=0:d=0.15:color=white"
    vf += ",format=yuv420p"
    out = f"clip2_{n}.mp4"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-loop", "1", "-i", f"shots2/{n}.png", "-vf", vf,
                    "-frames:v", str(fr), "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", out], check=True)
    clips.append(out)
open("list2.txt", "w").write("".join(f"file '{c}'\n" for c in clips))
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", "list2.txt", "-c", "copy", "video2_raw.mp4"], check=True)

# zaman çizelgesi
t = 0; T = {}
for x in S: T[x[0]] = (t, t + x[2]); t += x[2]
tel0, tel1 = T["e07"][0], T["e08"][1]
k0, k1 = T["e09"]
al0 = T["e09"][0]
# sentetik ses: drone + kabin açılış vurgusu + telsiz paraziti + vuruşlar + alarm (telifsiz)
music = (f"aevalsrc='(0.07*sin(2*PI*220*t)+0.05*sin(2*PI*261.6*t)+0.05*sin(2*PI*329.6*t)+0.03*sin(2*PI*440*t))*(0.6+0.4*sin(2*PI*0.25*t))+0.12*sin(2*PI*110*t)"
         f"+if(lt(t,0.9),0.35*sin(2*PI*(90-60*t)*t)*exp(-3*t),0)"
         f"+if(between(t,{k0},{k1}),0.6*sin(2*PI*180*t)*exp(-18*mod(t-{k0},0.88))*lt(mod(t-{k0},0.88),0.5),0)"
         f"+if(between(t,{al0},{TOTAL-1}),0.08*sin(2*PI*880*t)*lt(mod(t,0.8),0.18),0)':s=44100:d={TOTAL}")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i", music,
                "-f", "lavfi", "-i", f"anoisesrc=c=brown:a=0.35:d={TOTAL}",
                "-f", "lavfi", "-i", f"anoisesrc=c=white:a=0.25:d={TOTAL}",
                "-filter_complex",
                f"[1]lowpass=f=180,volume=0.6[n];"
                f"[2]bandpass=f=1800:width_type=h:w=1400,volume='if(between(t,{tel0},{tel1}),0.5*(0.6+0.4*sin(2*PI*7*t)),0)':eval=frame[st];"
                f"[0][n][st]amix=inputs=3:normalize=0,afade=t=in:d=0.2,afade=t=out:st={TOTAL-1.5}:d=1.5,volume=0.8[a]",
                "-map", "[a]", "-ac", "2", "-c:a", "aac", "-b:a", "160k", "music2.m4a"], check=True)
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", "video2_raw.mp4", "-i", "music2.m4a",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-maxrate", "6M", "-bufsize", "12M", "-pix_fmt", "yuv420p",
                "-c:a", "copy", "-shortest", "-movflags", "+faststart", "son_vagon_2_fon.mp4"], check=True)
print("ok", TOTAL)
