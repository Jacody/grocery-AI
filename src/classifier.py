import ollama
import time
import concurrent.futures
import difflib
from preprocess import sort_by_store_order

def classify_product(product, abteilungs_reihenfolge):
    """Klassifiziert ein Produkt in eine Supermarkt-Abteilung und stellt sicher, dass die Ausgabe exakt der CSV entspricht."""
    start_time = time.time()

    prompt = f"""
    Welcher Supermarkt-Abteilung gehört '{product}' an? Wähle exakt eine der folgenden Kategorien aus:
    {", ".join(abteilungs_reihenfolge)}.
    Gib nur den Namen der Abteilung als Antwort aus, ohne zusätzliche Erklärungen oder Formatierungen.
    """

    response = ollama.chat(model="gemma", messages=[{"role": "user", "content": prompt}])
    abteilung = response['message']['content'].strip()

    # **Bereinigung von unerwünschten Zeichen**
    abteilung = abteilung.replace("*", "").replace("\"", "").strip()

    # **Stelle sicher, dass die Abteilung exakt in der CSV existiert**
    if abteilung not in abteilungs_reihenfolge:
        abteilung = difflib.get_close_matches(abteilung, abteilungs_reihenfolge, n=1, cutoff=0.6)
        abteilung = abteilung[0] if abteilung else "Sonstige"

    elapsed_time = time.time() - start_time
    return product, abteilung, elapsed_time

def classify_products_parallel(product_list, abteilungs_reihenfolge, max_workers=6):
    """Klassifiziert eine Einkaufsliste parallel."""
    product_dict = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(lambda p: classify_product(p, abteilungs_reihenfolge), product_list)

    for product, abteilung, _ in results:
        product_dict[product] = abteilung

    return product_dict

def classification_task(einkaufsliste, vorhersagen, abteilungs_reihenfolge, update_gui, update_progress, root, start_time):
    """Klassifiziert zuerst sicher zugeordnete Produkte, dann 'Unbestimmt'-Produkte separat."""
    klassifizierte_liste = {}
    unbestimmte_produkte = []
    total_products = len(einkaufsliste)

    # **Zuerst alle sicher zugeordneten Produkte ausgeben (OHNE ZEIT)**
    for produkt in einkaufsliste:
        abteilung, confidence, _ = vorhersagen[produkt]

        if abteilung.lower() != "unbestimmt":
            # Produkt wurde mit hoher Sicherheit klassifiziert
            klassifizierte_liste[produkt] = abteilung
            root.after(0, update_gui, f"{produkt} → {abteilung}\n")  # ⏳ KEINE ZEITANGABE MEHR
        else:
            # Produkt wurde als "Unbestimmt" erkannt → später mit KI klassifizieren
            unbestimmte_produkte.append(produkt)

        root.after(0, update_progress, total_products)

    # **Jetzt alle 'Unbestimmt'-Produkte mit der KI klassifizieren (MIT ZEIT)**
    if unbestimmte_produkte:
        root.after(0, update_gui, "\n🔍 Unbestimmte Produkte werden nun mit der KI klassifiziert...\n")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(lambda p: classify_product(p, abteilungs_reihenfolge), unbestimmte_produkte)

        for produkt, abteilung, elapsed_time in results:
            klassifizierte_liste[produkt] = abteilung
            root.after(0, update_gui, f"🔍 KI-Check: {produkt} → {abteilung} ({elapsed_time:.2f} Sekunden)\n")
            root.after(0, update_progress, total_products)

    # **Sortierte Ausgabe der finalen Einkaufsliste**
    sortierte_liste = sort_by_store_order(klassifizierte_liste, abteilungs_reihenfolge)
    elapsed_time_total = time.time() - start_time

    root.after(0, update_gui, "\n✅ Vollständige Einkaufsliste in Supermarkt-Reihenfolge:\n")
    for abteilung, produkte in sortierte_liste.items():
        root.after(0, update_gui, f"\n{abteilung}:\n")
        for produkt in produkte:
            root.after(0, update_gui, f"  - {produkt}\n")

    root.after(0, update_gui, f"\n⏳ Gesamte Verarbeitungszeit: {elapsed_time_total:.2f} Sekunden\n")
