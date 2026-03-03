import ollama

COMUNI_EMAIL = {
    "bari": "protocollo@comune.bari.it",
    "roma": "urp@comune.roma.it",
    "milano": "comune.milano@pec.it",
    "napoli": "sindaco@comune.napoli.it",
    "torino": "urp@comune.torino.it",
}

def scan_photos(image_path, user_comment = ""):
    system_instructions = (
        "Sei un assistente per il decoro urbano. Analizza SOLO il livello di sporcizia nella strada e scrivi come in modo formare l'utente possa scrivere l'email. "
        "NON descrivere l'immagine in modo generico. "
        "Rispondi ESCLUSIVAMENTE con una di queste categorie:\n\n"
        "GRAVITA' MASSIMA: se vedi sacchetti, rifiuti ingombranti, mobili abbandonati, detriti. "
        "In questo caso scrivi anche una bozza di email al comune.\n"
        "GRAVITA' MEDIA: se c'è qualche rifiuto ma non critico.\n"
        "GRAVITA' MINIMA: se la strada è pulita o quasi pulita.\n\n"
        "Inizia SEMPRE la risposta con 'GRAVITA' MASSIMA', 'GRAVITA' MEDIA' o 'GRAVITA' MINIMA'."
    )

    try:
        with open(image_path,'rb')as f:
            image_data = f.read()
        response = ollama.chat(
            model='llava',
            messages=[
                {'role': 'system','content':system_instructions},
                {'role':'user','content': f"Analizza la sporcizia in questa immaghine. {user_comment}",'images': [image_data]},
            ],
            options={'temperature': 0.2}
        )
        return response['message']['content']
    except Exception as e:
        return f"Non sono riuscito a guardare bene la tua foto: {str(e)}"
    
def email_comune(nome_comune : str) -> str:
    key = nome_comune.strip().lower()
    if key in COMUNI_EMAIL:
        return COMUNI_EMAIL[key]
    else:
        return f"Email per '{nome_comune}' non trovata. Cercala su https://www.comuni-italiani.it/"
    