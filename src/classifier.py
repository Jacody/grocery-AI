import ollama
import time
import concurrent.futures

def classify_product(product, abteilungs_reihenfolge):
    """Klassifiziert ein Produkt in eine Supermarkt-Abteilung."""
    start_time = time.time()

    prompt = f"""
    Welcher Supermarkt-Abteilung gehört '{product}' an? Gib nur eine der folgenden Kategorien aus:
    {", ".join(abteilungs_reihenfolge)}.
    """

    response = ollama.chat(model="gemma", messages=[{"role": "user", "content": prompt}])
    abteilung = response['message']['content'].strip()

    if abteilung not in abteilungs_reihenfolge:
        abteilung = "Sonstige"

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
