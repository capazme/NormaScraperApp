import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import json
import tkinter as tk
from tkinter import messagebox, filedialog, Menu, simpledialog, Toplevel, StringVar
from tkinter.filedialog import askdirectory
import webbrowser
import pyperclip
from tools import sys_op
from tools.config import ConfigurazioneDialog
import os
import sys
from BrocardiScraper import BrocardiScraper

CURRENT_APP_PATH = os.path.dirname(os.path.abspath(__file__))

class Tooltip:
    """
    Create a tooltip for a given widget.
    """
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None

    def show_tooltip(self, event):
        x, y, cx, cy = self.widget.bbox("insert")   # Get the bounding box of the widget
        x += self.widget.winfo_rootx() + 25         # Calculate to display tooltip right of the widget
        y += self.widget.winfo_rooty() + 20         # Calculate to display tooltip below the widget
        # Create a toplevel window with required properties
        self.tip_window = tk.Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)   # Remove window decorations
        self.tip_window.wm_geometry(f"+{x}+{y}")    # Position the tooltip
        label = ttkb.Label(self.tip_window, text=self.text, background="lightyellow", relief='solid', borderwidth=1, wraplength=200)
        label.pack(ipadx=2, ipady=2)

    def hide_tooltip(self, event):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

class NormaScraperApp:
#
# SETUP
#
    def __init__(self, root):
        self.root = root
        self.configure_root()
        self.define_variables()
        self.bind_root_events()
        self.setup_style()
        self.create_widgets()
        self.create_menu()
        self.cronologia = []
        self.finestra_cronologia = None
        self.finestra_readme = None
        self.brocardi = BrocardiScraper()
        # self.updater = self.configure_updater()  # Uncomment and configure if updater is used

    def configure_root(self):
        self.root.title("NormaScraper - Beta")

    def define_variables(self):
        self.font_size = 15
        self.font_size_min = 10
        self.font_size_max = 30
        self.finestra_cronologia = None
        self.finestra_readme = None

    def bind_root_events(self):
        events = {
            '<Control-o>': lambda event:self.increase_text_size(),
            '<Control-i>': lambda event:self.decrease_text_size(),
            '<Control-r>': lambda event:self.restart_app(),
            '<Control-0>': lambda event:self.apply_high_contrast_theme(),
            '<Control-n>': lambda event:self.apply_normal_theme(),
            '<Control-p>': lambda event:self.apri_configurazione(),
            '<Control-q>': lambda event:self.on_exit(),
            '<Return>': lambda event:self.fetch_act_data(),
            '<Control-t>': lambda event:self.apri_finestra_cronologia(),
            '<Control-h>': lambda event: self.apri_readme(),
            '<Control-d>': lambda event: self.clear_all_fields(
                [self.date_entry, self.act_number_entry, self.article_entry, self.comma_entry, self.version_date_entry],
                self.act_type_combobox)
        }
        for event, action in events.items():
            self.root.bind(event, action)

#
# UI
#
    def setup_style(self):
        style = ttkb.Style()
        style.theme_use('flatly')  # Change theme here if needed
        self.font_configs = ('Helvetica', self.font_size)
        style.configure('TButton', font= self.font_configs)
        style.configure('TEntry', padding=5, font= self.font_configs)
        style.configure('TLabel', font= self.font_configs)
        style.configure('TRadiobutton', font= self.font_configs)

    def create_widgets(self):
        self.mainframe = ttkb.Frame(self.root, padding="3 3 12 12")
        self.configure_mainframe()
        self.create_input_widgets()
        self.create_version_radiobuttons()
        self.create_operation_buttons()
        self.create_output_area()
        self.create_history_buttons()
        
        self.brocardi_button = ttkb.Button(self.mainframe, text="Brocardi")
        self.brocardi_button.grid(row=1, column=3, sticky="ew", padx=5, pady=5)
        self.brocardi_button.grid_remove()

    def configure_mainframe(self):
        self.mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.geometry('800x800')  
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        for i in range(4):
            self.mainframe.columnconfigure(i, weight=1)
        for i in range(12):
            self.mainframe.rowconfigure(i, weight=1)
            
    def create_input_widgets(self):
        # Create input fields with labels and tooltips if necessary
        
        act_type_label = ttkb.Label(self.mainframe, text="Tipo atto:", bootstyle=INFO)
        act_type_label.grid(row=0, column=0, sticky=tk.W, padx=2, pady=2)

        act_types = [
            'legge', 'decreto legge', 'decreto legislativo', 'costituzione',
            'codice civile', 'preleggi', 'codice penale', 'codice di procedura civile',
            'codice di procedura penale', 'codice della navigazione',
            'codice postale e delle telecomunicazioni', 'codice della strada',
            'codice del processo tributario', 'codice in materia di protezione dei dati personali',
            'codice delle comunicazioni elettroniche', 'codice dei beni culturali e del paesaggio',
            'codice della proprietà industriale', "codice dell'amministrazione digitale",
            'codice della nautica da diporto', 'codice del consumo', 'codice delle assicurazioni private',
            'norme in materia ambientale', 'codice dei contratti pubblici', 'codice delle pari opportunità',
            "codice dell'ordinamento militare", 'codice del processo amministrativo', 'codice del turismo',
            'codice antimafia', 'codice di giustizia contabile', 'codice del terzo settore',
            'codice della protezione civile', "codice della crisi d'impresa e dell'insolvenza"
        ]
        self.act_type_var = tk.StringVar()
        self.act_type_combobox = self.create_combobox(self.mainframe, act_types, "Select", 0, 1)
        self.act_type_combobox['state'] = 'normal'

        #self.act_type_entry = self.create_labeled_entry("Tipo atto:", "Seleziona o digita il tipo di atto (es. legge, decreto)", 0)

        self.date_entry = self.create_labeled_entry("Data:", "Inserisci la data in formato YYYY-MM-DD, per esteso o solo anno (inserire solo l'anno comporterà un caricamento più lungo)", 1)
        self.act_number_entry = self.create_labeled_entry("Numero atto:", "Inserisci il numero dell'atto (obbligatorio se il tipo di atto è generico)", 2)

        self.article_entry = self.create_labeled_entry("Articolo:", "Inserisci l'articolo con estensione (-bis, -tris etc..), oppure aggiungi l'estensione premendo il pulsante", 3, increment=True)
         # Bottoni per incrementare e decrementare il valore
        self.comma_entry = self.create_labeled_entry("Comma:", "Inserisci il comma con estensione (-bis, -tris etc..), oppure aggiungi l'estensione premendo il pulsante", 4)

        self.version_date_entry = self.create_labeled_entry("Data versione atto (se non originale):", "Inserisci la data di versione dell'atto desiderata (default alla data corrente)", 6)

        # Setup for act_type_combobox, date_entry, act_number_entry, and article_entry goes here
    
    def create_version_radiobuttons(self):
        ttkb.Label(self.mainframe, text="Versione:", bootstyle=INFO).grid(row=5, column=0, sticky=W)
        self.version_var = StringVar(value="vigente")
        radio_buttons = [("Originale", "originale"), ("Vigente", "vigente")]
        for idx, (text, value) in enumerate(radio_buttons, start=1):
            ttkb.Radiobutton(self.mainframe, text=text, variable=self.version_var, value=value).grid(row=5, column=idx, sticky=W)

    def create_operation_buttons(self):
        # Create operation buttons like "Estrai dati", "Salva come XML", etc.
        operations = [
            ("Estrai dati", self.fetch_act_data, 0),
            ("Salva come XML", self.save_as_xml, 1),
            ("Cancella", lambda: self.clear_all_fields([self.date_entry, self.act_number_entry, self.article_entry, self.act_type_combobox], self.act_type_combobox), 2),
            ("Copia Testo", self.copia_output, 3)
        ]
        for text, command, column in operations:
            ttkb.Button(self.mainframe, text=text, command=command, bootstyle="success-outline").grid(row=8, column=column, sticky=(W, E), padx=4, pady=4)
    
    def create_tooltip(elf, widget, text):
        tool_tip = Tooltip(widget, text)
        widget.bind('<Enter>', tool_tip.show_tooltip)  # Bind mouse enter event
        widget.bind('<Leave>', tool_tip.hide_tooltip)  # Bind mouse leave event
            
    def create_combobox(self, container, values, default_text, row, column, **options):
            """
            Crea e restituisce una Combobox configurata.
            
            :param container: Il widget contenitore dove inserire la Combobox.
            :param values: Una lista di valori da mostrare nella Combobox.
            :param default_text: Il testo predefinito da visualizzare nella Combobox.
            :param row: La riga del layout grid dove posizionare la Combobox.
            :param column: La colonna del layout grid dove posizionare la Combobox.
            :param options: Opzioni aggiuntive per configurare la Combobox.
            :return: Un'istanza di ttkb.Combobox.
            """
            combobox = ttkb.Combobox(container, values=values, **options)
            combobox.grid(row=row, column=column, sticky=(tk.W, tk.E), padx=2, pady=2)
            combobox.set(default_text)
            return combobox
    
    def create_output_area(self):
        # Create scrolled text area for output
        self.output_text = ttkb.ScrolledText(self.mainframe, wrap=tk.WORD)
        self.output_text.grid(row=10, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

    def create_history_buttons(self):
        # Create buttons related to history operations
        history_ops = [
            ("Cronologia", self.apri_finestra_cronologia, 0),
            ("Salva cronologia", self.salva_cronologia, 2),
            ("Carica cronologia", self.carica_cronologia, 3)
        ]
        for text, command, column in history_ops:
            button = ttkb.Button(self.mainframe, text=text, command=command)
            button.grid(row=11, column=column, sticky="ew")
            
    def create_labeled_entry(self, label_text, placeholder, row, width=None, increment=False):
        # Create and place the label for the entry
        label = ttkb.Label(self.mainframe, text=label_text, bootstyle='info')
        label.grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)

        # Create the entry widget
        entry = ttkb.Entry(self.mainframe)
        entry.grid(row=row, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Attach a tooltip to the entry widget
        self.create_tooltip(entry, placeholder)  # Assuming create_tooltip is correctly implemented

        if increment:
            # Buttons for incrementing and decrementing the value
            inc_button = ttkb.Button(self.mainframe, text="▲", bootstyle="outline", command=lambda: self.increment_entry(entry))
            dec_button = ttkb.Button(self.mainframe, text="▼", bootstyle="outline", command=lambda: self.decrement_entry(entry))
            inc_button.grid(row=row, column=3, padx=2, pady=2, sticky=tk.E)
            dec_button.grid(row=row, column=4, padx=2, pady=2, sticky=tk.E)

        return entry


#
# FUNZIONI
#
    def apri_readme(self):
        github_url = "https://github.com/capazme/NormaScraperApp"
        webbrowser.open(github_url)

    def increment_entry(self, entry):
        current_value = entry.get()
        try:
            new_value = int(current_value) + 1 if current_value.isdigit() else 1
            entry.delete(0, tk.END)
            entry.insert(0, str(new_value))
        except ValueError:
            # Se il valore corrente non è un numero, imposta a 1
            entry.delete(0, tk.END)
            entry.insert(0, '1')

        # Chiamare fetch_act_data solo se il Combobox ha un valore valido e non è il default
        if self.act_type_combobox.get() != "Select":
            self.fetch_act_data()

    def decrement_entry(self, entry):
        current_value = entry.get()
        try:
            new_value = max(1, int(current_value) - 1) if current_value.isdigit() else 1
            entry.delete(0, tk.END)
            entry.insert(0, str(new_value))
        except ValueError:
            # Se il valore corrente non è un numero, imposta a 1
            entry.delete(0, tk.END)
            entry.insert(0, '1')

        # Chiamare fetch_act_data solo se il Combobox ha un valore valido e non è il default
        if self.act_type_combobox.get() != "Select":
            self.fetch_act_data()

    def toggle_extension(self):
        """Mostra o nasconde il frame dell'estensione."""
        if self.extension_frame.winfo_viewable():
            self.extension_frame.grid_forget()
            self.toggle_extension_btn.config(text="▼")
        else:
            self.extension_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E))
            self.toggle_extension_btn.config(text="▲") 

    def copia_output(self):
        content = self.output_text.get("1.0", tk.END)
        pyperclip.copy(content)
        messagebox.showinfo("Copia", "Testo copiato negli appunti!")

    def apri_url(self, url):
        webbrowser.open_new_tab(url)

    def clear_all_fields(self, entries, comboboxes=None, combobox_default_value="Seleziona il tipo di atto"):
        # Resetta tutti i campi Entry
        for entry in entries:
            entry.delete(0, tk.END)
        
        # Se è stato fornito un singolo Combobox, lo gestisce come se fosse in una lista
        if comboboxes is not None and not isinstance(comboboxes, list):
            comboboxes = [comboboxes]
        
        # Resetta tutti i Combobox ai loro valori predefiniti
        if comboboxes is not None:
            for combobox in comboboxes:
                combobox.set(combobox_default_value)

#
# XLM 
#
    def save_as_xml(self):
        file_path = filedialog.asksaveasfilename(
            title="Salva come XML",
            initialdir="/",
            filetypes=[("XML files", "*.xml")],
            defaultextension=".xml"
        )
        if file_path:
            self.fetch_act_data(save_xml_path=file_path)
            
        
#
# CRONOLOGIA
#        
    def aggiungi_a_cronologia(self, norma):
        # Controlla la dimensione massima della cronologia e aggiunge una nuova norma
        if len(self.cronologia) >= 50:
            self.cronologia.pop(0)
        if norma not in self.cronologia:
            self.cronologia.append(norma)

    def apri_finestra_cronologia(self):
        if hasattr(self, 'finestra_cronologia') and self.finestra_cronologia:
            self.finestra_cronologia.destroy()
            self.finestra_cronologia = None
        self.finestra_cronologia = tk.Toplevel(self.root)
        self.finestra_cronologia.title("Cronologia Ricerche")
        self.finestra_cronologia.geometry("600x400")

        self.tree = ttkb.Treeview(self.finestra_cronologia, columns=('Dato normativo', 'URL'), show='headings')
        self.tree.heading('Dato normativo', text='Dato normativo')
        self.tree.heading('URL', text='URL')
        self.tree.column('Dato normativo', width=400)
        self.tree.column('URL', width=200)
        
        self.tree_items = {}
        for norma in self.cronologia:
            item_id = self.tree.insert('', tk.END, values=(str(norma), norma.url))
            self.tree_items[item_id] = norma

        self.tree.bind("<Double-1>", self.on_item_clicked)
        scrollbar = ttkb.Scrollbar(self.finestra_cronologia, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        btn_pulisci = ttkb.Button(self.finestra_cronologia, text="Pulisci", command=self.cancella_cronologia)
        btn_pulisci.pack(side=tk.BOTTOM, anchor=tk.E, padx=10, pady=10)

    def on_item_clicked(self, event):
        col = self.tree.identify_column(event.x)
        item_id = self.tree.selection()[0]
        norma = self.tree_items.get(item_id)
        
        if col == '#1' and norma:  # Clic su "Dato normativo"
            self.ripeti_ricerca_selezionata(norma)
        elif col == '#2' and norma.url:  # Clic su "URL"
            webbrowser.open_new_tab(norma.url)
                
    def ripeti_ricerca_selezionata(self, norma):
        if norma:
            self.act_type_combobox.delete(0, tk.END)
            self.act_type_combobox.insert(0, norma.tipo_atto_str)

            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, norma.data)

            self.act_number_entry.delete(0, tk.END)
            self.act_number_entry.insert(0, norma.numero_atto)

            self.article_entry.delete(0, tk.END)
            self.article_entry.insert(0, norma.numero_articolo)

    def salva_cronologia(self):
        nome_file = simpledialog.askstring("Salva Cronologia", "Inserisci il nome del file:")
        if nome_file:
            # Chiede all'utente di scegliere la cartella dove salvare
            cartella_selezionata = askdirectory(title="Seleziona la cartella dove salvare la cronologia")
            
            if cartella_selezionata:  # Verifica che l'utente abbia selezionato una cartella
                # Costruisce il percorso completo dove salvare il file
                percorso_completo = os.path.join(cartella_selezionata, f"{nome_file}.json")

                try:
                    with open(percorso_completo, 'w') as f:
                        json.dump([n.to_dict() for n in self.cronologia], f, indent=4)
                    messagebox.showinfo("Salvato", "Cronologia salvata in " + percorso_completo)
                except Exception as e:
                    messagebox.showerror("Errore", f"Non è stato possibile salvare la cronologia: {e}")
            else:
                messagebox.showwarning("Annullato", "Salvataggio cronologia annullato.")

    def carica_cronologia(self):
        dir_cronologia = os.path.join(CURRENT_APP_PATH, "Resources", "Frameworks", "usr", "cron")
        
        percorso_file = filedialog.askopenfilename(title="Seleziona file cronologia", filetypes=(("JSON files", "*.json"), ("all files", "*.*"),), initialdir=dir_cronologia)
        if percorso_file:
            with open(percorso_file, 'r') as f:
                self.cronologia = [sys_op.NormaVisitata.from_dict(n) for n in json.load(f)]
            messagebox.showinfo("Caricato", "Cronologia caricata con successo")
            self.apri_finestra_cronologia()
 
    def cancella_cronologia(self):
        # Pulisce la cronologia
        if len(self.cronologia)>0:
            self.tree.delete(*self.tree.get_children())
            self.cronologia.clear()
            messagebox.showinfo("Cronologia", "Cronologia pulita con successo.")


#       
# OUTPUT
#
    def fetch_act_data(self, save_xml_path=None):
        act_type = self.act_type_combobox.get()  
        date = self.date_entry.get()
        act_number = self.act_number_entry.get()
        article = self.article_entry.get()
        #extension = self.extension_entry.get()
        version = self.version_var.get()
        version_date = self.version_date_entry.get()
        comma = self.comma_entry.get()
        
        if save_xml_path:
            article = None
        
        try:
            data, url, norma = sys_op.get_urn_and_extract_data(act_type=act_type, date=date, act_number=act_number, article=article, comma=comma, version=version, version_date=version_date, save_xml_path=save_xml_path)
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, data)
            self.crea_link("Apri URN Normattiva", url, 9, 1)
            self.aggiungi_a_cronologia(norma)
            self.check_brocardi(norma)
                

        except Exception as e:
            messagebox.showerror("Errore", str(e))

    def check_brocardi(self, norma):
        result = self.brocardi.look_up(norma)
        if result:
            self.brocardi_button.grid()  # Mostra il pulsante
            self.brocardi_button.configure(command=lambda: self.apri_url(result))
        else:
            self.brocardi_button.grid_remove()
        
    def crea_link(self, text, url, row, column):
        link = tk.Label(self.mainframe, text=text, fg="blue", cursor="hand2")
        link.bind("<Button-1>", lambda e: self.apri_url(url))
        link.grid(row=row, column=column)
        
#
# MENU
#

    def create_menu(self):
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)

        #
        # File menu
        #
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Restart (ctrl+r)", command=self.restart_app)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit (ctrl+q)", command=self.on_exit)
        #
        # Accessibility menu
        #
        
        self.accessibility_menu = Menu(self.menu_bar, tearoff=0)
        self.accessibility_menu.add_command(label="Increase Text Size (ctrl+i)", command=self.increase_text_size)
        self.accessibility_menu.add_command(label="HELP (ctrl+h)", command=self.apri_readme)
        self.accessibility_menu.add_command(label="High Contrast (ctrl+h)", command=self.apply_high_contrast_theme)
        self.menu_bar.add_cascade(label="Accessibility", menu=self.accessibility_menu)
        self.accessibility_menu.add_command(label="Decrease Text Size (ctrl+o)", command=self.decrease_text_size)
        self.accessibility_menu.add_command(label="Normal Theme (ctrl+n)", command=self.apply_normal_theme)
        #self.accessibility_menu.add_command(label="Configura", command=self.apri_configurazione)
      
        # Update menu
        #self.update_menu = tk.Menu(self.menu_bar, tearoff=0)
        #self.update_menu.add_command(label="Check for Updates", command=self.user_initiated_update)
        #self.menu_bar.add_cascade(label="Update", menu=self.update_menu)

    def apri_configurazione(self):
        ConfigurazioneDialog(self.root)

    def restart_app(self):
        """Restart the app."""
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def apply_normal_theme(self):
        """Apply normal theme for default visibility."""
        self.style.configure('TButton', background='SystemButtonFace', foreground='SystemButtonText')

    def on_exit(self):
        """Handle the exit command from the menu."""
        self.root.quit()

    def increase_text_size(self):
        """Aumenta la dimensione del testo entro il limite massimo."""
        if self.font_size < self.font_size_max:
            self.font_size += 2  # Incrementa di 2 punti
            self.setup_style()  # Riapplica gli stili con la nuova dimensione del font

    def decrease_text_size(self):
        """Diminuisce la dimensione del testo entro il limite minimo."""
        if self.font_size > self.font_size_min:
            self.font_size -= 2  # Decrementa di 2 punti
            self.setup_style()  # Riapplica gli stili con la nuova dimensione del font


    def apply_high_contrast_theme(self):
        """Apply high contrast theme for better visibility."""
        self.style.configure('TButton', background='black', foreground='white')
        # Apply high contrast configurations to other widgets as needed

    #def check_for_updates(self):
    #    self.updater.check_and_update()

if __name__ == "__main__":
    root = tk.Tk()
    app = NormaScraperApp(root)
    #codes_to_preload = ["costituzione", "codice civile", "codice penale"]
    #app.start_async_preloading(codes_to_preload)
    root.mainloop()
   

