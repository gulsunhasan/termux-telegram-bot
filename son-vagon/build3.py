"""Son Vagon #3 — sessiz POV (ekran yazısı + sentetik ses). Çalıştır: python3 build2.py"""
import json, subprocess, os
D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
os.environ["EP"] = "3"
FPS = 30
# (ad, sahne, süre, büyük yazı, alt yazı, rozet, kırmızı, top, zoom)
S = [
 ("e01","telsiz_kirmizi",2.9,"ALO?","Telsizin düğmesine bastın.","1 DURAK KALDI",True,None,"in"),
 ("e02","telsiz",3.0,"AYNI<br>ANDA.","Ses aynı anda cevap verdi: “Alo?”","1 DURAK KALDI",False,None,"in"),
 ("e03","telsiz_kirmizi",2.5,"SENİN<br>SESİN.","Kelimesi kelimesine…","1 DURAK KALDI",True,None,"in"),
 ("e04","ekran",2.1,"ZAMANDA<br>GERİ.","“Bu tren zamanda geri gidiyor.”","SÜRÜCÜ: YOK",True,300,"in"),
 ("e05","vagon_mavi",2.0,"1 SAAT<br>ÖNCE.","“Bir saat önceki son metroya.”","1 DURAK KALDI",False,None,"in"),
 ("e06","kabin_yolcu",1.5,"YAVAŞLIYOR.","Tren yavaşlıyor.","SON DURAK",False,1150,"out"),
 ("e07","peron_yolcu",2.7,"","Perondaki tek yolcu… turuncu kapüşonlu.","SON DURAK",False,None,"in"),
 ("e08","peron_yolcu",1.5,"O SENSİN.","","SON DURAK",True,1180,"in"),
 ("e09","secim3",2.8,"A: TRENDEN<br>İN","Kendinle konuş.","SEN SEÇ",True,360,"left"),
 ("e10","secim3",2.7,"B: KAPIYI<br>KİLİTLE","Ona görünme.","SEN SEÇ",True,360,"right"),
 ("e11","secim3",4.3,"A MI, B Mİ?<br><span style='font-size:72px'>YORUMLARA YAZ</span>","En çok oy alan seçim 4. bölümde.","SEN SEÇ",True,360,"out"),
]
TOTAL = round(sum(x[2] for x in S), 2)
jobs = [dict(name=n, scene=sc, big=b, sub=sb, badge=bd, red=r, top=tp) for n, sc, d, b, sb, bd, r, tp, z in S]
json.dump(jobs, open("shots3.json", "w"))
subprocess.run(["python3", "render.py", "shots3.json", "shots3"], check=True)

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
    out = f"clip3_{n}.mp4"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-loop", "1", "-i", f"shots3/{n}.png", "-vf", vf,
                    "-frames:v", str(fr), "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", out], check=True)
    clips.append(out)
open("list3.txt", "w").write("".join(f"file '{c}'\n" for c in clips))
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", "list3.txt", "-c", "copy", "video3_raw.mp4"], check=True)

# zaman çizelgesi
t = 0; T = {}
for x in S: T[x[0]] = (t, t + x[2]); t += x[2]
tel0, tel1 = T["e01"][0], T["e03"][1]
k0, k1 = T["e08"]
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
                f"[0][n][st]amix=inputs=3:normalize=0,afade=t=in:d=0.2,afade=t=out:st={TOTAL-1.5}:d=1.5,volume=0.45[a]",
                "-map", "[a]", "-ac", "2", "-c:a", "aac", "-b:a", "160k", "music3.m4a"], check=True)
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", "video3_raw.mp4", "-i", "music3.m4a",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-maxrate", "6M", "-bufsize", "12M", "-pix_fmt", "yuv420p",
                "-c:a", "copy", "-shortest", "-movflags", "+faststart", "son_vagon_3_fon.mp4"], check=True)
print("ok", TOTAL)
