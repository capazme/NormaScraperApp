import tkinter as tk
import webbrowser
from tkinter import messagebox, scrolledtext, Scrollbar, filedialog
from urn import get_urn_and_extract_data

def apri_url(url):
    webbrowser.open(url, new=2)
    
def crea_link(ui, text, url, row, column):
    link = tk.Label(ui, text=text, fg="blue", cursor="hand2")
    link.bind("<Button-1>", lambda e: apri_url(url))
    link.grid(row=row, column=column)  # Usa grid con parametri row e column
    return link

def clear_all_fields():
    # Imposta il contenuto di ogni Entry a una stringa vuota o a un valore predefinito
    act_type_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    act_number_entry.delete(0, tk.END)
    article_entry.delete(0, tk.END)
    extension_entry.delete(0, tk.END)
    version_date_entry.delete(0, tk.END)
    comma_entry.delete(0, tk.END)
    # Assicurati di aggiungere qui il codice per resettare eventuali altri campi che potresti avere.

def save_as_xml():
    save_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
    if save_path:
        # Chiamata alla funzione modificata con il nuovo parametro del percorso di salvataggio
        fetch_act_data(save_xml_path=save_path)

def fetch_act_data(save_xml_path=None):
    act_type = act_type_entry.get()
    date = date_entry.get()
    act_number = act_number_entry.get()
    article = article_entry.get()
    extension = extension_entry.get()
    version = version_var.get()
    version_date = version_date_entry.get()
    comma = comma_entry.get()
    
    try:
        data = get_urn_and_extract_data(act_type, date, act_number, article, extension, comma, version, version_date, save_xml_path=save_xml_path)
        if data:
            # Aggiorna il widget di testo con i dati recuperati
            output_text.delete('1.0', tk.END)  # Pulisce il widget di testo prima di inserire nuovi dati
            output_text.insert(tk.END, str(data[0]))  # Inserisce i dati nel widget di testo
            crea_link(root, "Apri URN Normattiva", data[1], 9, 0)
            pass
    except Exception as e:
        messagebox.showerror("Errore", f"Si è verificato un errore: {e}")
    

# Inizializza la finestra principale
root = tk.Tk()
root.title("NormaScraper v2")

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

save_xml_button = tk.Button(root, text="Salva come XML", command=save_as_xml)
save_xml_button.grid(row=8, column=1, columnspan=3)

clear_button = tk.Button(root, text="Cancella", command=clear_all_fields)
clear_button.grid(row=8, column=2)  # Modifica il valore di row e column secondo le tue necessità


# Widget di testo per l'output
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=130, height=30)
output_text.grid(row=10, column=0, columnspan=3, pady=10)





root.mainloop()