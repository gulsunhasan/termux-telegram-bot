"""
Termux Telegram Bot Şablonu
Telefonda (Termux) ya da herhangi bir Linux'ta 7/24 çalışan, Türkçe, hazır Telegram botu.

Komutlar:
  /start      - Karşılama
  /yardim     - Komut listesi
  /not        - Not ekle          (/not süt al)
  /notlar     - Notlarını listele
  /notsil     - Not sil           (/notsil 3)
  /hatirlat   - Hatırlatıcı kur   (/hatirlat 10 çayı ocaktan al)
  /doviz      - Döviz kuru        (/doviz  ya da  /doviz GBP)
  /durum      - Botun çalışma süresi ve kullanıcı sayısı
"""

import logging
import os
import sqlite3
import time
from datetime import datetime

import httpx
from dotenv import load_dotenv
from telegram import BotCommand, Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
DB_PATH = os.getenv("DB_PATH", "bot.db")
BASLANGIC = time.time()

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger("bot")


# ---------------------------------------------------------------- veritabanı
def db() -> sqlite3.Connection:
    con = sqlite3.connect(DB_PATH)
    con.execute(
        "CREATE TABLE IF NOT EXISTS notlar ("
        " id INTEGER PRIMARY KEY AUTOINCREMENT,"
        " kullanici INTEGER NOT NULL,"
        " metin TEXT NOT NULL,"
        " tarih TEXT NOT NULL)"
    )
    con.execute(
        "CREATE TABLE IF NOT EXISTS kullanicilar ("
        " id INTEGER PRIMARY KEY,"
        " ad TEXT,"
        " ilk_gorulme TEXT)"
    )
    return con


def kullanici_kaydet(update: Update) -> None:
    u = update.effective_user
    if not u:
        return
    with db() as con:
        con.execute(
            "INSERT OR IGNORE INTO kullanicilar (id, ad, ilk_gorulme) VALUES (?, ?, ?)",
            (u.id, u.full_name, datetime.now().isoformat(timespec="seconds")),
        )


# ---------------------------------------------------------------- komutlar
YARDIM = (
    "📋 *Komutlar*\n\n"
    "/not `metin` — not ekle\n"
    "/notlar — notlarını gör\n"
    "/notsil `numara` — not sil\n"
    "/hatirlat `dakika` `mesaj` — hatırlatıcı kur\n"
    "/doviz `[kur]` — güncel döviz (varsayılan USD, EUR)\n"
    "/durum — bot bilgisi\n"
    "/yardim — bu liste"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    kullanici_kaydet(update)
    ad = update.effective_user.first_name if update.effective_user else ""
    await update.message.reply_text(
        f"Merhaba {ad}! 👋\nBen 7/24 çalışan yardımcı botunum.\n\n" + YARDIM,
        parse_mode="Markdown",
    )


async def yardim(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(YARDIM, parse_mode="Markdown")


async def not_ekle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    kullanici_kaydet(update)
    metin = " ".join(context.args).strip()
    if not metin:
        await update.message.reply_text("Kullanım: /not süt al")
        return
    with db() as con:
        con.execute(
            "INSERT INTO notlar (kullanici, metin, tarih) VALUES (?, ?, ?)",
            (update.effective_user.id, metin[:1000], datetime.now().strftime("%d.%m %H:%M")),
        )
    await update.message.reply_text("✅ Not kaydedildi.")


async def notlar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    with db() as con:
        satirlar = con.execute(
            "SELECT id, metin, tarih FROM notlar WHERE kullanici = ? ORDER BY id DESC LIMIT 20",
            (update.effective_user.id,),
        ).fetchall()
    if not satirlar:
        await update.message.reply_text("Henüz notun yok. Eklemek için: /not metin")
        return
    liste = "\n".join(f"#{i}  {m}  ({t})" for i, m, t in satirlar)
    await update.message.reply_text(f"🗒 Notların:\n\n{liste}\n\nSilmek için: /notsil numara")


async def not_sil(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args or not context.args[0].lstrip("#").isdigit():
        await update.message.reply_text("Kullanım: /notsil 3")
        return
    not_id = int(context.args[0].lstrip("#"))
    with db() as con:
        silinen = con.execute(
            "DELETE FROM notlar WHERE id = ? AND kullanici = ?",
            (not_id, update.effective_user.id),
        ).rowcount
    await update.message.reply_text("🗑 Silindi." if silinen else "Bu numarada notun yok.")


async def _hatirlatma_gonder(context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(context.job.chat_id, f"⏰ Hatırlatma: {context.job.data}")


async def hatirlat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 2 or not context.args[0].isdigit():
        await update.message.reply_text("Kullanım: /hatirlat 10 çayı ocaktan al")
        return
    dakika = int(context.args[0])
    if not 1 <= dakika <= 1440:
        await update.message.reply_text("Süre 1 ile 1440 dakika (24 saat) arasında olmalı.")
        return
    mesaj = " ".join(context.args[1:])
    context.job_queue.run_once(
        _hatirlatma_gonder, dakika * 60, chat_id=update.effective_chat.id, data=mesaj
    )
    await update.message.reply_text(f"👍 {dakika} dakika sonra hatırlatacağım.")


async def doviz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    kurlar = [k.upper() for k in context.args] or ["USD", "EUR"]
    sonuc, tarih = [], ""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            for kur in kurlar[:5]:
                r = await client.get(
                    "https://api.frankfurter.app/latest", params={"from": kur, "to": "TRY"}
                )
                if r.status_code != 200:
                    sonuc.append(f"{kur}: bulunamadı")
                    continue
                veri = r.json()
                tarih = veri.get("date", tarih)
                sonuc.append(f"1 {kur} = {veri['rates']['TRY']:.2f} ₺")
        await update.message.reply_text("💱 " + "\n".join(sonuc) + (f"\n\n({tarih}, ECB)" if tarih else ""))
    except httpx.HTTPError:
        await update.message.reply_text("Kur servisine şu an ulaşılamıyor, biraz sonra dene.")


async def durum(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    sure = int(time.time() - BASLANGIC)
    saat, dk = divmod(sure // 60, 60)
    with db() as con:
        kisi = con.execute("SELECT COUNT(*) FROM kullanicilar").fetchone()[0]
    await update.message.reply_text(
        f"🟢 Çalışıyor\n⏱ Açık kalma süresi: {saat} sa {dk} dk\n👥 Kullanıcı: {kisi}"
    )


async def hata(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    log.error("Hata: %s", context.error, exc_info=context.error)


async def komutlari_ayarla(app: Application) -> None:
    await app.bot.set_my_commands(
        [
            BotCommand("yardim", "Komut listesi"),
            BotCommand("not", "Not ekle"),
            BotCommand("notlar", "Notlarını gör"),
            BotCommand("notsil", "Not sil"),
            BotCommand("hatirlat", "Hatırlatıcı kur"),
            BotCommand("doviz", "Döviz kuru"),
            BotCommand("durum", "Bot bilgisi"),
        ]
    )


def main() -> None:
    if not TOKEN:
        raise SystemExit("BOT_TOKEN bulunamadı. .env dosyasına BOT_TOKEN=... yaz (bkz. .env.example).")
    db().close()
    app = Application.builder().token(TOKEN).post_init(komutlari_ayarla).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler(["yardim", "help"], yardim))
    app.add_handler(CommandHandler("not", not_ekle))
    app.add_handler(CommandHandler("notlar", notlar))
    app.add_handler(CommandHandler("notsil", not_sil))
    app.add_handler(CommandHandler("hatirlat", hatirlat))
    app.add_handler(CommandHandler("doviz", doviz))
    app.add_handler(CommandHandler("durum", durum))
    app.add_error_handler(hata)
    log.info("Bot başladı. Durdurmak için Ctrl+C")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
