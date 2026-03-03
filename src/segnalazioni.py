import json
import os
from datetime import datetime

FILE = "segnalazioni.json"

def carica_segnalazioni():
    if not os.path.exists(FILE):
        return []
    with open(FILE, 'r') as f:
        return json.load(f)

def salva_segnalazione(via: str, gravita: str, analisi: str, foto_path: str, user_id: int):
    segnalazioni = carica_segnalazioni()
    segnalazione = {
        "id": len(segnalazioni) + 1,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "via": via,
        "gravita": gravita,
        "analisi": analisi,
        "foto": foto_path,
        "user_id": user_id,
        "stato": "APERTA" 
    }
    segnalazioni.append(segnalazione)
    with open(FILE, 'w') as f:
        json.dump(segnalazioni, f, indent=2, ensure_ascii=False)
    return segnalazione["id"]

def get_riepilogo() -> str:
    segnalazioni = carica_segnalazioni()
    if not segnalazioni:
        return "Nessuna segnalazione presente."
    
    testo = f"📊 <b>Totale segnalazioni: {len(segnalazioni)}</b>\n\n"
    for s in reversed(segnalazioni):
        emoji = "🔴" if s["gravita"] == "MASSIMA" else "🟡" if s["gravita"] == "MEDIA" else "🟢"
        testo += (
            f"{emoji} <b>#{s['id']}</b> — {s['data']}\n"
            f"📍 {s['via']}\n"
            f"⚠️ Gravità: {s['gravita']} | Stato: {s['stato']}\n\n"
        )
    return testo