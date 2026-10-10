import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import yt_dlp

TOKEN = "8311264471:AAEW_M-v98k0iA_QlrRLOPjtLCYZJ_EJrms"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً بك! أرسل لي رابط الفيديو وسأقوم بتحميله لك مجاناً.")

async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if not url.startswith("http"):
        await update.message.reply_text("عافاك أرسل رابط صحيح.")
        return

    msg = await update.message.reply_text("⏳ جاري التحميل، انتظر قليلاً...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(id)s.%(ext)s',
    }

    file_path = None
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        with open(file_path, 'rb') as video_file:
            await update.message.reply_video(video=video_file)

        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"حدث خطأ أثناء التحميل: {str(e)}")

    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_media))
    app.run_polling()
      
