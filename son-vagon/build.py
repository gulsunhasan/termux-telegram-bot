import json, subprocess, os
D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
TOTAL = 46.2
W_ = [("Tak.",0.16,1.04),("Tak.",1.12,1.92),("Tak.",1.96,2.4),("Bu",2.96,3.04),("ses",3.12,3.36),("arka",3.44,3.68),("vagondan",3.76,4.16),("geliyor.",4.24,4.88),("Ve",4.96,5.04),("trende",5.12,5.44),("senden",5.56,5.84),("başka",5.88,6.08),("kimse",6.24,6.56),("yok.",6.6,6.88),
("Kırk",7.52,7.68),("saniye",7.76,8.16),("önce.",8.2,8.8),("Gece",9.04,9.36),("01.13.",9.44,10.24),("Son",10.36,10.48),("metrodasın.",10.6,11.44),("Üç",11.48,11.6),("durak",11.68,11.92),("kaldı.",11.96,12.64),("Anons",12.72,13.04),("cızırdıyor:",13.08,14.08),("“Sayın",14.12,14.4),("yolcu,",14.48,15.04),("lütfen",15.12,15.44),("yerinizden",15.52,16.08),("kalkmayın.”",16.16,16.72),("Sayın",17.12,17.44),("yolcu...",17.52,18.48),("Tek",18.6,18.72),("kişi.",18.8,19.24),
("İki",19.44,19.6),("durak",19.68,19.92),("kaldı.",20,20.64),("Işıklar",20.68,21.12),("sönüyor.",21.2,21.84),("Kırmızı",21.88,22.24),("alarm",22.32,22.64),("yanıyor.",22.72,23.28),("Vuruşlar",23.36,23.76),("yaklaşıyor.",23.8,24.72),("Son",24.8,24.96),("durak.",25.04,25.44),("Tren",25.84,26.08),("duruyor...",26.16,27.04),("ama",27.16,27.28),("kapılar",27.36,27.68),("açılmıyor.",27.72,28.64),
("Önünde",28.68,29.04),("iki",29.12,29.28),("kapı",29.36,29.6),("var.",29.72,30.12),("A:",30.4,30.96),("Makinist",31,31.44),("kabini.",31.52,32.16),("Kilitli,",32.2,32.72),("ama",32.8,32.96),("içeriden",33.04,33.44),("ışık",33.52,33.68),("sızıyor.",33.76,34.24),("B:",34.72,35.28),("Arka",35.36,35.52),("vagonun",35.6,35.92),("kapısı.",36,36.56),("Ses",36.72,36.96),("oradan",37.04,37.28),("geliyor.",37.36,38.04),
("Sen",38.32,38.48),("hangisini",38.56,38.96),("seçerdin?",39.04,39.84),("Yorumlara",39.88,40.4),("A",40.48,40.64),("ya",40.72,40.8),("da",40.88,40.96),("B",41.04,41.2),("yaz.",41.24,41.76),("En",41.84,41.92),("çok",42,42.16),("oy",42.24,42.32),("alan",42.44,42.56),("kapıyı,",42.64,43.12),("yarın",43.2,43.36),("birlikte",43.44,43.76),("açıyoruz.",43.84,44.64)]

# altyazı grupları: cümle sonu veya 4 kelime
groups, cur = [], []
for w in W_:
    cur.append(w)
    if len(cur) >= 4 or w[0][-1] in ".?:,”" and len(cur) >= 2 or w[0].endswith((".", "?", "...", "”")):
        groups.append(cur); cur = []
if cur: groups.append(cur)

def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"
ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "",
       "[V4+ Styles]",
       "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
       "Style: S,Oswald,74,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,-1,0,0,0,100,100,1,0,1,6,2,2,60,60,520,1",
       "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
for i, g in enumerate(groups):
    st = g[0][1]; en = groups[i + 1][0][1] if i + 1 < len(groups) else TOTAL - 0.3
    en = min(en, g[-1][2] + 0.6)
    # aktif kelimeyi sarı vurgula
    for j, w in enumerate(g):
        ws = w[1]; we = g[j + 1][1] if j + 1 < len(g) else en
        txt = " ".join(("{\\c&H00D8FF&}" + x[0].upper() + "{\\c&HFFFFFF&}") if k == j else x[0].upper() for k, x in enumerate(g))
        ass.append(f"Dialogue: 0,{ts(ws)},{ts(we)},S,,0,0,0,,{txt}")
open("subs.ass", "w").write("\n".join(ass))

# çekimler: (ad, sahne, başla, bitiş, büyük yazı, rozet, kırmızı rozet, top, zoom yönü)
S = [
 ("s01","yolcu_kirmizi",0,2.9,"TAK.<br>TAK.<br>TAK.","SON DURAK",True,None,"in"),
 ("s02","vagon_kirmizi",2.9,7.35,"TRENDE<br>KİMSE YOK.","SON DURAK",True,None,"in"),
 ("s03","vagon_mavi",7.35,11.45,"40 SANİYE<br>ÖNCE","GECE 01:13",False,None,"in"),
 ("s04","yolcu_mavi",11.45,14.1,"SON METRO.","3 DURAK KALDI",False,None,"out"),
 ("s05","anons",14.1,17.05,"","3 DURAK KALDI",False,None,"in"),
 ("s06","yolcu_mavi",17.05,19.4,"TEK KİŞİ.","3 DURAK KALDI",False,None,"in"),
 ("s07","vagon_mavi",19.4,21.15,"IŞIKLAR<br>SÖNÜYOR.","2 KALDI",False,None,"in"),
 ("s08","vagon_kirmizi",21.15,24.75,"VURUŞLAR<br>YAKLAŞIYOR.","2 KALDI",True,None,"in"),
 ("s09","durak",24.75,28.65,"KAPILAR<br>AÇILMIYOR.","SON DURAK",True,560,"in"),
 ("s10","kapilar",28.65,30.35,"İKİ KAPI.","SON DURAK",True,250,"out"),
 ("s11","kapilar",30.35,34.6,"A: IŞIK<br>SIZIYOR","SON DURAK",True,250,"in"),
 ("s12","kapilar",34.6,38.2,"B: SES<br>ORADAN","SON DURAK",True,250,"out"),
 ("s13","kapilar",38.2,TOTAL,"A MI, B Mİ?<br><span style='font-size:72px'>YORUMLARA YAZ</span>","SEN SEÇ",True,250,"out"),
]
jobs = [dict(name=n, scene=sc, big=b, badge=bd, red=r, top=tp) for n, sc, a, e, b, bd, r, tp, z in S]
json.dump(jobs, open("shots.json", "w"))
subprocess.run(["python3", "render.py", "shots.json", "shots"], check=True)

FPS = 30
clips = []
for n, sc, a, e, b, bd, r, tp, z in S:
    dur = e - a; fr = round(dur * FPS)
    if z == "in": zx, zy, zz = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)", f"1+0.10*on/{fr}"
    elif z == "out": zx, zy, zz = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)", f"1.10-0.10*on/{fr}"
    elif z == "face": zx, zy, zz = "iw/2-(iw/zoom/2)+20", f"(ih*0.42)-(ih/zoom/2)", f"1.25+0.15*on/{fr}"
    elif z == "left": zx, zy, zz = "iw*0.27-(iw/zoom/2)", "ih*0.5-(ih/zoom/2)", f"1.25+0.08*on/{fr}"
    else: zx, zy, zz = "iw*0.73-(iw/zoom/2)", "ih*0.5-(ih/zoom/2)", f"1.25+0.08*on/{fr}"
    # büyük yazı yakınlaşmada kesilmesin diye: zoom yalnız sahnede değil tüm karede; kenar zoom çekimleri için max(0,..)
    vf = (f"scale=2160:3840,zoompan=z='{zz}':x='max(0,min(iw-iw/zoom,{zx}))':y='max(0,min(ih-ih/zoom,{zy}))':d={fr}:s=1080x1920:fps={FPS}")
    if sc.endswith("kirmizi") or sc in ("durak", "kapilar"):
        vf += ",eq=brightness='0.06*sin(2*PI*t*1.6)'"  # alarm nabzı
    vf += ",format=yuv420p"
    out = f"clip_{n}.mp4"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-loop", "1", "-i", f"shots/{n}.png", "-vf", vf,
                    "-frames:v", str(fr), "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", out], check=True)
    clips.append(out)
open("list.txt", "w").write("".join(f"file '{c}'\n" for c in clips))
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", "list.txt", "-c", "copy", "video_raw.mp4"], check=True)

# fon: alçak drone + tünel uğultusu + alarm bipleri (21.2-28.6) — tamamen sentetik, telifsiz
music = (f"aevalsrc='0.22*sin(2*PI*55*t)*(0.7+0.3*sin(2*PI*0.13*t))+0.12*sin(2*PI*82.4*t+sin(2*PI*0.2*t))+0.06*sin(2*PI*110.5*t)"
         f"+if(between(t,21.2,28.6),0.10*sin(2*PI*880*t)*lt(mod(t,0.8),0.18),0)"
         f"+if(lt(t,2.5),0.25*sin(2*PI*60*t)*exp(-14*mod(t-0.12,0.88))*lt(mod(t-0.12,0.88),0.5),0)':s=44100:d={TOTAL}")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i", music,
                "-f", "lavfi", "-i", f"anoisesrc=c=brown:a=0.35:d={TOTAL}",
                "-filter_complex", "[1]lowpass=f=180,volume=0.6[n];[0][n]amix=inputs=2:normalize=0,afade=t=in:d=0.3,afade=t=out:st=" + str(TOTAL - 1.5) + ":d=1.5,volume=0.55[a]",
                "-map", "[a]", "-ac", "2", "-c:a", "aac", "-b:a", "160k", "music.m4a"], check=True)
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", "video_raw.mp4", "-i", "music.m4a",
                "-vf", f"ass=subs.ass:fontsdir={D}/fonts", "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-maxrate", "6M", "-bufsize", "12M", "-pix_fmt", "yuv420p",
                "-c:a", "copy", "-shortest", "-movflags", "+faststart", "son_vagon_1_sessiz.mp4"], check=True)
print("ok")
