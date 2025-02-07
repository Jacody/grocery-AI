import pandas as pd

def load_departments(csv_file):
    """Lädt die Supermarkt-Abteilungen aus einer CSV-Datei."""
    df = pd.read_csv(csv_file)
    return df["Abteilung"].tolist()

def sort_by_store_order(product_dict, abteilungs_reihenfolge):
    """Sortiert die Einkaufsliste nach der Reihenfolge der Abteilungen im Supermarkt."""
    sorted_products = {}

    for abteilung in abteilungs_reihenfolge + ["Sonstige"]:
        items = [produkt for produkt, kat in product_dict.items() if kat == abteilung]
        if items:
            sorted_products[abteilung] = items  

    return sorted_products
