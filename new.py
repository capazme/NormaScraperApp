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

class AutoUpdater:
    def __init__(self, repo_url, app_directory, build_command, main_app_script=None):
        self.repo_url = repo_url
        self.app_directory = app_directory
        self.build_command = build_command
        self.main_app_script = main_app_script if main_app_script else ""

    def fetch_latest_tag(self):
        repo = Repo.clone_from(self.repo_url, tempfile.mkdtemp())
        tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
        latest_tag = tags[-1] if tags else None
        return latest_tag

    def is_update_available(self):
        current_version = self.get_current_version()
        latest_tag = self.fetch_latest_tag()
        if latest_tag and (latest_tag.name != current_version):
            return True, latest_tag.name
        return False, None

    def get_current_version(self):
        try:
            with open(os.path.join(self.app_directory, 'version.txt'), 'r') as version_file:
                return version_file.read().strip()
        except FileNotFoundError:
            return '0.0.0'

    def apply_update(self, latest_version):
        temp_dir = tempfile.mkdtemp()
        Repo.clone_from(self.repo_url, temp_dir, branch=latest_version)
        subprocess.check_call(self.build_command, cwd=temp_dir, shell=True)
        # Copia l'eseguibile aggiornato e il nuovo file version.txt
        # Assicurati che queste operazioni siano atomiche e gestisci i permessi di file se necessario
        # Il codice specifico dipende dalla struttura del progetto e dalla piattaforma

        self.restart_app()

    def restart_app(self):
        python = sys.executable
        os.execl(python, python, self.main_app_script)



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
        self.font_size = 15  # Imposta la dimensione iniziale del font
        self.font_size_min = 10  # Dimensione minima del font
        self.font_size_max = 30
        self.root.bind('<Control-o>', lambda event: self.increase_text_size())
        self.root.bind('<Control-i>', lambda event: self.decrease_text_size())
        self.root.bind('<Control-r>', lambda event: self.restart_app())
        self.root.bind('<Control-0>', lambda event: self.apply_high_contrast_theme())
        self.root.bind('<Control-n>', lambda event: self.apply_normal_theme())
        self.root.bind('<Control-p>', lambda event: self.apri_configurazione())
        self.root.bind('<Control-q>', lambda event: self.on_exit())
        self.root.bind('<Return>', lambda event: self.fetch_act_data())
        self.root.bind('<Control-t>', lambda event: self.apri_finestra_cronologia())
        self.root.bind('<Control-h>', lambda event: self.apri_finestra_readme())
        self.root.bind('<Control-z>', lambda event: self.clear_all_fields([self.date_entry, self.act_number_entry, self.article_entry, self.comma_entry, self.version_date_entry], self.act_type_combobox))
        self.setup_style()
        self.create_menu()
        self.create_widgets()
        self.cronologia = []
        self.finestra_cronologia = None
        self.finestra_readme = None
        #self.updater = AutoUpdater(
        #    repo_url='https://github.com/capazme/NormaScraperApp.git',
        #    app_directory=os.path.dirname(os.path.abspath(sys.argv[0])),
        #    build_command='pyinstaller -c -F -i resources/icon.icns --onefile NormaScraper.py'
        #)

        #print(self.updater.app_directory)


#
#  STYLE
#

    def setup_style(self):
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('TButton', font=('Helvetica', self.font_size), foreground='black', background='white')
        self.style.configure('TEntry', padding=5, font=('Helvetica', self.font_size))
        self.style.configure('TLabel', font=('Helvetica', self.font_size))
        self.style.configure('TRadioButton', font=('Helvetica', self.font_size))


#
#  INPUT
#

    def create_widgets(self):
        # Configura il mainframe
        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Configura la griglia per espandersi
        for i in range(4):
            self.mainframe.columnconfigure(i, weight=1)
        for i in range(12):
            self.mainframe.rowconfigure(i, weight=1)

        # Input fields
        self.act_type_entry = self.create_labeled_entry("Tipo atto:", "Seleziona o digita il tipo di atto (es. legge, decreto)", 0)
        
        act_types = ['legge', 'decreto legge', 'decreto legislativo', 'costituzione', 'codice civile', 'preleggi', 'codice penale', 'codice di procedura civile', 'codice di procedura penale', 'codice della navigazione', 'codice postale e delle telecomunicazioni', 'codice della strada', 'codice del processo tributario', 'codice in materia di protezione dei dati personali', 'codice delle comunicazioni elettroniche', 'codice dei beni culturali e del paesaggio', 'codice della proprietà industriale', "codice dell'amministrazione digitale", 'codice della nautica da diporto', 'codice del consumo', 'codice delle assicurazioni private', 'norme in materia ambientale', 'codice dei contratti pubblici', 'codice delle pari opportunità', "codice dell'ordinamento militare", 'codice del processo amministrativo', 'codice del turismo', 'codice antimafia', 'codice di giustizia contabile', 'codice del terzo settore', 'codice della protezione civile', "codice della crisi d'impresa e dell'insolvenza"]
        self.act_type_combobox = ttk.Combobox(self.mainframe, values=act_types, font=('Helvetica', 15))
        self.act_type_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=2, pady=2)
        self.act_type_combobox.set("Seleziona il tipo di atto")
        
        self.date_entry = self.create_labeled_entry("Data:", "Inserisci la data in formato YYYY-MM-DD, per esteso o solo anno (inserire solo l'anno comporterà un caricamento più lungo)", 1)
        self.act_number_entry = self.create_labeled_entry("Numero atto:", "Inserisci il numero dell'atto (obbligatorio se il tipo di atto è generico)", 2)
        
        #Entry articolo + pulsanti
        self.article_entry = self.create_labeled_entry("Articolo:", "Inserisci l'articolo con estensione (-bis, -tris etc..), oppure aggiungi l'estensione premendo il pulsante", 3)

        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=2)  # Peso maggiore per l'entry
        self.mainframe.columnconfigure(2, weight=1)
        self.mainframe.columnconfigure(3, weight=2)  # Peso maggiore per l'entry
        self.mainframe.columnconfigure(4, weight=1)  # Peso minore per il resto

        # Aggiungi l'entry e i pulsanti al layout
        self.article_entry.grid(row=3, column=1, columnspan=3, sticky=(tk.W, tk.E))  # Usa columnspan per allargare l'entry

        # Aggiungi il pulsante di decremento
        decrement_button_art = ttk.Button(self.mainframe, text="<", width=3, command=lambda: self.decrement_entry(self.article_entry))
        decrement_button_art.grid(row=3, column=0, sticky=tk.E)

        # Aggiungi il pulsante di incremento
        increment_button_art = ttk.Button(self.mainframe, text=">", width=3, command=lambda: self.increment_entry(self.article_entry))
        increment_button_art.grid(row=3, column=4, sticky=tk.W)

        # Version radio buttons
        ttk.Label(self.mainframe, text="Versione:").grid(row=6, column=0, sticky=tk.W)
        self.version_var = tk.StringVar(value="vigente")
        ttk.Radiobutton(self.mainframe, text="Originale", variable=self.version_var, value="originale").grid(row=6, column=1, sticky=tk.W)
        ttk.Radiobutton(self.mainframe, text="Vigente", variable=self.version_var, value="vigente").grid(row=6, column=2, sticky=tk.W)
        
       


        self.version_date_entry = self.create_labeled_entry("Data versione atto (se non originale):", "Inserisci la data di versione dell'atto desiderata (default alla data corrente)", 7)


        # Pulsanti
        fetch_button = ttk.Button(self.mainframe, text="Estrai dati", command=self.fetch_act_data)
        fetch_button.grid(row=8, column=0, sticky=(tk.W, tk.E), padx=4, pady=4)

        # Pulsante per salvare come XML
        save_xml_button = ttk.Button(self.mainframe, text="Salva come XML", command=self.save_as_xml)
        save_xml_button.grid(row=8, column=1, sticky=(tk.W, tk.E), padx=4, pady=4)

        # Pulsante per cancellare i campi di input
        clear_button = ttk.Button(self.mainframe, text="Cancella (ctrl-z)", command=lambda: self.clear_all_fields([self.date_entry, self.act_number_entry, self.article_entry, self.comma_entry, self.version_date_entry], self.act_type_combobox))
        clear_button.grid(row=8, column=2, sticky=(tk.W, tk.E), padx=4, pady=4)

        # Pulsante per copiare il testo
        copia_button = ttk.Button(self.mainframe, text="Copia Testo", command=self.copia_output)
        copia_button.grid(row=8, column=3, sticky=(tk.W, tk.E), padx=4, pady=4)
        self.mainframe.columnconfigure(1, weight=1)
        
        # Area di testo scorrevole per l'output
        self.output_text = scrolledtext.ScrolledText(self.mainframe, wrap=tk.WORD)
        self.output_text.grid(row=10, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

        self.button_cronologia = ttk.Button(self.mainframe, text="Cronologia", command=self.apri_finestra_cronologia)
        self.button_cronologia.grid(row=11, column=0, sticky="ew")

        salva_cron = ttk.Button(self.mainframe, text="Salva cronologia", command=self.salva_cronologia)
        salva_cron.grid(row=11, column=2, sticky="ew")

        carica_cron = ttk.Button(self.mainframe, text="Carica cronologia", command=self.carica_cronologia)
        carica_cron.grid(row=11, column=3, sticky="ew")
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.columnconfigure(2, weight=1)
        self.mainframe.columnconfigure(3, weight=1)
        
#
#  FUNCIONS
#
    def create_labeled_entry(self, label, placeholder, row, width = None):
        ttk.Label(self.mainframe, text=label).grid(row=row, column=0, sticky=tk.W)
        entry = ttk.Entry(self.mainframe)
        entry.grid(row=row, column=1, columnspan=2, sticky=(tk.W, tk.E))
            
            # Icona tooltip
        tooltip_icon = ttk.Label(self.mainframe, text="?", font=('Helvetica', 10, 'bold'), background='lightgray', relief='raised', width=width)
        tooltip_icon.grid(row=row, column=1+2, sticky=tk.W, padx=(2, 0))
        Tooltip(tooltip_icon, placeholder)  # Associa il tooltip all'icona
        return entry
    
    def increment_entry(self, entry):
        # Recupera il valore corrente dall'entry specificata, incrementalo e aggiorna l'entry
        current_value = entry.get()
        try:
            # Assicurati che il valore corrente sia un numero intero
            new_value = int(current_value) + 1
            entry.delete(0, tk.END)  # Pulisci l'entry
            entry.insert(0, str(new_value))  # Inserisci il nuovo valore
        except ValueError:
            # Se il valore corrente non è un numero, ignoralo o mostra un messaggio di errore
            pass

    def decrement_entry(self, entry):
        # Recupera il valore corrente dall'entry specificata, decrementalo e aggiorna l'entry
        current_value = entry.get()
        try:
            # Assicurati che il valore corrente sia un numero intero e non negativo
            new_value = max(0, int(current_value) - 1)
            entry.delete(0, tk.END)  # Pulisci l'entry
            entry.insert(0, str(new_value))  # Inserisci il nuovo valore
        except ValueError:
            # Se il valore corrente non è un numero, ignoralo o mostra un messaggio di errore
            pass
        
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

    def clear_all_fields(self, entries, combobox=None, combobox_default_value="Seleziona il tipo di atto"):
        for entry in entries:
            entry.delete(0, tk.END)
        if combobox is not None:
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
   

