import ollama

def scan_photos(image_path, user_comment=""):
    system_instructions = (
        "Sei un assistente intelligente specializzato nel decoro urbano. Analizza l'immagine di una strada e "
        "valuta il livello di sporcizia. Rispondi seguendo rigorosamente queste categorie:\n"
        "Concentrati soprattuto su sacchetti, mobili abbandonati, detriti, fazzoletti, tanta plastica"
        "1. GRAVITA' MASSIMA: Se c'è molta sporcizia o rifiuti ingombranti. In questo caso, scrivi anche una bozza di email da inviare al comune.\n"
        "2. GRAVITA' MEDIA: Se la sporcizia è presente ma non critica.\n"
        "3. GRAVITA' MINIMA: Se la strada è pulita o quasi.\n"
        "Sii preciso e diretto."
    )

    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()

        response = ollama.chat(
            model='llava',
            messages=[
                {
                    'role': 'system',
                    'content': system_instructions
                },
                {
                    
                    'role': 'user', 
                    'content': f"Ecco l'immagine. {user_comment}",
                    'images': [image_data]
                },
            ],
            options={'temperature': 0.5}
        )
        return response['message']['content']
    except Exception as e:
        return f"Non sono riuscito a guardare bene la tua foto: {str(e)}"