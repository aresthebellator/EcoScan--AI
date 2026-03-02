from telegram.ext import ApplicationBuilder, MessageHandler, filters
from bot import handle_photo
from ai_service import scan_photos
import os

def main():
    TOKEN = "8734746238:AAEop0Cyu52vY5Reg9YaDh6rTHF11-dQKsA"

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO,
        lambda u, c: handle_photo(u,c,scan_photos)))
    print("Il bot e' stato avviato e l'IA e' pronta...")
    app.run_polling()


if __name__ == "__main__":
    main()