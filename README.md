# 🌿 EcoScan — Bot Telegram per il Decoro Urbano

EcoScan è un bot Telegram che permette ai cittadini di segnalare problemi di sporcizia urbana inviando una foto. L'intelligenza artificiale analizza l'immagine, valuta la gravità e salva la segnalazione in un file JSON consultabile dal comune tramite una dashboard grafica.

---

## 📋 Funzionalità

- 📸 **Analisi foto** — il bot riceve una foto e la classifica in tre livelli di gravità
- 📍 **Segnalazione via** — solo in caso di gravità massima, chiede all'utente dove si trova il problema
- 📊 **Dashboard comune** — interfaccia grafica per visualizzare tutte le segnalazioni e scegliere dove salvarle
- 📧 **Email comune** — comando `/email` per ottenere il contatto del comune di riferimento

---

## 🗂️ Struttura del progetto

```
EcoScan/
│
├── src/
│   ├── main.py              # Avvia il bot
│   ├── bot.py               # Gestisce i messaggi Telegram
│   ├── ai_service.py        # Logica IA (analisi foto, email comune)
│   └── segnalazioni.py      # Lettura e scrittura del file JSON
│
├── comune_dashboard.py      # GUI per il comune
├── .env                     # Token Telegram (non committare!)
├── requirements.txt         # Dipendenze
└── README.md
```

---

## ⚙️ Requisiti

- Python 3.10 o superiore
- [Ollama](https://ollama.com) installato e in esecuzione
- Un bot Telegram creato tramite [@BotFather](https://t.me/BotFather)

---

## 🚀 Installazione

### 1. Clona il repository

```bash
git clone https://github.com/tuo-utente/ecoscan.git
cd ecoscan
```

### 2. Crea un ambiente virtuale

```bash
python -m venv .venv

# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Installa le dipendenze

```bash
pip install -r requirements.txt
```

### 4. Installa il modello IA

Assicurati di avere [Ollama](https://ollama.com/download) installato, poi esegui:

```bash
ollama pull llama3.2-vision
```

### 5. Crea il file `.env`

Nella root del progetto crea un file `.env`:

```env
TELEGRAM_TOKEN=il_tuo_token_qui
```

Per ottenere il token:
1. Apri Telegram e cerca **@BotFather**
2. Scrivi `/newbot` e segui le istruzioni
3. Copia il token e incollalo nel file `.env`

---

## ▶️ Avvio

### Avviare il bot

```bash
cd src
python main.py
```

### Avviare la dashboard del comune

In un terminale separato, dalla root del progetto:

```bash
python comune_dashboard.py
```

---

## 🤖 Comandi del bot

| Comando | Descrizione |
|---|---|
| `/start` | Mostra il messaggio di benvenuto e i comandi |
| `/comandi` | Mostra l'elenco dei comandi |
| `/email` | Chiede il comune e restituisce l'email di contatto |
| `/segnalazioni` | Mostra il riepilogo delle segnalazioni ricevute |
| 📸 Invia una foto | Analizza la sporcizia e salva la segnalazione |

---

## 📊 Livelli di gravità

| Livello | Descrizione |
|---|---|
| 🔴 MASSIMA | Sacchetti, mobili abbandonati, cumuli di rifiuti. Chiede la via. |
| 🟡 MEDIA | Qualche rifiuto piccolo, sporco localizzato |
| 🟢 MINIMA | Strada pulita o quasi pulita |

---


## 🔒 Note di sicurezza

- Non committare mai il file `.env` su GitHub
- Aggiungi `.env` al `.gitignore`:

```
.env
config.json
segnalazioni.json
__pycache__/
.venv/
```

---

## 📬 Contatti

Progetto sviluppato per migliorare il decoro urbano e semplificare le segnalazioni dei cittadini ai comuni italiani.
