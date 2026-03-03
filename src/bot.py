from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from segnalazioni import salva_segnalazione, get_riepilogo
from ai_service import estrai_gravita
import os

ASPETTA_COMUNE = 1
ASPETTA_VIA = 2


foto_temp = {}

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    messaggio = (
        "👋 Benvenuto su <b>EcoScan</b>!\n\n"
        "Ecco cosa posso fare per te:\n\n"
        "📸 <b>Invia una foto</b> — Analizzo la sporcizia e salvo la segnalazione\n"
        "📋 /comandi — Mostra questo elenco\n"
        "📊 /segnalazioni — Vedi tutte le segnalazioni\n"
    )
    await update.message.reply_text(messaggio, parse_mode="HTML")

async def handle_comandi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_start(update, context)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE, ia_function):
    await update.message.reply_text("🔍 Sto analizzando l'immagine...")

    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    path = f"foto_{photo.file_id}.jpg"
    await file.download_to_drive(path)

    try:
        risposta = ia_function(path, update.message.caption or "")
        gravita = estrai_gravita(risposta)
        await update.message.reply_text(risposta)

        if gravita == "MASSIMA" or gravita == "MEDIA":
            foto_temp[update.message.from_user.id] = {
                "path": path,
                "analisi": risposta,
                "gravita": gravita
            }
            await update.message.reply_text("📍 In quale via si trova il problema? Scrivi l'indirizzo:")
            return ASPETTA_VIA
        else:
            
            salva_segnalazione(
                via="Non specificata",
                gravita=gravita,
                analisi=risposta,
                foto_path=path,
                user_id=update.message.from_user.id
            )

    except Exception as e:
        await update.message.reply_text(f"Errore: {str(e)}")
        if os.path.exists(path):
            os.remove(path)

async def salva_con_via(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    via = update.message.text.strip()

    if user_id not in foto_temp:
        await update.message.reply_text("Nessuna foto in attesa. Invia prima una foto.")
        return ConversationHandler.END

    dati = foto_temp.pop(user_id)
    segnalazione_id = salva_segnalazione(
        via=via,
        gravita=dati["gravita"],
        analisi=dati["analisi"],
        foto_path=dati["path"],
        user_id=user_id
    )

    emoji = "🔴" if dati["gravita"] == "MASSIMA" else "🟡" if dati["gravita"] == "MEDIA" else "🟢"
    await update.message.reply_text(
        f"✅ Segnalazione <b>#{segnalazione_id}</b> salvata!\n\n"
        f"📍 Via: {via}\n"
        f"{emoji} Gravità: {dati['gravita']}",
        parse_mode="HTML"
    )
    return ConversationHandler.END

async def handle_segnalazioni(update: Update, context: ContextTypes.DEFAULT_TYPE):
    riepilogo = get_riepilogo()
    await update.message.reply_text(riepilogo, parse_mode="HTML")

async def chiedi_comune(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("In quale comune si trova la strada? Scrivi il nome:")
    return ASPETTA_COMUNE

async def manda_email(update: Update, context: ContextTypes.DEFAULT_TYPE, email_function):
    comune = update.message.text.strip()
    email = email_function(comune)
    await update.message.reply_text(
        f"📧 Email comune di {comune.capitalize()}:\n<code>{email}</code>",
        parse_mode="HTML"
    )
    return ConversationHandler.END