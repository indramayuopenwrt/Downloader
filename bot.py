import logging
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Set logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Token bot Telegram Anda
TELEGRAM_TOKEN = '8353682116:AAG-XvsJxaMZ83leHuJNXNR8uy7ZgXHlX2s'

# Fungsi untuk mengunduh video TikTok
def download_tiktok(url):
    ydl_opts = {
        'outtmpl': 'downloads/%(id)s.%(ext)s',  # Template untuk nama file output
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_url = info_dict['url']
    return video_url

# Fungsi untuk mendeteksi jenis URL dan mengunduhnya
async def detect_and_download(update: Update, context):
    url = update.message.text
    
    if "tiktok.com" in url:
        video_url = download_tiktok(url)
        update.message.reply_text(f"Video TikTok berhasil diunduh: {video_url}")
    
    elif "facebook.com" in url:
        # Gantilah ini dengan kode unduhan Facebook Anda
        update.message.reply_text("Fitur Facebook sedang dalam pengembangan.")
    
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
