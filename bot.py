import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters
from bs4 import BeautifulSoup
import yt_dlp

# Fungsi untuk menghapus webhook
def remove_webhook(token):
    url = f'https://api.telegram.org/bot{token}/deleteWebhook'
    response = requests.get(url)
    if response.status_code == 200:
        print("Webhook berhasil dihapus.")
    else:
        print("Gagal menghapus webhook.")

# Fungsi untuk mendapatkan metadata description dari URL
def get_metadata(url):
    try:
        # Mendapatkan HTML dari URL
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Mencari tag meta description
        description = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
        if description:
            return description.get('content')
        else:
            return "Deskripsi tidak ditemukan."
    except Exception as e:
        return f"Terjadi kesalahan: {e}"

# Fungsi untuk mengonversi URL ke public link (untuk Facebook dan TikTok)
def convert_to_public_link(url):
    if "facebook.com" in url:
        return url.split('?')[0]  # Menghapus parameter query dari link
    elif "tiktok.com" in url:
        return url.split('?')[0]  # Menghapus parameter query dari link
    return url

# Fungsi untuk mengunduh dan mengirimkan video TikTok
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

# Fungsi untuk mengunduh dan mengirimkan video Facebook
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

# Fungsi untuk mendeteksi platform berdasarkan link
def detect_platform(url):
    if "facebook.com" in url:
        return "Facebook"
    elif "tiktok.com" in url:
        return "TikTok"
    else:
        return "Platform Tidak Tersedia."

# Fungsi untuk menangani pesan yang dikirim ke bot
async def handle_message(update: Update, context):
    message = update.message.text
    url = message.strip()

    # Memastikan link valid
    if "http" in url:
        # Mengambil platform berdasarkan link
        platform = detect_platform(url)
        
        # Mengambil metadata dari URL
        metadata = get_metadata(url)
        
        # Mengonversi ke public link (jika perlu)
        public_link = convert_to_public_link(url)

        # Mengunduh video berdasarkan platform
        if platform == "TikTok":
            video_file, video_title, video_description = download_tiktok(url)
        elif platform == "Facebook":
            video_file, video_title, video_description = download_facebook(url)
        else:
            await update.message.reply_text(f"Platform {platform} tidak dikenali.")
            return
        
        # Mengirimkan video dan metadata ke pengguna
        if video_file:
            await update.message.reply_text(f"**Judul Video**: {video_title}\n**Deskripsi**: {video_description}\n**Link Publik**: {public_link}")
            await update.message.reply_video(video_file)
        else:
            await update.message.reply_text("Gagal mengunduh video.")
    else:
        await update.message.reply_text("Mohon kirimkan link yang valid.")

def main():
    # Gantilah 'YOUR_BOT_TOKEN' dengan token bot Anda
    token = '8353682116:AAG-XvsJxaMZ83leHuJNXNR8uy7ZgXHlX2s'

    # Menghapus webhook yang ada (untuk memastikan polling yang digunakan)
    remove_webhook(token)

    # Membuat aplikasi bot dengan token
    application = Application.builder().token(token).build()

    # Menambahkan handler untuk menangani pesan
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Menjalankan polling
    application.run_polling()

if __name__ == '__main__':
    main()
