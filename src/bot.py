from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    messaggio = (
        "👋 Benvenuto su <b>EcoScan</b>!\n\n"
        "Ecco cosa posso fare per te:\n\n"
        "📸 <b>Invia una foto</b> — Analizzo la sporcizia nella strada\n"
        "📧 /email — Ti dico l'email del comune per segnalare\n"
        "📋 /comandi — Mostra questo elenco\n"
    )
    await update.message.reply_text(messaggio, parse_mode= "HTML")

async def handle_comandi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_start(update,context)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE, ia_function):
    await update.message.reply_text("Sto scannerizzando l'immagine")
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    path = f"{photo.file_id}.jpg"
    await file.download_to_drive(path)

    risposta = ia_function(path,update.message.caption or "")

    await update.message.reply_text(risposta)
    os.remove(path)

async def handle_email(update: Update, context: ContextTypes.DEFAULT_TYPE, email_function):
    comune = update.message.text.replace("/email", "").strip()
    if not comune:
        await update.message.reply_text("Scrivi il nome del comune, es: /email Bari")
        return

    email = email_function(comune)
    await update.message.reply_text(
        f"📧 Email comune di {comune.capitalize()}:\n<code>{email}</code>",
        parse_mode="HTML"
    )
