import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import webbrowser
import pyperclip
from urn import get_urn_and_extract_data
class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        if self.tooltip_window:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 20
        y += self.widget.winfo_rooty() + 20
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tooltip_window, text=self.text, background="lightyellow", borderwidth=1, relief="solid")
        label.pack(ipadx=1, ipady=1)
    
    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
            
class NormaScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NormaScraper - Beta")
        self.setup_style()
        self.create_widgets()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Helvetica', 10))
        style.configure('TEntry', padding=5)
        style.configure('TLabel', font=('Helvetica', 10))
        style.configure('TRadiobutton', font=('Helvetica', 10))
        style.configure('Tooltip.TLabel', background='lightyellow', font=('Helvetica', 8))

    def create_widgets(self):
        self.mainframe = ttk.Frame(self.root, padding="5")
        self.mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        # Input fields
        self.act_type_entry = self.create_labeled_entry("Tipo atto:", "Inserisci il tipo di atto", 0, 0)
        self.date_entry = self.create_labeled_entry("Data (YYYY-MM-DD, esteso o solo anno):", "Inserisci il tipo di atto", 1, 0)
        self.act_number_entry = self.create_labeled_entry("Numero atto:", "Inserisci il tipo di atto", 2, 0)
        self.article_entry = self.create_labeled_entry("Articolo:", "Inserisci il tipo di atto", 3, 0)
        self.extension_entry = self.create_labeled_entry("Estensione:", "Inserisci il tipo di atto", 4, 0)
        self.comma_entry = self.create_labeled_entry("Comma:", "Inserisci il tipo di atto", 5, 0)

        # Version radio buttons
        tk.Label(self.mainframe, text="Versione:").grid(row=6, column=0)
        self.version_var = tk.StringVar(value="vigente")
        tk.Radiobutton(self.mainframe, text="Originale", variable=self.version_var, value="originale").grid(row=6, column=1)
        tk.Radiobutton(self.mainframe, text="Vigente", variable=self.version_var, value="vigente").grid(row=6, column=2)

        self.version_date_entry = self.create_labeled_entry("Data versione atto (se applicabile):", "Inserisci la data di versione dell'atto se disponibile", 7, 0)

        # Buttons
        fetch_button = tk.Button(self.mainframe, text="Estrai dati", command=self.fetch_act_data)
        fetch_button.grid(row=8, column=0, columnspan=3)
        save_xml_button = tk.Button(self.mainframe, text="Salva come XML", command=self.save_as_xml)
        save_xml_button.grid(row=8, column=1, columnspan=3)
        clear_button = tk.Button(self.mainframe, text="Cancella", command=lambda: self.clear_all_fields([self.act_type_entry, self.date_entry, self.act_number_entry, self.article_entry, self.extension_entry, self.comma_entry, self.version_date_entry]))
        clear_button.grid(row=8, column=2)
        copia_button = tk.Button(self.mainframe, text="Copia Testo", command=self.copia_output)
        copia_button.grid(row=9, column=0)

        self.output_text = scrolledtext.ScrolledText(self.mainframe, wrap=tk.WORD, width=130, height=30)
        self.output_text.grid(row=10, column=0, columnspan=3, pady=10)

    def create_labeled_entry(self, label_text, tooltip_text, row, col):
        ttk.Label(self.mainframe, text=label_text).grid(row=row, column=col, sticky=tk.W)
        entry = ttk.Entry(self.mainframe)
        entry.grid(row=row, column=col+1, sticky=(tk.W, tk.E), padx=2, pady=2)
        Tooltip(entry, tooltip_text)
        return entry

    def copia_output(self):
        content = self.output_text.get("1.0", tk.END)
        pyperclip.copy(content)
        messagebox.showinfo("Copia", "Testo copiato negli appunti!")

    def apri_url(self, url):
        webbrowser.open_new_tab(url)

    def clear_all_fields(self, entries):
        for entry in entries:
            entry.delete(0, tk.END)

    def save_as_xml(self):
        file_path = filedialog.asksaveasfilename(
            title="Salva come XML",
            initialdir="/",
            filetypes=[("XML files", "*.xml")],
            defaultextension=".xml"
        )
        if file_path:
            self.fetch_act_data(save_xml_path=file_path)

    def fetch_act_data(self, save_xml_path=None):
        act_type = self.act_type_entry.get()
        date = self.date_entry.get()
        act_number = self.act_number_entry.get()
        article = self.article_entry.get()
        extension = self.extension_entry.get()
        version = self.version_var.get()
        version_date = self.version_date_entry.get()
        comma = self.comma_entry.get()
        
        try:
            data, url = get_urn_and_extract_data(act_type, date, act_number, article, extension, comma, version, version_date, save_xml_path=save_xml_path)
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, data)
            self.crea_link("Apri URN Normattiva", url, 9, 1)
        except Exception as e:
            messagebox.showerror("Errore", str(e))

    def crea_link(self, text, url, row, column):
        link = tk.Label(self.mainframe, text=text, fg="blue", cursor="hand2")
        link.bind("<Button-1>", lambda e: self.apri_url(url))
        link.grid(row=row, column=column)

if __name__ == "__main__":
    root = tk.Tk()
    app = NormaScraperApp(root)
    root.mainloop()
