import logging
import yt_dlp
from telegram import Update
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler
import requests

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Token Bot Telegram Anda
TELEGRAM_TOKEN = '8353682116:AAG-XvsJxaMZ83leHuJNXNR8uy7ZgXHlX2s'

# Fungsi untuk memendekkan URL
def shorten_url(url):
    try:
        response = requests.get(f"https://api.shrtco.de/v2/shorten?url={url}")
        return response.json()['result']['full_short_link']
    except Exception as e:
        logger.error(f"Gagal memendekkan URL: {e}")
        return url  # Kembalikan URL aslinya jika pemendekan gagal

# Fungsi untuk mengunduh video TikTok menggunakan yt-dlp dan mendapatkan metadata
def download_tiktok(url):
    logger.info(f"Mulai mengunduh video TikTok: {url}")
    try:
        ydl_opts = {
            'outtmpl': 'downloads/%(id)s.%(ext)s',  # Template untuk output file
            'quiet': True,
            'noplaylist': True,
            'writeinfojson': True,  # Menyimpan metadata dalam format JSON
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_url = info_dict['url']  # Mendapatkan URL video setelah diunduh
            description = info_dict.get('description', 'Tidak ada deskripsi tersedia')  # Mendapatkan deskripsi
        logger.info(f"Video TikTok berhasil diunduh: {video_url}")
        short_url = shorten_url(video_url)  # Memendekkan URL
        return short_url, description
    except Exception as e:
        logger.error(f"Gagal mengunduh video TikTok: {e}")
        return None, None

# Fungsi untuk mengunduh video Facebook menggunakan yt-dlp dan mendapatkan metadata
def download_facebook(url):
    logger.info(f"Mulai mengunduh video Facebook: {url}")
    try:
        ydl_opts = {
            'outtmpl': 'downloads/%(id)s.%(ext)s',  # Template untuk output file
            'quiet': True,
            'noplaylist': True,
            'writeinfojson': True,  # Menyimpan metadata dalam format JSON
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_url = info_dict['url']  # Mendapatkan URL video setelah diunduh
            description = info_dict.get('description', 'Tidak ada deskripsi tersedia')  # Mendapatkan deskripsi
        logger.info(f"Video Facebook berhasil diunduh: {video_url}")
        short_url = shorten_url(video_url)  # Memendekkan URL
        return short_url, description
    except Exception as e:
        logger.error(f"Gagal mengunduh video Facebook: {e}")
        return None, None

# Fungsi untuk mendeteksi jenis URL dan mengunduhnya
async def detect_and_download(update: Update, context):
    url = update.message.text
    logger.info(f"Mendeteksi URL: {url}")

    if "tiktok.com" in url:
        # Jika URL TikTok ditemukan
        video_url, description = download_tiktok(url)
        if video_url:
            caption = f"{description}\n\nLink Unduhan: {video_url}"
            await update.message.reply_text(caption)
        else:
            await update.message.reply_text("Gagal mengunduh video TikTok.")
    elif "facebook.com" in url:
        # Jika URL Facebook ditemukan
        video_url, description = download_facebook(url)
        if video_url:
            caption = f"{description}\n\nLink Unduhan: {video_url}"
            await update.message.reply_text(caption)
        else:
            await update.message.reply_text("Gagal mengunduh video Facebook.")
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
