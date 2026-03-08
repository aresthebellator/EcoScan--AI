from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ConversationHandler, filters
from bot import handle_photo, chiedi_comune, manda_email, handle_start, handle_comandi, handle_segnalazioni, salva_con_via, ASPETTA_COMUNE, ASPETTA_VIA
from ai_service import scan_photos, email_comune
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TOKEN:
        raise ValueError("TELEGRAM_TOKEN non trovato nel file .env")

    app = ApplicationBuilder().token(TOKEN).build()

    async def photo_handler(u, c):
        return await handle_photo(u, c, scan_photos)

    async def email_handler(u, c):
        return await manda_email(u, c, email_comune)

    foto_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.PHOTO, photo_handler)],
        states={
            ASPETTA_VIA: [MessageHandler(filters.TEXT & ~filters.COMMAND, salva_con_via)]
        },
        fallbacks=[]
    )

    email_conv = ConversationHandler(
        entry_points=[CommandHandler("email", chiedi_comune)],
        states={
            ASPETTA_COMUNE: [MessageHandler(filters.TEXT & ~filters.COMMAND, email_handler)]
        },
        fallbacks=[]
    )

    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(CommandHandler("comandi", handle_comandi))
    app.add_handler(CommandHandler("segnalazioni", handle_segnalazioni))
    app.add_handler(foto_conv)
    app.add_handler(email_conv)

    print("Il bot è stato avviato e l'IA è pronta...\n")
    print("Puoi avviare il programma comune_dashboard")
    app.run_polling()

if __name__ == "__main__":
    main()