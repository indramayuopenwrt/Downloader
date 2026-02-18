import logging
import yt_dlp
from telegram import Update
from telegram.ext import Application, MessageHandler, filters

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Fungsi untuk mengunduh dan mengonversi video TikTok
def download_tiktok(url):
    logger.info(f"Mulai mengunduh video TikTok: {url}")
    try:
        ydl_opts = {
            'outtmpl': 'downloads/%(id)s.%(ext)s',  # Menyimpan video secara lokal
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',  # Konversi ke mp4
            }]
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_file = info_dict['filepath']
            video_title = info_dict.get('title', 'No Title Available')
            video_description = info_dict.get('description', 'No Description Available')
        logger.info(f"Video TikTok berhasil diunduh: {video_file}")
        return video_file, video_title, video_description
    except Exception as e:
        logger.error(f"Gagal mengunduh video TikTok: {e}")
        return None, None, None

# Fungsi untuk mengonversi dan mengunduh video Facebook
def download_facebook(url):
    logger.info(f"Mulai mengunduh video Facebook: {url}")
    try:
        ydl_opts = {
            'outtmpl': 'downloads/%(id)s.%(ext)s',  # Menyimpan video secara lokal
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',  # Konversi ke mp4
            }]
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_file = info_dict['filepath']
            video_title = info_dict.get('title', 'No Title Available')
            video_description = info_dict.get('description', 'No Description Available')
        logger.info(f"Video Facebook berhasil diunduh: {video_file}")
        return video_file, video_title, video_description
    except Exception as e:
        logger.error(f"Gagal mengunduh video Facebook: {e}")
        return None, None, None

# Fungsi untuk mendeteksi URL dan mengunduh video
async def detect_and_download(update: Update, context):
    url = update.message.text
    logger.info(f"Mendeteksi URL: {url}")

    if "tiktok.com" in url:
        # Mengonversi dan mengunduh video TikTok
        video_file, video_title, video_description = download_tiktok(url)
        if video_file:
            # Kirimkan video dan deskripsi ke pengguna
            await update.message.reply_text(f"**Judul Video**: {video_title}\n**Deskripsi**: {video_description}")
            await update.message.reply_video(video_file)
        else:
            await update.message.reply_text("Gagal mengunduh video TikTok.")
    elif "facebook.com" in url:
        # Mengonversi dan mengunduh video Facebook
        video_file, video_title, video_description = download_facebook(url)
        if video_file:
            # Kirimkan video dan deskripsi ke pengguna
            await update.message.reply_text(f"**Judul Video**: {video_title}\n**Deskripsi**: {video_description}")
            await update.message.reply_video(video_file)
        else:
            await update.message.reply_text("Gagal mengunduh video Facebook.")
    else:
        # Jika URL tidak dikenali
        await update.message.reply_text("Tautan tidak dikenali. Pastikan itu adalah tautan TikTok atau Facebook!")

# Fungsi utama untuk memulai bot
def main():
    application = Application.builder().token('8353682116:AAG-XvsJxaMZ83leHuJNXNR8uy7ZgXHlX2s').build()

    # Menambahkan handler untuk mendeteksi URL dan mengunduh video
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, detect_and_download))

    # Menjalankan bot
    application.run_polling()

if __name__ == '__main__':
    main()
