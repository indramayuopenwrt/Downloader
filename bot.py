from telegram import Update
from telegram.ext import Application, MessageHandler, filters
import logging

TELEGRAM_TOKEN = '8353682116:AAG-XvsJxaMZ83leHuJNXNR8uy7ZgXHlX2s'

# Set logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Fungsi untuk mendeteksi dan mengunduh video
async def detect_and_download(update: Update, context):
    url = update.message.text
    
    if "tiktok.com" in url:
        video_url = download_tiktok(url)
        await update.message.reply_text(f"Video TikTok berhasil diunduh: {video_url}")
    else:
        await update.message.reply_text("Tautan tidak dikenali.")

# Fungsi utama untuk memulai bot menggunakan Webhook
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Menambahkan handler
    application.add_handler(MessageHandler(filters.TEXT, detect_and_download))

    # Menyeting webhook URL
    application.run_webhook(
        listen="0.0.0.0",
        port=5000,
        url_path=TELEGRAM_TOKEN,
        webhook_url=f"web-production-337ef.up.railway.app/8353682116:AAG-XvsJxaMZ83leHuJNXNR8uy7ZgXHlX2s",
    )

if __name__ == '__main__':
    main()
