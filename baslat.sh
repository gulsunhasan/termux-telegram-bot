#!/usr/bin/env bash
# Botu başlatır; çökerse ya da internet koparsa 5 saniye sonra kendini yeniden açar.
cd "$(dirname "$0")"
command -v termux-wake-lock >/dev/null && termux-wake-lock

while true; do
  echo "$(date '+%F %T') ▶ Bot başlatılıyor..." | tee -a bot.log
  python bot.py 2>&1 | tee -a bot.log
  echo "$(date '+%F %T') ⚠ Bot durdu, 5 sn sonra yeniden başlayacak (çıkmak için Ctrl+C iki kez)" | tee -a bot.log
  sleep 5
done
