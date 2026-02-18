import logging
import yt_dlp
from telegram import Update
from telegram.ext import Application, MessageHandler, filters
import requests
import re

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Token Bot Telegram Anda
TELEGRAM_TOKEN = '8353682116:AAG-XvsJxaMZ83leHuJNXNR8uy7ZgXHlX2s'

# Fungsi untuk memverifikasi apakah URL adalah link video Facebook yang valid
def is_valid_facebook_url(url):
    # Cek apakah URL adalah link video Facebook yang valid
    return bool(re.match(r'https://www\.facebook\.com/.*?/videos/\d+', url))

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
            view_count = info_dict.get('view_count', 'Tidak diketahui')  # Jumlah tampilan
            like_count = info_dict.get('like_count', 'Tidak diketahui')  # Jumlah reaksi
            uploader = info_dict.get('uploader', 'Pengunggah tidak diketahui')  # Nama pengunggah

        logger.info(f"Video TikTok berhasil diunduh: {video_url}")
        short_url = shorten_url(video_url)  # Memendekkan URL
        caption = f"🎬 {view_count} tampilan ・ {like_count} reaksi\n"
        caption += f"👤 {uploader}\n"
        caption += f"📌 {description}\n\n"
        caption += f"Link Unduhan: {short_url}"
        
        return caption
    except Exception as e:
        logger.error(f"Gagal mengunduh video TikTok: {e}")
        return None

# Fungsi untuk mengunduh video Facebook menggunakan yt-dlp dan mendapatkan metadata
def download_facebook(url):
    if not is_valid_facebook_url(url):
        return "URL Facebook tidak valid. Pastikan itu adalah link video langsung."

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
            view_count = info_dict.get('view_count', 'Tidak diketahui')  # Jumlah tampilan
            like_count = info_dict.get('like_count', 'Tidak diketahui')  # Jumlah reaksi
            uploader = info_dict.get('uploader', 'Pengunggah tidak diketahui')  # Nama pengunggah

        logger.info(f"Video Facebook berhasil diunduh: {video_url}")
        short_url = shorten_url(video_url)  # Memendekkan URL
        caption = f"🎬 {view_count} tampilan ・ {like_count} reaksi\n"
        caption += f"👤 {uploader}\n"
        caption += f"📌 {description}\n\n"
        caption += f"Link Unduhan: {short_url}"

        return caption
    except Exception as e:
        logger.error(f"Gagal mengunduh video Facebook: {e}")
        return "Gagal mengunduh video Facebook."

# Fungsi untuk mendeteksi jenis URL dan mengunduhnya
async def detect_and_download(update: Update, context):
    url = update.message.text
    logger.info(f"Mendeteksi URL: {url}")
    message = await update.message.reply_text("🔄 Mengunduh video, mohon tunggu...")

    if "tiktok.com" in url:
        # Jika URL TikTok ditemukan
        caption = download_tiktok(url)
        if caption:
            await message.edit_text(caption)
        else:
            await message.edit_text("Gagal mengunduh video TikTok.")
    elif "facebook.com" in url:
        # Jika URL Facebook ditemukan
        caption = download_facebook(url)
        if caption:
            await message.edit_text(caption)
        else:
            await message.edit_text("Gagal mengunduh video Facebook.")
    else:
        # Jika URL tidak dikenali
        await message.edit_text("Tautan tidak dikenali. Pastikan itu adalah tautan TikTok atau Facebook!")

# Fungsi utama untuk memulai bot
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Menambahkan handler untuk mendeteksi URL dan mengunduh video
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, detect_and_download))

    # Menjalankan bot
    application.run_polling()

if __name__ == '__main__':
    main()
