import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
from datetime import datetime

CONFIG_FILE = "config.json"

# ─── CONFIG ───────────────────────────────────────────────────────────────────

def get_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"cartella": os.getcwd()}

def salva_config(cartella: str):
    with open(CONFIG_FILE, 'w') as f:
        json.dump({"cartella": cartella}, f)

def get_file_segnalazioni():
    config = get_config()
    return os.path.join(config["cartella"], "segnalazioni.json")

def carica_segnalazioni():
    path = get_file_segnalazioni()
    if not os.path.exists(path):
        return []
    with open(path, 'r') as f:
        return json.load(f)

# ─── GUI ──────────────────────────────────────────────────────────────────────

class ComuneDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EcoScan — Dashboard Comune")
        self.geometry("820x600")
        self.resizable(False, False)
        self.configure(bg="#0f1923")

        self._build_header()
        self._build_cartella_section()
        self._build_segnalazioni_section()
        self._aggiorna_lista()

    # ── Header ────────────────────────────────────────────────────────────────

    def _build_header(self):
        frame = tk.Frame(self, bg="#0f1923")
        frame.pack(fill="x", padx=24, pady=(20, 0))

        tk.Label(
            frame, text="🌿 EcoScan", font=("Georgia", 22, "bold"),
            fg="#4ecca3", bg="#0f1923"
        ).pack(side="left")

        tk.Label(
            frame, text="Dashboard Comune",
            font=("Georgia", 12), fg="#8899aa", bg="#0f1923"
        ).pack(side="left", padx=(10, 0), pady=(8, 0))

        self.lbl_data = tk.Label(
            frame, text=datetime.now().strftime("%d/%m/%Y %H:%M"),
            font=("Courier", 10), fg="#8899aa", bg="#0f1923"
        )
        self.lbl_data.pack(side="right", pady=(8, 0))

        tk.Frame(self, bg="#1e2d3d", height=1).pack(fill="x", padx=24, pady=12)

    # ── Sezione cartella ──────────────────────────────────────────────────────

    def _build_cartella_section(self):
        frame = tk.Frame(self, bg="#0f1923")
        frame.pack(fill="x", padx=24, pady=(0, 12))

        tk.Label(
            frame, text="📁  Cartella salvataggio segnalazioni",
            font=("Georgia", 11, "bold"), fg="#e0e8f0", bg="#0f1923"
        ).pack(anchor="w")

        row = tk.Frame(frame, bg="#0f1923")
        row.pack(fill="x", pady=(6, 0))

        self.var_cartella = tk.StringVar(value=get_config()["cartella"])

        entry = tk.Entry(
            row, textvariable=self.var_cartella,
            font=("Courier", 10), bg="#1e2d3d", fg="#4ecca3",
            insertbackground="#4ecca3", relief="flat",
            bd=0, highlightthickness=1, highlightcolor="#4ecca3",
            highlightbackground="#2a3f55"
        )
        entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 8))

        tk.Button(
            row, text="Sfoglia", command=self._scegli_cartella,
            bg="#1e2d3d", fg="#4ecca3", font=("Georgia", 10),
            relief="flat", cursor="hand2", padx=12, pady=4,
            activebackground="#2a3f55", activeforeground="#4ecca3"
        ).pack(side="left", padx=(0, 6))

        tk.Button(
            row, text="Salva", command=self._salva_cartella,
            bg="#4ecca3", fg="#0f1923", font=("Georgia", 10, "bold"),
            relief="flat", cursor="hand2", padx=12, pady=4,
            activebackground="#3ab88d", activeforeground="#0f1923"
        ).pack(side="left")

        tk.Frame(self, bg="#1e2d3d", height=1).pack(fill="x", padx=24, pady=12)

    def _scegli_cartella(self):
        cartella = filedialog.askdirectory(title="Scegli cartella")
        if cartella:
            self.var_cartella.set(cartella)

    def _salva_cartella(self):
        cartella = self.var_cartella.get().strip()
        if not cartella:
            messagebox.showerror("Errore", "Inserisci un percorso valido.")
            return
        os.makedirs(cartella, exist_ok=True)
        salva_config(cartella)
        messagebox.showinfo("✅ Salvato", f"Cartella impostata:\n{cartella}")
        self._aggiorna_lista()

    # ── Sezione segnalazioni ──────────────────────────────────────────────────

    def _build_segnalazioni_section(self):
        header = tk.Frame(self, bg="#0f1923")
        header.pack(fill="x", padx=24)

        tk.Label(
            header, text="📋  Segnalazioni ricevute",
            font=("Georgia", 11, "bold"), fg="#e0e8f0", bg="#0f1923"
        ).pack(side="left")

        tk.Button(
            header, text="⟳ Aggiorna", command=self._aggiorna_lista,
            bg="#1e2d3d", fg="#4ecca3", font=("Georgia", 9),
            relief="flat", cursor="hand2", padx=10, pady=2,
            activebackground="#2a3f55", activeforeground="#4ecca3"
        ).pack(side="right")

        # Tabella
        frame = tk.Frame(self, bg="#0f1923")
        frame.pack(fill="both", expand=True, padx=24, pady=(8, 0))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Custom.Treeview",
            background="#13202e", foreground="#c8d8e8",
            fieldbackground="#13202e", rowheight=28,
            font=("Courier", 10)
        )
        style.configure(
            "Custom.Treeview.Heading",
            background="#1e2d3d", foreground="#4ecca3",
            font=("Georgia", 10, "bold"), relief="flat"
        )
        style.map("Custom.Treeview", background=[("selected", "#2a3f55")])

        cols = ("#", "Data", "Via", "Gravità", "Stato")
        self.tree = ttk.Treeview(
            frame, columns=cols, show="headings",
            style="Custom.Treeview", height=14
        )

        for col, w in zip(cols, [40, 130, 280, 90, 100]):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center" if col in ("#", "Gravità", "Stato") else "w")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Stats bar
        self.lbl_stats = tk.Label(
            self, text="", font=("Courier", 9),
            fg="#8899aa", bg="#0f1923"
        )
        self.lbl_stats.pack(pady=(6, 12))

    def _aggiorna_lista(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        segnalazioni = carica_segnalazioni()
        massima = media = minima = 0

        for s in reversed(segnalazioni):
            g = s.get("gravita", "?")
            if g == "MASSIMA":
                emoji, massima = "🔴", massima + 1
            elif g == "MEDIA":
                emoji, media = "🟡", media + 1
            else:
                emoji, minima = "🟢", minima + 1

            self.tree.insert("", "end", values=(
                f"#{s.get('id', '?')}",
                s.get("data", ""),
                s.get("via", ""),
                f"{emoji} {g}",
                s.get("stato", "APERTA")
            ))

        totale = len(segnalazioni)
        self.lbl_stats.config(
            text=f"Totale: {totale}   🔴 Massima: {massima}   🟡 Media: {media}   🟢 Minima: {minima}"
        )


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = ComuneDashboard()
    app.mainloop()