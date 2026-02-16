import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from tiktokapi import TikTokApi
from youtube_dl import YoutubeDL

# Set logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Token bot Telegram Anda
TELEGRAM_TOKEN = '8353682116:AAG-XvsJxaMZ83leHuJNXNR8uy7ZgXHlX2s'

# Fungsi untuk mengunduh video TikTok
def download_tiktok(url):
    api = TikTokApi.get_instance()
    video = api.video(url)
    return video.download()

# Fungsi untuk mengunduh video Facebook
def download_facebook(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
    }
    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=True)
    return result['url']

# Fungsi untuk menghapus watermark pada video (gunakan ffmpeg)
def remove_watermark(input_path, output_path):
    # Ganti dengan perintah ffmpeg untuk menghapus watermark
    pass

# Fungsi untuk mendeteksi jenis URL dan mengunduhnya
async def detect_and_download(update: Update, context):
    url = update.message.text
    
    if "tiktok.com" in url:
        video_path = download_tiktok(url)
        update.message.reply_text(f"Video TikTok berhasil diunduh: {video_path}")
    
    elif "facebook.com" in url:
        video_path = download_facebook(url)
        update.message.reply_text(f"Video Facebook berhasil diunduh: {video_path}")
    
    else:
        update.message.reply_text("Tautan tidak dikenali. Pastikan itu adalah tautan TikTok atau Facebook!")

# Fungsi utama untuk memulai bot
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT, detect_and_download))
    
    # Menjalankan bot
    application.run_polling()

if __name__ == '__main__':
    main()