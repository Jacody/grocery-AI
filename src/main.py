import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import time
import os
import concurrent.futures
from preprocess import load_departments, sort_by_store_order
from classifier import classify_product, classify_products_parallel

# 🔍 📂 **Verzeichnis korrekt bestimmen**
try:
    # Falls `__file__` existiert (nur in `.py`-Skripten)
    base_dir = os.path.dirname(os.path.abspath(__file__))  
except NameError:
    # Falls `__file__` nicht existiert (Jupyter Notebook)
    base_dir = os.getcwd()

# 🛒 **Abteilungen-Datei aus `data/`-Ordner**
abteilungen_path = os.path.join(base_dir, "../data/abteilungen.csv")

ABTEILUNGS_REIHENFOLGE = load_departments(abteilungen_path)

# 🔄 Vordefinierte Einkaufslisten für Tests
KURZE_LISTE = ["Milch", "Bananen", "Nudeln", "Mehl", "Tomatensoße", "Joghurt"]
LANGE_LISTE = [
    "Bananen", "Milch", "Brot", "Hackfleisch", "Nudeln", "Wasser", "Schokolade", "Tomaten",
    "Joghurt", "Croissants", "Cola", "Hähnchenbrust", "Mehl", "Apfelsaft", "Butter", "Käse",
    "Kekse", "Paprika", "Reis", "Erdbeeren"
]

def update_gui(message):
    """Fügt eine Nachricht zum GUI-Textfeld hinzu und aktualisiert die Anzeige."""
    result_text.insert(tk.END, message)
    result_text.see(tk.END)  # Automatisches Scrollen nach unten

def update_progress(total_products):
    """Aktualisiert den Fortschrittsbalken basierend auf der Anzahl der Produkte."""
    progress_bar["value"] += 100 / total_products
    root.update_idletasks()

def run_classification():
    """Startet die Klassifikation mit Live-Updates und Fortschrittsanzeige."""
    selection = list_option.get()

    if selection == "Kurze Liste":
        einkaufsliste = KURZE_LISTE
    elif selection == "Lange Liste":
        einkaufsliste = LANGE_LISTE
    else:
        produkte_eingabe = entry_products.get()
        if not produkte_eingabe.strip():
            messagebox.showwarning("Fehler", "Bitte eine Einkaufsliste eingeben oder eine vordefinierte Liste wählen.")
            return
        einkaufsliste = produkte_eingabe.strip().split()

    # GUI zurücksetzen und Startmeldung anzeigen
    result_text.delete("1.0", tk.END)
    update_gui("🛒 Starte Klassifikation...\n\n")
    progress_bar["value"] = 0

    start_time = time.time()

    # 🔄 Live-Klassifikation mit Zeitmessung
    def classification_task():
        klassifizierte_liste = {}
        for product in einkaufsliste:
            produkt, abteilung, elapsed_time = classify_product(product, ABTEILUNGS_REIHENFOLGE)
            klassifizierte_liste[produkt] = abteilung
            root.after(0, update_gui, f"[{elapsed_time:.2f} Sekunden] {produkt} → {abteilung}\n")

        sortierte_liste = sort_by_store_order(klassifizierte_liste, ABTEILUNGS_REIHENFOLGE)
        elapsed_time_total = time.time() - start_time

        root.after(0, update_gui, "\n✅ Einkaufsliste in Supermarkt-Reihenfolge:\n")
        for abteilung, produkte in sortierte_liste.items():
            root.after(0, update_gui, f"\n{abteilung}:\n")
            for produkt in produkte:
                root.after(0, update_gui, f"  - {produkt}\n")

        root.after(0, update_gui, f"\n⏳ Gesamte Verarbeitungszeit: {elapsed_time_total:.2f} Sekunden\n")

    concurrent.futures.ThreadPoolExecutor().submit(classification_task)

# 🖥️ GUI-Erstellung
root = tk.Tk()
root.title("Einkaufsliste Sortierer")
root.geometry("600x550")

tk.Label(root, text="Wähle eine Test-Einkaufsliste:").pack(pady=5)

# 📌 Dropdown-Menü für Testlisten
list_option = tk.StringVar(value="Eigene Liste eingeben")
dropdown = tk.OptionMenu(root, list_option, "Kurze Liste", "Lange Liste", "Eigene Liste eingeben")
dropdown.pack(pady=5)

# 📝 Eingabefeld für benutzerdefinierte Liste
entry_products = tk.Entry(root, width=60)
entry_products.pack(pady=5)

# ⏳ Fortschrittsbalken für die Verarbeitung
progress_bar = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
progress_bar.pack(pady=10)

# 🛠️ Button zum Starten der Klassifikation
tk.Button(root, text="Einkaufsliste sortieren", command=run_classification).pack(pady=5)

# 📜 Textfeld zur Anzeige der Ergebnisse mit Scroll-Funktion
result_text = scrolledtext.ScrolledText(root, height=20, width=70)
result_text.pack(pady=10)

# 🚀 GUI starten
root.mainloop()
