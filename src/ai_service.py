import ollama

COMUNI_EMAIL = {
    "bari": "protocollo@comune.bari.it",
    "roma": "urp@comune.roma.it",
    "milano": "comune.milano@pec.it",
    "napoli": "sindaco@comune.napoli.it",
    "torino": "urp@comune.torino.it",
    "palermo": "protocollo@comune.palermo.it",
    "genova": "urp@comune.genova.it",
    "bologna": "urp@comune.bologna.it",
    "firenze": "urp@comune.fi.it",
    "venezia": "protocollo@comune.venezia.it",
}

def estrai_gravita(risposta: str) -> str:
    risposta_upper = risposta.upper()
    if "MASSIMA" in risposta_upper:
        return "MASSIMA"
    elif "MEDIA" in risposta_upper:
        return "MEDIA"
    elif "MINIMA" in risposta_upper:
        return "MINIMA"
    return "SCONOSCIUTA"

def scan_photos(image_path, user_comment=""):
    system_instructions = (
        "Sei un sistema di rilevamento sporcizia urbana. Analizza SOLO i rifiuti visibili nell'immagine.\n\n"
        "REGOLE FERREE:\n"
        "- GRAVITA' MINIMA: strada pulita, qualche foglia, sporco normale. Nessun rifiuto evidente.\n"
        "- GRAVITA' MEDIA: qualche rifiuto piccolo, carta, mozziconi, sporco localizzato.\n"
        "- GRAVITA' MASSIMA: sacchetti aperti, mobili abbandonati, cumuli di rifiuti, detriti abbondanti.\n\n"
        "IMPORTANTE: Se non vedi chiaramente rifiuti, rispondi GRAVITA' MINIMA.\n"
        "Non esagerare. Sii oggettivo.\n"
        "Inizia SEMPRE la risposta con GRAVITA' MINIMA, GRAVITA' MEDIA o GRAVITA' MASSIMA."
    )

    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()

        response = ollama.chat(
            model='llava',
            messages=[
                {'role': 'system', 'content': system_instructions},
                {
                    'role': 'user',
                    'content': f"Analizza la sporcizia in questa immagine. {user_comment}",
                    'images': [image_data]
                },
            ],
            options={'temperature': 0.1}
        )
        risposta = response['message']['content']

        
        if "MASSIMA" in risposta.upper():
            verifica = ollama.chat(
                model='llava',
                messages=[
                    {
                        'role': 'user',
                        'content': (
                            "Guarda di nuovo questa immagine. "
                            "Ci sono DAVVERO sacchetti, mobili abbandonati o cumuli di rifiuti? "
                            "Rispondi solo SI o NO."
                        ),
                        'images': [image_data]
                    }
                ],
                options={'temperature': 0.1}
            )
            conferma = verifica['message']['content'].upper()
            if "NO" in conferma:
                risposta = risposta.upper().replace("MASSIMA", "MEDIA")

        return risposta

    except Exception as e:
        return f"Non sono riuscito ad analizzare la foto: {str(e)}"


def email_comune(nome_comune: str) -> str:
    key = nome_comune.strip().lower()
    if key in COMUNI_EMAIL:
        return COMUNI_EMAIL[key]
    return f"Email per '{nome_comune}' non trovata. Cercala su: https://www.comuni-italiani.it/"