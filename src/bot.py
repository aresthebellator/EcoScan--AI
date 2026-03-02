from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE, ia_function):
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    path = f"{photo.file_id}.jpg"
    await file.download_to_drive(path)

    risposta = ia_function(path,update.message.caption or "")

    await update.message.reply_text(risposta)
    os.remove(path)

