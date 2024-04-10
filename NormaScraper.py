import tkinter as tk 
import json
from tkinter import ttk, messagebox, scrolledtext, filedialog, Menu, simpledialog
from tkinter.filedialog import askdirectory
import webbrowser
import pyperclip
from usr import *
from sys_op import get_urn_and_extract_data, NormaVisitata
from config import ConfigurazioneDialog
import os
from functools import lru_cache
import sys
import tempfile
import subprocess
#from git import Repo

CURRENT_APP_PATH = os.path.dirname(os.path.abspath(__file__))

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
            '<Control-h>': lambda event: self.apri_finestra_readme(),
            '<Control-z>': lambda event: self.clear_all_fields(
                [self.date_entry, self.act_number_entry, self.article_entry, self.comma_entry, self.version_date_entry],
                self.act_type_combobox)
        }
        for event, action in events.items():
            self.root.bind(event, action)

#
# UI
#
    def setup_style(self):
        style = ttk.Style()
        style.theme_use('alt')
        font_configs = ('Helvetica', self.font_size)
        style.configure('TButton', font=font_configs, foreground='black', background='white')
        style.configure('TEntry', padding=5, font=font_configs)
        style.configure('TLabel', font=font_configs)
        style.configure('TRadioButton', font=font_configs)

    def create_widgets(self):
        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.configure_mainframe()
        self.create_input_widgets()
        self.create_version_radiobuttons()
        self.create_operation_buttons()
        self.create_output_area()
        self.create_history_buttons()

    def configure_mainframe(self):
        self.mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        for i in range(4):
            self.mainframe.columnconfigure(i, weight=1)
        for i in range(12):
            self.mainframe.rowconfigure(i, weight=1)
            
    def create_input_widgets(self):
        # Create input fields with labels and tooltips if necessary
        
        act_type_label = ttk.Label(self.mainframe, text="Tipo atto:")
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
        self.act_type_combobox = self.create_combobox(self.mainframe, act_types, "Seleziona il tipo di atto", 0, 1)
        self.act_type_combobox['state'] = 'normal'

        #self.act_type_entry = self.create_labeled_entry("Tipo atto:", "Seleziona o digita il tipo di atto (es. legge, decreto)", 0)

        self.date_entry = self.create_labeled_entry("Data:", "Inserisci la data in formato YYYY-MM-DD, per esteso o solo anno (inserire solo l'anno comporterà un caricamento più lungo)", 1)
        self.act_number_entry = self.create_labeled_entry("Numero atto:", "Inserisci il numero dell'atto (obbligatorio se il tipo di atto è generico)", 2)

        self.article_entry = self.create_labeled_entry("Articolo:", "Inserisci l'articolo con estensione (-bis, -tris etc..), oppure aggiungi l'estensione premendo il pulsante", 3)
         # Bottoni per incrementare e decrementare il valore
        increment_button = ttk.Button(self.mainframe, text="▲", command=lambda: self.increment_entry(self.article_entry), width = 3) 
        increment_button.grid(row=3, column=3, padx=(0,1), sticky=(tk.E))  # Riduci lo spazio tra i pulsanti con padx
        decrement_button = ttk.Button(self.mainframe, text="▼", command=lambda: self.decrement_entry(self.article_entry), width = 3)
        decrement_button.grid(row=3, column=4, padx=(0,1), sticky=(tk.E))

        self.comma_entry = self.create_labeled_entry("Comma:", "Inserisci il comma con estensione (-bis, -tris etc..), oppure aggiungi l'estensione premendo il pulsante", 4)

        self.version_date_entry = self.create_labeled_entry("Data versione atto (se non originale):", "Inserisci la data di versione dell'atto desiderata (default alla data corrente)", 6)

        # Setup for act_type_combobox, date_entry, act_number_entry, and article_entry goes here
        
    def create_version_radiobuttons(self):
        # Create and layout version radio buttons
        label = ttk.Label(self.mainframe, text="Versione:")
        label.grid(row=5, column=0, sticky=tk.W)
        self.version_var = tk.StringVar(value="vigente")
        radio_buttons = [
            ("Originale", "originale"),
            ("Vigente", "vigente")
        ]
        for idx, (text, value) in enumerate(radio_buttons, start=1):
            button = ttk.Radiobutton(self.mainframe, text=text, variable=self.version_var, value=value)
            button.grid(row=5, column=idx, sticky=tk.W)

    def create_operation_buttons(self):
        # Create operation buttons like "Estrai dati", "Salva come XML", etc.
        operations = [
            ("Estrai dati", self.fetch_act_data, 0),
            ("Salva come XML", self.save_as_xml, 1),
            ("Cancella", lambda: self.clear_all_fields([self.date_entry, self.act_number_entry, self.article_entry, self.act_type_combobox], self.act_type_combobox), 2),
            ("Copia Testo", self.copia_output, 3)
        ]
        for text, command, column in operations:
            button = ttk.Button(self.mainframe, text=text, command=command)
            button.grid(row=8, column=column, sticky=(tk.W, tk.E), padx=4, pady=4)
            
    def create_combobox(self, container, values, default_text, row, column, **options):
            """
            Crea e restituisce una Combobox configurata.
            
            :param container: Il widget contenitore dove inserire la Combobox.
            :param values: Una lista di valori da mostrare nella Combobox.
            :param default_text: Il testo predefinito da visualizzare nella Combobox.
            :param row: La riga del layout grid dove posizionare la Combobox.
            :param column: La colonna del layout grid dove posizionare la Combobox.
            :param options: Opzioni aggiuntive per configurare la Combobox.
            :return: Un'istanza di ttk.Combobox.
            """
            combobox = ttk.Combobox(container, values=values, **options)
            combobox.grid(row=row, column=column, sticky=(tk.W, tk.E), padx=2, pady=2)
            combobox.set(default_text)
            return combobox
    
    def create_output_area(self):
        # Create scrolled text area for output
        self.output_text = scrolledtext.ScrolledText(self.mainframe, wrap=tk.WORD)
        self.output_text.grid(row=10, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

    def create_history_buttons(self):
        # Create buttons related to history operations
        history_ops = [
            ("Cronologia", self.apri_finestra_cronologia, 0),
            ("Salva cronologia", self.salva_cronologia, 2),
            ("Carica cronologia", self.carica_cronologia, 3)
        ]
        for text, command, column in history_ops:
            button = ttk.Button(self.mainframe, text=text, command=command)
            button.grid(row=11, column=column, sticky="ew")
            
    def create_labeled_entry(self, label, placeholder, row, width = None):
        ttk.Label(self.mainframe, text=label).grid(row=row, column=0, sticky=tk.W)
        entry = ttk.Entry(self.mainframe)
        entry.grid(row=row, column=1, columnspan=2, sticky=(tk.W, tk.E))
            
            # Icona tooltip
        tooltip_icon = ttk.Label(self.mainframe, text="?", font=('Helvetica', 10, 'bold'), background='lightgray', relief='raised', width=width)
        tooltip_icon.grid(row=row, column=1+2, sticky=tk.W, padx=(2, 0))
        Tooltip(tooltip_icon, placeholder)  # Associa il tooltip all'icona
        return entry
    





#
# FUNZIONI
#
    
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
        if self.act_type_combobox.get() != "Seleziona il tipo di atto":
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
        if self.act_type_combobox.get() != "Seleziona il tipo di atto":
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

    def apri_finestra_readme(self):
        if not self.finestra_readme or not self.finestra_readme.winfo_exists():
            self.finestra_readme = tk.Toplevel(self.root)
            self.finestra_readme.title("INFO")
            self.finestra_readme.geometry("600x400")

            text_area = scrolledtext.ScrolledText(self.finestra_readme, wrap=tk.WORD, width=40, height=10)
            text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            text_area.configure(font='TkFixedFont', state='disabled')
            

            # Costruisce il percorso alla cartella "usr/cron" partendo dalla directory corrente
            readmepath = os.path.join(CURRENT_APP_PATH, "README.txt")
            if dir:
                with open(readmepath, 'r') as file:
                    readme_content = file.read()
            else:
                readme_content = "File README.txt non trovato."

            text_area.configure(state='normal')
            text_area.insert(tk.INSERT, readme_content)
            text_area.configure(state='disabled')
        else:
            # Porta la finestra secondaria esistente in primo piano
            self.finestra_readme.lift()

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
        if self.finestra_cronologia:
            self.finestra_cronologia.destroy()
            self.finestra_cronologia = None
        self.finestra_cronologia = tk.Toplevel(self.root)
        self.finestra_cronologia.title("Cronologia Ricerche")
        self.finestra_cronologia.geometry("600x400")

        self.tree = ttk.Treeview(self.finestra_cronologia, columns=('Dato normativo', 'URL'), show='headings')
        self.tree.heading('Dato normativo', text='Dato normativo')
        self.tree.heading('URL', text='URL')
        self.tree.column('Dato normativo', width=400)
        self.tree.column('URL', width=200)
        
        self.tree_items = {}
        for norma in self.cronologia:
            item_id = self.tree.insert('', tk.END, values=(str(norma), norma.url))
            self.tree_items[item_id] = norma

        self.tree.bind("<Double-1>", self.on_item_clicked)
        scrollbar = ttk.Scrollbar(self.finestra_cronologia, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

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
            self.act_type_combobox.insert(0, norma.tipo_atto)

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
                self.cronologia = [NormaVisitata.from_dict(n) for n in json.load(f)]
            messagebox.showinfo("Caricato", "Cronologia caricata con successo")
            self.apri_finestra_cronologia()
 
    def cancella_cronologia(self):
        # Pulisce la cronologia
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
        
        try:
            data, url, norma = get_urn_and_extract_data(act_type=act_type, date=date, act_number=act_number, article=article, comma=comma, version=version, version_date=version_date, save_xml_path=save_xml_path)
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, data)
            self.crea_link("Apri URN Normattiva", url, 9, 1)
            self.aggiungi_a_cronologia(norma)

        except Exception as e:
            messagebox.showerror("Errore", str(e))

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
        self.accessibility_menu.add_command(label="HELP (ctrl+h)", command=self.apri_finestra_readme)
        self.accessibility_menu.add_command(label="High Contrast (ctrl+h)", command=self.apply_high_contrast_theme)
        self.menu_bar.add_cascade(label="Accessibility", menu=self.accessibility_menu)
        self.accessibility_menu.add_command(label="Decrease Text Size (ctrl+o)", command=self.decrease_text_size)
        self.accessibility_menu.add_command(label="Normal Theme (ctrl+n)", command=self.apply_normal_theme)
        #self.accessibility_menu.add_command(label="Configura", command=self.apri_configurazione)
      
        # Update menu
        #self.update_menu = tk.Menu(self.menu_bar, tearoff=0)
        #self.update_menu.add_command(label="Check for Updates", command=self.user_initiated_update)
        #self.menu_bar.add_cascade(label="Update", menu=self.update_menu)

        
    #def user_initiated_update(self):
    #    """Controlla gli aggiornamenti in un thread separato."""
    #    update_thread = threading.Thread(target=self.check_and_apply_update, daemon=True)
    #    update_thread.start()

    #def check_and_apply_update(self):
    #    is_available, latest_version = self.updater.is_update_available()
    #    if is_available:
    #        self.prompt_for_update(latest_version)

    #def prompt_for_update(self, latest_version):
    #    """Chiede all'utente se desidera applicare l'aggiornamento."""
    #    # Usa self.root.after per eseguire questa operazione nel thread dell'UI
    #    self.root.after(0, lambda: self.ask_to_update(latest_version))
 
    #def ask_to_update(self, latest_version):
    #    response = messagebox.askyesno("Aggiornamento Disponibile", f"È disponibile un nuovo aggiornamento alla versione {latest_version}. Vuoi applicarlo ora?")
    #    if response:
    #        self.updater.apply_update(latest_version)

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
   

