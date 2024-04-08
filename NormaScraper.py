import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog, Menu
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
        self.create_menu()
        self.root.bind('<Control-i>', lambda event: self.increase_text_size())
        self.root.bind('<Control-d>', lambda event: self.decrease_text_size())
        self.root.bind('<Control-h>', lambda event: self.apply_high_contrast_theme())
        self.root.bind('<Control-n>', lambda event: self.apply_normal_theme())
        self.create_widgets()

    def setup_style(self):
        self.style = ttk.Style()
        self.style.theme_use('alt')  # A theme better suited for accessibility
        self.style.configure('TButton', font=('Helvetica', 12), foreground='black', background='white')
        self.style.configure('TEntry', padding=5, font=('Helvetica', 12))
        self.style.configure('TLabel', font=('Helvetica', 12))
        # Accessibility: High contrast theme configurations
        self.style.configure('HighContrast.TButton', font=('Helvetica', 12), foreground='yellow', background='black')

    def create_widgets(self):
        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.grid_columnconfigure(0, weight=1)  
        self.root.grid_rowconfigure(0, weight=1)  
        self.mainframe.columnconfigure(0, weight=1)  
        self.mainframe.rowconfigure(10, weight=1)  


        # Input fields
        self.act_type_entry = self.create_labeled_entry("Tipo atto:", """
Inserisci il tipo di atto generico (legge, decreto-legge, decreto legislativo) o un atto specifico tra quelli elencati (o una sua abbraviazione): 
Costituzione (costituzione, cost, cost., c.)
Codice Civile (cc, c.c., codice civile, cod. civ., disp. att. c.c.)
Preleggi (disp. prel., preleggi, prel.)
Codice Penale (cp, c.p., cod. pen.)
Codice di Procedura Civile (cpc, c.p.c., cod. proc. civ., disp. att. c.p.c.)
Codice di Procedura Penale (cpp, c.p.p., cod. proc. pen.)
Codice della Navigazione (cn, cod. nav.)
Codice Postale e delle Telecomunicazioni (cpet, cod. post. telecom.)
Codice della Strada (cds, cod. strada)
Codice del Processo Tributario (cpt, cod. proc. trib.)
Codice in Materia di Protezione dei Dati Personali (cpd, cod. prot. dati)
Codice delle Comunicazioni Elettroniche (cce, cod. com. elet.)
Codice dei Beni Culturali e del Paesaggio (cbc, cod. beni cult.)
Codice della Proprietà Industriale (cpi, cod. prop. ind.)
Codice dell'Amministrazione Digitale (cad, cod. amm. dig.)
Codice della Nautica da Diporto (cnd, cod. naut. diport.)
Codice del Consumo (cdc, cod. consumo)
Codice delle Assicurazioni Private (cap, cod. ass. priv.)
Norme in Materia Ambientale (camb, norme amb.)
Codice dei Contratti Pubblici (ccp, cod. contr. pubb.)
Codice delle Pari Opportunità (cpo, cod. pari opp.)
Codice dell'Ordinamento Militare (com, cod. ord. mil.)
Codice del Processo Amministrativo (cpa, cod. proc. amm.)
Codice del Turismo (ctu, cod. turismo)
Codice Antimafia (cam, cod. antimafia)
Codice di Giustizia Contabile (cgco, cod. giust. cont.)
Codice del Terzo Settore (cts, cod. ter. sett.)
Codice della Protezione Civile (cdpc, cod. prot. civ.)
Codice della Crisi d'Impresa e dell'Insolvenza (cci, cod. crisi imp.)
 """, 0, 0)
        self.date_entry = self.create_labeled_entry("Data:", "Inserisci la data in formato YYYY-MM-DD, per esteso o solo anno (inserire solo l'anno comporterà un caricamento più lungo)", 1, 0)
        self.act_number_entry = self.create_labeled_entry("Numero atto:", "Inserisci il numero dell'atto (obbligatorio se il tipo di atto è generico)", 2, 0)
        self.article_entry = self.create_labeled_entry("Articolo:", "Inserisci l'articolo, con eventuale estensione con trattino (-bis, -tris etc...)", 3, 0)
        self.extension_entry = self.create_labeled_entry("Estensione:", "Inserisci l'estensione (bis, tris etc...)", 4, 0)
        self.comma_entry = self.create_labeled_entry("Comma:", "Inserisci il comma, con eventuale estensione con trattino (-bis, -tris etc...) ", 5, 0)

        # Version radio buttons
        ttk.Label(self.mainframe, text="Versione:").grid(row=6, column=0, sticky=tk.W)
        self.version_var = tk.StringVar(value="vigente")
        ttk.Radiobutton(self.mainframe, text="Originale", variable=self.version_var, value="originale").grid(row=6, column=1, sticky=tk.W)
        ttk.Radiobutton(self.mainframe, text="Vigente", variable=self.version_var, value="vigente").grid(row=6, column=2, sticky=tk.W)



        self.version_date_entry = self.create_labeled_entry("Data versione atto (se non originale):", "Inserisci la data di versione dell'atto desiderata (default alla data corrente)", 7, 0)

        # Buttons
        fetch_button = ttk.Button(self.mainframe, text="Estrai dati", command=self.fetch_act_data)
        fetch_button.grid(row=8, column=0)
        save_xml_button = ttk.Button(self.mainframe, text="Salva come XML", command=self.save_as_xml)
        save_xml_button.grid(row=8, column=1)
        clear_button = ttk.Button(self.mainframe, text="Cancella", command=lambda: self.clear_all_fields([self.act_type_entry, self.date_entry, self.act_number_entry, self.article_entry, self.extension_entry, self.comma_entry, self.version_date_entry]))
        clear_button.grid(row=8, column=2)
        copia_button = ttk.Button(self.mainframe, text="Copia Testo", command=self.copia_output)
        copia_button.grid(row=8, column=3)

        self.output_text = scrolledtext.ScrolledText(self.mainframe, wrap=tk.WORD, width=130, height=30)
        self.output_text.grid(row=10, column=0, columnspan=3, pady=10)

    def create_labeled_entry(self, label_text, tooltip_text, row, col):
        ttk.Label(self.mainframe, text=label_text).grid(row=row, column=col, sticky=tk.W)
        entry = ttk.Entry(self.mainframe)
        entry.grid(row=row, column=col+1, sticky=(tk.W, tk.E), padx=2, pady=2)
        
        # Icona tooltip
        tooltip_icon = ttk.Label(self.mainframe, text="?", font=('Helvetica', 10, 'bold'), background='lightgray', relief='raised')
        tooltip_icon.grid(row=row, column=col+2, sticky=tk.W, padx=(2, 0))
        Tooltip(tooltip_icon, tooltip_text)  # Associa il tooltip all'icona
        
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
        
    def create_menu(self):
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File menu
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Exit", command=self.on_exit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Accessibility menu
        self.accessibility_menu = Menu(self.menu_bar, tearoff=0)
        self.accessibility_menu.add_command(label="Increase Text Size", command=self.increase_text_size)
        self.accessibility_menu.add_command(label="High Contrast", command=self.apply_high_contrast_theme)
        self.menu_bar.add_cascade(label="Accessibility", menu=self.accessibility_menu)
        self.accessibility_menu.add_command(label="Decrease Text Size", command=self.decrease_text_size)
        self.accessibility_menu.add_command(label="Normal Theme", command=self.apply_normal_theme)
        
    def decrease_text_size(self):
        """Decrease text size of the widgets."""
        self.style.configure('TButton', font=('Helvetica', 10))
        self.style.configure('TLabel', font=('Helvetica', 10))


    def apply_normal_theme(self):
        """Apply normal theme for default visibility."""
        self.style.configure('TButton', background='SystemButtonFace', foreground='SystemButtonText')

    def on_exit(self):
        """Handle the exit command from the menu."""
        self.root.quit()

    def increase_text_size(self):
        """Increase text size of the widgets."""
        # Example: Increase font size for buttons
        self.style.configure('TButton', font=('Helvetica', 14))
        self.style.configure('TLabel', font=('Helvetica', 14))

    def apply_high_contrast_theme(self):
        """Apply high contrast theme for better visibility."""
        self.style.configure('TButton', background='black', foreground='white')
        # Apply high contrast configurations to other widgets as needed

if __name__ == "__main__":
    root = tk.Tk()
    app = NormaScraperApp(root)
    root.mainloop()
