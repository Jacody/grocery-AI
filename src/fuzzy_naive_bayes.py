#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
import time
from difflib import get_close_matches


# Daten laden
file_produkte = "data/produkte abteilungen.csv"
df = pd.read_csv(file_produkte)


# In[2]:


# Trainingsdaten vorbereiten
X_train = df["Produkt"]
y_train = df["Abteilung"]
#print(X_train)
#print(y_train)


# In[3]:


# Text in numerische Features umwandeln
vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
#print(vectorizer)
#print(X_train_vec)


# In[4]:


# Naive Bayes Modell trainieren
model = MultinomialNB()
model.fit(X_train_vec, y_train)

#print(model.fit(X_train_vec, y_train))


# In[5]:


# Funktion für Fuzzy-Suche
def fuzzy_search(food_list, keyword, cutoff=0.8):
    matches = get_close_matches(keyword, food_list, n=1, cutoff=cutoff)
    return matches[0] if matches else keyword  # Gibt das beste Match zurück oder das Originalwort
    

# Funktion zur Vorhersage der Abteilung mit Wahrscheinlichkeitsbewertung
def predict_abteilung(produktname):
    produktname = fuzzy_search(X_train, produktname)
    X_test_vec = vectorizer.transform([produktname])
    probabilities = model.predict_proba(X_test_vec)
    predicted_class = model.classes_[probabilities.argmax()]
    confidence = probabilities.max()
    return predicted_class, confidence
#print(predict_abteilung("Bananen"))


# In[6]:


# Funktion zur Klassifikation einer Liste von Produkten mit Zeitmessung
def classify_products(einkaufsliste):
    klassifizierte_liste = {}
    start_time = time.time()
    
    for produkt in einkaufsliste:
        start_time_product = time.time()
        abteilung, confidence = predict_abteilung(produkt)
        if confidence <= 0.08:
            abteilung = "Unbestimmt"
        elapsed_time = time.time() - start_time_product
        klassifizierte_liste[produkt] = (abteilung, confidence, elapsed_time)
        #print(f"[{elapsed_time:.2f} Sekunden] {produkt} → {abteilung} (Sicherheit: {confidence:.2%})")
    
    elapsed_time_total = time.time() - start_time
    #print(f"\n⏳ Gesamte Verarbeitungszeit: {elapsed_time_total:.2f} Sekunden\n")
    return klassifizierte_liste


# In[7]:


# Beispiel-Liste
#KURZE_LISTE = ["Milch", "Bananen", "Nudeln", "Mehl", "Tomatensoße", "Joghurt"]
#classified = classify_products(KURZE_LISTE)

