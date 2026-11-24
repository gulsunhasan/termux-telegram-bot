#!/data/data/com.termux/files/usr/bin/bash
# Termux için tek komutla kurulum.
# Kullanım:  bash kurulum.sh
set -e

echo "📦 Paketler güncelleniyor..."
pkg update -y && pkg upgrade -y
pkg install -y python git

echo "🐍 Python kütüphaneleri kuruluyor..."
pip install -r requirements.txt

if [ ! -f .env ]; then
  cp .env.example .env
  echo ""
  echo "🔑 .env dosyası oluşturuldu."
  read -rp "BotFather'dan aldığın token'ı yapıştır: " TOKEN
  sed -i "s|^BOT_TOKEN=.*|BOT_TOKEN=${TOKEN}|" .env
fi

chmod +x baslat.sh

# Telefon uyusa bile Termux çalışmaya devam etsin
command -v termux-wake-lock >/dev/null && termux-wake-lock || true

echo ""
echo "✅ Kurulum tamam! Botu başlatmak için:  ./baslat.sh"
echo "   Telefon açılınca otomatik başlasın istersen README'deki 'Otomatik başlatma' bölümüne bak."
