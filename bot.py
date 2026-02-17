import logging
import yt_dlp
from telegram import Update
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Token Bot Telegram Anda
TELEGRAM_TOKEN = '8353682116:AAG-XvsJxaMZ83leHuJNXNR8uy7ZgXHlX2s'

# Fungsi untuk mengunduh video TikTok menggunakan yt-dlp
def download_tiktok(url):
    ydl_opts = {
        'outtmpl': 'downloads/%(id)s.%(ext)s',  # Template untuk output file
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_url = info_dict['url']  # Mendapatkan URL video setelah diunduh
    return video_url

# Fungsi untuk mengunduh video Facebook menggunakan yt-dlp
def download_facebook(url):
    ydl_opts = {
        'outtmpl': 'downloads/%(id)s.%(ext)s',  # Template untuk output file
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_url = info_dict['url']  # Mendapatkan URL video setelah diunduh
    return video_url

# Fungsi untuk mendeteksi jenis URL dan mengunduhnya
async def detect_and_download(update: Update, context):
    url = update.message.text
    logger.info(f"Mendeteksi URL: {url}")

    if "tiktok.com" in url:
        # Jika URL TikTok ditemukan
        video_url = download_tiktok(url)
        await update.message.reply_text(f"Video TikTok berhasil diunduh: {video_url}")
    elif "facebook.com" in url:
        # Jika URL Facebook ditemukan
        video_url = download_facebook(url)
        await update.message.reply_text(f"Video Facebook berhasil diunduh: {video_url}")
    else:
        # Jika URL tidak dikenali
        await update.message.reply_text("Tautan tidak dikenali. Pastikan itu adalah tautan TikTok atau Facebook!")

# Fungsi utama untuk memulai bot
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Menambahkan handler untuk mendeteksi URL dan mengunduh video
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, detect_and_download))

    # Menjalankan bot
    application.run_polling()

if __name__ == '__main__':
    main()
