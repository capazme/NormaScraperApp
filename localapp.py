import datetime
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import tkinter as tk
from tkinter import messagebox, scrolledtext
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urn import get_urn_and_extract_data

def fetch_act_data():
    act_type = act_type_entry.get()
    date = date_entry.get()
    act_number = act_number_entry.get()
    article = article_entry.get()
    extension = ''
    if "-" in article: #se l'interprete non dovesse cogliere l'estensione come parametro aggiuntivo
            parts = article.split("-")
            article = parts[0]
            extension = parts[1]
    extension = extension_entry.get()
    version = version_var.get()
    version_date = version_date_entry.get()
    comma = comma_entry.get()
    
    # Configura il WebDriver qui (es. Chrome, Firefox, etc.)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Imposta la modalità headless
    chrome_options.add_argument("--disable-gpu")  # Raccomandato per eseguire in modalità headless
    chrome_options.add_argument("--window-size=1920x1080")  # Opzionale, imposta la risoluzione del browser

    driver = webdriver.Chrome(options=chrome_options)

    try:
        data = get_urn_and_extract_data(driver, act_type, date, act_number, article, extension, comma, version, version_date)
        if data:
            # Aggiorna il widget di testo con i dati recuperati
            output_text.delete('1.0', tk.END)  # Pulisce il widget di testo prima di inserire nuovi dati
            output_text.insert(tk.END, data)  # Inserisce i dati nel widget di testo
        else:
            messagebox.showerror("Errore", "Impossibile estrarre i dati.")
    except Exception as e:
        messagebox.showerror("Errore", f"Si è verificato un errore: {e}")
    finally:
        driver.quit()

# Inizializza la finestra principale
root = tk.Tk()
root.title("Estrattore dati Normattiva")

# Crea e organizza gli elementi dell'interfaccia
tk.Label(root, text="Tipo atto:").grid(row=0, column=0)
act_type_entry = tk.Entry(root)
act_type_entry.grid(row=0, column=1)
act_type_entry.insert(0, "legge")  # Valore di default per il tipo di atto

tk.Label(root, text="Data (YYYY-MM-DD o esteso):").grid(row=1, column=0)
date_entry = tk.Entry(root)
date_entry.grid(row=1, column=1)
date_entry.insert(0, "7 agosto 1990")  # Valore di default per la data

tk.Label(root, text="Numero atto:").grid(row=2, column=0)
act_number_entry = tk.Entry(root)
act_number_entry.grid(row=2, column=1)
act_number_entry.insert(0, "241")  # Valore di default per il numero di atto

tk.Label(root, text="Articolo:").grid(row=3, column=0)
article_entry = tk.Entry(root)
article_entry.grid(row=3, column=1)
#article_entry.insert(0, "2")  # Valore di default per l'articolo

tk.Label(root, text="Estensione articolo:").grid(row=4, column=0)
extension_entry = tk.Entry(root)
extension_entry.grid(row=4, column=1)
#extension_entry.insert(0, "bis")  # Valore di default per l'estensione articolo

tk.Label(root, text="Comma:").grid(row=5, column=0)
comma_entry = tk.Entry(root)
comma_entry.grid(row=5, column=1)

tk.Label(root, text="Versione:").grid(row=6, column=0)
version_var = tk.StringVar(value="vigente")  # 'originale' è già impostato come valore di default
tk.Radiobutton(root, text="Originale", variable=version_var, value="originale").grid(row=6, column=1)
tk.Radiobutton(root, text="Vigente", variable=version_var, value="vigente").grid(row=6, column=2)

tk.Label(root, text="Data versione vigente:").grid(row=7, column=0)
version_date_entry = tk.Entry(root)
version_date_entry.grid(row=7, column=1)
#version_date_entry.insert(0, "2023-01-01")  # Valore di default per la data della versione vigente

# Bottoni
fetch_button = tk.Button(root, text="Estrai dati", command=fetch_act_data)
fetch_button.grid(row=8, column=0, columnspan=3)

# Widget di testo per l'output
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=130, height=110)
output_text.grid(row=9, column=0, columnspan=3, pady=10)

root.mainloop()