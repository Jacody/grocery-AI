Grocery-AI

Ein KI-gestütztes Einkaufsliste-Tool mit intelligenter Kategorisierung von Produkten.

Installation

1. Virtuelle Umgebung erstellen

Bevor du das Projekt installierst, erstelle eine virtuelle Umgebung:

python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

2. Abhängigkeiten installieren

Empfohlene Installation (nur Hauptabhängigkeiten):

pip install -r requirements_clean.txt

Komplette Installation (exakte Umgebung mit allen Paketen):

pip install -r requirements.txt

3. Falls tkinter fehlt

Das Projekt benötigt tkinter, welches standardmäßig in Python enthalten ist. Falls es fehlt:

Ubuntu/Debian:

sudo apt install python3-tk

Mac (Homebrew):

brew install python-tk

Windows: Ist in der Regel vorinstalliert.

Nutzung

Starte die Anwendung mit:

python main.py

Projektstruktur

Grocery-AI/
│-- main.py            # Hauptprogramm
│-- requirements.txt   # Alle Abhängigkeiten
│-- requirements_clean.txt # Nur notwendige Pakete
│-- README.md          # Diese Datei
│-- src/               # Quellcode
│-- data/              # Beispiel-Daten (falls vorhanden)

Mitwirken

Pull Requests sind willkommen! Stelle sicher, dass du Änderungen in einem separaten Branch erstellst und eine klare Beschreibung hinzufügst.

Lizenz

Dieses Projekt steht unter der MIT-Lizenz.