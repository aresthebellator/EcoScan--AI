from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters
from bot import handle_photo, handle_email
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
        await handle_photo(u, c, scan_photos)

    async def email_handler(u, c):
        await handle_email(u, c, email_comune)

    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    app.add_handler(CommandHandler("email", email_handler))

    print("Il bot è stato avviato e l'IA è pronta...")
    app.run_polling()

if __name__ == "__main__":
    main()