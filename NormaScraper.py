# ==============================================================================


#   /$$   /$$                                              /$$$$$$                                                            
#  | $$$ | $$                                             /$$__  $$                                                           
#  | $$$$| $$  /$$$$$$   /$$$$$$  /$$$$$$/$$$$   /$$$$$$ | $$  \__/  /$$$$$$$  /$$$$$$  /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$ 
#  | $$ $$ $$ /$$__  $$ /$$__  $$| $$_  $$_  $$ |____  $$|  $$$$$$  /$$_____/ /$$__  $$|____  $$ /$$__  $$ /$$__  $$ /$$__  $$
#  | $$  $$$$| $$  \ $$| $$  \__/| $$ \ $$ \ $$  /$$$$$$$ \____  $$| $$      | $$  \__/ /$$$$$$$| $$  \ $$| $$$$$$$$| $$  \__/
#  | $$\  $$$| $$  | $$| $$      | $$ | $$ | $$ /$$__  $$ /$$  \ $$| $$      | $$      /$$__  $$| $$  | $$| $$_____/| $$      
#  | $$ \  $$|  $$$$$$/| $$      | $$ | $$ | $$|  $$$$$$$|  $$$$$$/|  $$$$$$$| $$     |  $$$$$$$| $$$$$$$/|  $$$$$$$| $$      
#  |__/  \__/ \______/ |__/      |__/ |__/ |__/ \_______/ \______/  \_______/|__/      \_______/| $$____/  \_______/|__/      
#                                                                                               | $$                          
#                                                                                               | $$                          
#                                                                                               |__/                          
                                                                                             
                                             
# ==============================================================================
# Application Name: NormaScraper App
# Description: This application is designed to fetch, display, and manage legal
# norms and articles from various legal databases. It supports configuration
# through a GUI, making it accessible for non-technical users to perform complex
# queries and retrieve legal documents effectively.
#
# Main Features:
# - Fetch and display legal norms based on user inputs.
# - Save queries to XML.
# - Manage query history and configurations.
# - Dynamic tooltips and UI elements for better user experience.
#
# Author: gpuzio - capazme
# License: CC0-1.0 License
# ==============================================================================


# ==============================================================================
# Environment and Path Setup
# ==============================================================================
import os
import sys

CURRENT_APP_PATH = os.path.dirname(os.path.abspath(__file__))

# ==============================================================================
# Import Section
# ==============================================================================
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import json
import tkinter as tk
from ttkbootstrap.constants import *
from tkinter import BooleanVar, Tk
from tkinter import messagebox, filedialog, Menu, simpledialog, Toplevel, StringVar
from tkinter.filedialog import askdirectory
import webbrowser
import pyperclip
from tools import sys_op
from tools.config import ConfigurazioneDialog
import threading
from BrocardiScraper import BrocardiScraper

# ==============================================================================
# Class Definitions
# Description: Contains all class definitions including Tooltip for widget 
# tooltips and NormaScraperApp for main application logic.
#
# Classes:
# - Tooltip: Manages tooltips for widgets.
# - NormaScraperApp: Main class for the application UI and functionality.
# ==============================================================================
# --------------------------------
# UTILITY CLASSES
# --------------------------------
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

# --------------------------------
# MAIN APPLICATION CLASS
# --------------------------------
class NormaScraperApp:
    
# ==============================================================================
# Class Initialization
# Description: Initializes the application, sets up the main window, binds events,
# and configures the application's initial state and behavior.
# ==============================================================================
    
    def __init__(self, root):
        self.root = root
        self.configure_root()
        self.define_variables()
        self.bind_root_events()
        self.setup_style()
        self.setup_driver()
        self.create_widgets()
        self.create_menu()
        self.brocardi = BrocardiScraper()
        # self.updater = self.configure_updater()  # Uncomment and configure if updater is used

# ==============================================================================
# Root Configuration
# Description: Configures the main window's properties.
# ==============================================================================
    def configure_root(self):
        self.root.title("NormaScraper - Beta")
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

# ==============================================================================
# Driver Setup
# Description: Sets up and initializes the driver required for operations.
# ==============================================================================
    def setup_driver(self):
        try:
            sys_op.setup_driver()
        except Exception as e:
            messagebox.showerror("Errore di Avvio", f"Impossibile avviare il driver: {e}")
            return self.close_driver_safely()

# ==============================================================================
# Safe Driver Closure
# Description: Safely closes the driver and handles any exceptions.
# ==============================================================================
    def close_driver_safely(self, close=False):
        try:
            sys_op.close_driver()
        except Exception as e:
            messagebox.showerror("Errore di Chiusura", f"Errore durante la chiusura del driver: {e}")
        if close==True:
            self.root.destroy()

# ==============================================================================
# Variable Definitions
# Description: Defines and initializes variables used throughout the application.
# ==============================================================================
    def define_variables(self):
        self.font_size = 15
        self.font_size_min = 10
        self.font_size_max = 30
        self.finestra_cronologia = None
        self.finestra_readme = None
        self.cronologia = []
        self.finestra_cronologia = None
        self.finestra_readme = None
        self.brocardi_but = False
        self.brocardi_var = BooleanVar(value=self.brocardi_but)


# ==============================================================================
# Event Binding
# Description: Binds keyboard and mouse events to their respective handler functions.
# ==============================================================================
    def bind_root_events(self):
        events = {
            '<Control-o>': lambda event: self.increase_text_size(),
            '<Shift-Right>': lambda event: self.increment_entry(self.article_entry),
            '<Shift-Left>': lambda event: self.decrement_entry(self.article_entry),
            '<Control-i>': lambda event: self.decrease_text_size(),
            '<Control-r>': lambda event: self.restart_app(),
            '<Control-0>': lambda event: self.apply_high_contrast_theme(),
            '<Control-9>': lambda event: self.apply_normal_theme(),
            '<Control-p>': lambda event: self.apri_configurazione(),
            '<Control-q>': lambda event: self.on_exit(),
            '<Return>': lambda event: self.fetch_act_data(),
            '<Control-t>': lambda event: self.apri_finestra_cronologia(),
            '<Control-h>': lambda event: self.apri_readme(),
            '<Control-6>': lambda event: self.break_progress(),
            '<Control-d>': lambda event: self.clear_all_fields(
                [self.date_entry, self.act_number_entry, self.article_entry, self.comma_entry, self.version_date_entry],
                self.act_type_combobox)
        }
        for event, action in events.items():
            self.root.bind(event, action)

# ==============================================================================
# UI Style Configuration
# Description: Configures the visual style of the application using the ttkbootstrap library.
# ==============================================================================
    def setup_style(self):
        style = ttkb.Style()
        style.theme_use('flatly')  # Change theme here if needed
        self.font_configs = ('Helvetica', self.font_size)
        style.configure('TButton', font= self.font_configs)
        style.configure('TEntry', padding=5, font= self.font_configs)
        style.configure('TLabel', font= self.font_configs)
        style.configure('TRadiobutton', font= self.font_configs)
        style.configure('act.TCombobox', font=self.font_configs, arrowsize=self.font_size)
        style.map('act.TCombobox', arrowcolor=[
                    ('disabled', 'gray'),
                    ('pressed !disabled', 'blue'),
                    ('focus !disabled', 'green'),
                    ('hover !disabled', 'green')])


# ==============================================================================
# Widget Creation
# Description: Creates and organizes all widgets in the main application window.
# ==============================================================================
    def create_widgets(self):
        self.mainframe = ttkb.Frame(self.root, padding="3 3 12 12")
        self.create_input_widgets()
        self.create_version_radiobuttons()
        self.create_operation_buttons()
        self.create_output_area()
        self.create_history_buttons()
        self.create_progress_bar()
        self.create_brocardi_toggle_button()
        self.brocardi_buttons_frame = ttkb.Frame(self.mainframe)
        self.brocardi_buttons_frame.grid(row=13, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)
        self.brocardi_link_button = ttkb.Button(self.mainframe, text="Apri in Brocardi")
        self.brocardi_link_button.grid(row=1, column=3, sticky="ew", padx=5, pady=5)
        self.brocardi_link_button.grid_remove()
        self.configure_mainframe()
    
# ==============================================================================
# Main Frame Configuration
# Description: Configures the layout and geometry of the main application frame.
# ==============================================================================
    def configure_mainframe(self):
        self.mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Get the number of columns and rows currently in use
        cols, rows = self.mainframe.grid_size()

        # Configure weight for each column in use
        for col in range(cols):
            self.mainframe.columnconfigure(col, weight=1)

        # Configure weight for each row in use
        for row in range(rows):
            self.mainframe.rowconfigure(row, weight=1)

# ==============================================================================
# Input Widgets
# Description: Creates and configures input widgets for user data entry.
# ==============================================================================          
    def create_brocardi_toggle_button(self):
        # Utilizza lo stile predefinito di ttk.Checkbutton
        self.brocardi_var = BooleanVar(value=self.brocardi_but)  # Crea la variabile di controllo
        self.brocardi_toggle_button = ttkb.Checkbutton(
            self.mainframe, text="Brocardi",
            variable=self.brocardi_var,  # Associa la variabile di controllo al Checkbutton
            onvalue=True, offvalue=False,  # Imposta i valori per gli stati selezionato e deselezionato
            command=self.toggle_brocardi,  # Chiama toggle_brocardi quando il Checkbutton viene cliccato
            bootstyle='primary'  # Usa lo stile primary per un colore di base
        )
        self.brocardi_toggle_button.grid(row=2, column=4, sticky='ew', padx=10, pady=10)

    def create_input_widgets(self):
        # Create input fields with labels and tooltips if necessary
        
        act_type_label = ttkb.Label(self.mainframe, text="Tipo atto:", bootstyle=INFO)
        act_type_label.grid(row=0, column=0, sticky=tk.W, padx=2, pady=2)

        act_types = [
            'legge', 'decreto legge', 'decreto legislativo', 'costituzione', 'd.p.r.', 'TUE', 'TFUE', 'CDFUE','regio decreto',
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
        self.act_type_combobox = self.create_combobox(container=self.mainframe, values=act_types, default_text="Select", row=0, column=1, style='act.TCombobox')
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
        pos_operations = [
            ("Estrai dati", self.fetch_act_data, 8, 0),
        ]
        for text, command, row, column in pos_operations:
            ttkb.Button(self.mainframe, text=text, command=command, bootstyle="success-outline").grid(row=row, column=column, sticky=(W, E), padx=4, pady=4)

        neg_operations = [
            ('Interrompi estrazione', self.break_progress, 8, 1),
        ]
        for text, command, row, column in neg_operations:
            ttkb.Button(self.mainframe, text=text, command=command, bootstyle="danger").grid(row=row, column=column, sticky=(W, E), padx=4, pady=4)
    
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
        self.output_text.grid(row=9, column=0, columnspan=6, rowspan=4, sticky=(tk.N, tk.S, tk.W, tk.E), pady=(10,0))

        operations = [
            ("Salva come XML", self.save_as_xml, 14, 0),
            ("Cancella", lambda: self.clear_all_fields([self.date_entry, self.act_number_entry, self.article_entry, self.act_type_combobox], self.act_type_combobox), 14, 2),
            ("Copia Testo", self.copia_output, 14, 4)
        ]
        
        # Use a consistent padx to space out the buttons horizontally
        button_padx = (20, 20)  # Increase the spacing between buttons by adjusting these values
        # Align the buttons to the west and east within their grid cells to distribute them evenly
        for text, command, row, column in operations:
            button = ttkb.Button(self.mainframe, text=text, command=command, bootstyle="success-outline")
            button.grid(row=row, column=column, columnspan=2, sticky=(tk.W, tk.E), padx=button_padx)

    def create_history_buttons(self):
        # Create buttons related to history operations
        history_ops = [
            ("Cronologia", self.apri_finestra_cronologia, 0),
            ("Salva cronologia", self.salva_cronologia, 2),
            ("Carica cronologia", self.carica_cronologia, 4)  # Changed from 3 to 4 to add more space
        ]
        button_padx = (20, 20)  # Horizontal padding to add space between buttons
        pady_between_rows = 20  # Vertical padding to add space between the rows of buttons
        
        for text, command, column in history_ops:
            button = ttkb.Button(self.mainframe, text=text, command=command)
            button.grid(row=15, column=column, sticky="ew", padx=button_padx)
        
        # Add padding below the 'Cronologia' button to add vertical spacing
        self.mainframe.grid_rowconfigure(14, pad=pady_between_rows)
      
    def create_labeled_entry(self, label_text, placeholder, row, width=None, increment=False):
        # Create and place the label for the entry
        label = ttkb.Label(self.mainframe, text=label_text, bootstyle='info')
        label.grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)

        # Create the entry widget
        entry = ttkb.Entry(self.mainframe, width=width)
        # Adjust columnspan if increment is True, place the Entry right next to the increment buttons
        entry.grid(row=row, column=1, columnspan=2 if increment else 3, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Attach a tooltip to the entry widget
        self.create_tooltip(entry, placeholder)  # Assuming create_tooltip is correctly implemented

        if increment:
            # Frame to hold both increment buttons, this keeps them together
            inc_dec_frame = ttkb.Frame(self.mainframe)
            # Reduce the padx to bring the frame closer to the Entry
            inc_dec_frame.grid(row=row, column=3, sticky=tk.W, padx=(0, 5))

            # Buttons for incrementing and decrementing the value
            inc_button = ttkb.Button(inc_dec_frame, text="▲", bootstyle="outline", command=lambda: self.increment_entry(entry))
            dec_button = ttkb.Button(inc_dec_frame, text="▼", bootstyle="outline", command=lambda: self.decrement_entry(entry))
            # No padding needed as they are inside the frame which is already positioned
            inc_button.pack(side=tk.LEFT)
            dec_button.pack(side=tk.LEFT)

        return entry
 
    def create_progress_bar(self):
        self.progress_bar = ttkb.Progressbar(self.mainframe, orient="horizontal", length=300, mode='determinate', style='success.Striped.Horizontal.TProgressbar')
        self.progress_bar.grid(row=16, column=0, columnspan=4, pady=10, padx=5, sticky="ew")

    def break_progress(self, e=None):
        # Stop the progress bar first
        self.progress_bar.stop()
        # Try to close the driver safely; handle any exceptions that might occur
        try:
            self.close_driver_safely()
        except Exception as exc:
            messagebox.showerror("Errore di Chiusura", f"Non è stato possibile chiudere il driver correttamente: {exc}")
        
        # Set up the driver again, handling potential errors
        try:
            self.setup_driver()
        except Exception as exc:
            messagebox.showerror("Errore di Avvio", f"Impossibile riavviare il driver: {exc}")
            return  # Exit the function if the driver cannot be restarted
        
        # Display a warning message about the interruption
        if e:
            messagebox.showwarning("Progresso", f"Ricerca interrotta: {e}")
        #else:
            messagebox.showwarning("Progresso", "La ricerca è stata interrotta.")

    def toggle_brocardi(self):
        # Questa funzione verrà chiamata ogni volta che il Checkbutton viene cliccato
        # Aggiorna il valore della variabile di controllo brocardi_but basato sul valore di brocardi_var
        self.brocardi_but = self.brocardi_var.get()  # Ottiene il valore corrente della variabile di controllo
        print(f"Stato dei Brocardi: {'attivato' if self.brocardi_but else 'disattivato'}")







# ==============================================================================
# Function Definitions
# Description: Contains all key functional operations that handle data manipulation, 
# user interaction, and application behavior.
# ==============================================================================

# ==============================================================================
# Open README
# Description: Opens the GitHub README page in a default web browser.
# ==============================================================================
    def apri_readme(self):
        github_url = "https://github.com/capazme/NormaScraperApp"
        webbrowser.open(github_url)

# ==============================================================================
# Increment Entry
# Description: Increases the numeric value in an entry field.
# ==============================================================================
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
            try:
                self.fetch_act_data()
            except Exception as e:
                self.break_progress(e)

# ==============================================================================
# Decrement Entry
# Description: Decreases the numeric value in an entry field.
# ==============================================================================
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
            try:
                self.fetch_act_data()
            except Exception as e:
                self.break_progress(e)

# ==============================================================================
# Toggle Extension Frame
# Description: Shows or hides additional UI components dynamically.
# ==============================================================================
    def toggle_extension(self):
        """Mostra o nasconde il frame dell'estensione."""
        if self.extension_frame.winfo_viewable():
            self.extension_frame.grid_forget()
            self.toggle_extension_btn.config(text="▼")
        else:
            self.extension_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E))
            self.toggle_extension_btn.config(text="▲") 

# ==============================================================================
# Copy Output to Clipboard
# Description: Copies the content of the output text area to the clipboard.
# ==============================================================================
    def copia_output(self):
        content = self.output_text.get("1.0", tk.END)
        pyperclip.copy(content)
        messagebox.showinfo("Copia", "Testo copiato negli appunti!")

# ==============================================================================
# Open URL
# Description: Opens a specified URL in a new browser tab.
# ==============================================================================
    def apri_url(self, url):
        webbrowser.open_new_tab(url)

# ==============================================================================
# Clear All Fields
# Description: Resets all input fields and dropdowns to their default states.
# ==============================================================================
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

# ==============================================================================
# XML Saving Functionality
# Description: Handles saving of data in XML format based on user input.
# ==============================================================================
    def save_as_xml(self):
        file_path = filedialog.asksaveasfilename(
            title="Salva come XML",
            initialdir="/",
            filetypes=[("XML files", "*.xml")],
            defaultextension=".xml"
        )
        if file_path:
            try:
                self.fetch_act_data(save_xml_path=file_path)
            except Exception as e:
                self.break_progress(e)

# ==============================================================================
# History Management
# Description: Methods related to managing and manipulating the history of searches
# and norm data within the application.
# ==============================================================================

# ==============================================================================
# Add to History
# Description: Adds a new norm to the history, ensuring the history does not exceed
# a maximum size limit.
# ==============================================================================
    def aggiungi_a_cronologia(self, norma):
        # Controlla la dimensione massima della cronologia e aggiunge una nuova norma
        if len(self.cronologia) >= 50:
            self.cronologia.pop(0)
        if norma not in self.cronologia:
            self.cronologia.append(norma)

# ==============================================================================
# Open History Window
# Description: Opens a new window displaying the history of searched norms, allowing
# for interaction and re-querying of historical data.
# ==============================================================================
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

# ==============================================================================
# Item Click Event Handler
# Description: Handles the click event on history items, allowing actions such as
# re-querying or opening related URLs.
# ==============================================================================
    def on_item_clicked(self, event):
        col = self.tree.identify_column(event.x)
        item_id = self.tree.selection()[0]
        norma = self.tree_items.get(item_id)
        
        if col == '#1' and norma:  # Clic su "Dato normativo"
            self.ripeti_ricerca_selezionata(norma)
        elif col == '#2' and norma.url:  # Clic su "URL"
            webbrowser.open_new_tab(norma.url)

# ==============================================================================
# Repeat Selected Search
# Description: Repeats a previously selected search from history.
# ==============================================================================
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

# ==============================================================================
# Save History
# Description: Saves the current history to a file selected by the user.
# ==============================================================================
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

# ==============================================================================
# Load History
# Description: Loads history from a file selected by the user.
# ==============================================================================
    def carica_cronologia(self):
        dir_cronologia = os.path.join(CURRENT_APP_PATH, "Resources", "Frameworks", "usr", "cron")
        
        percorso_file = filedialog.askopenfilename(title="Seleziona file cronologia", filetypes=(("JSON files", "*.json"), ("all files", "*.*"),), initialdir=dir_cronologia)
        if percorso_file:
            with open(percorso_file, 'r') as f:
                self.cronologia = [sys_op.NormaVisitata.from_dict(n) for n in json.load(f)]
            messagebox.showinfo("Caricato", "Cronologia caricata con successo")
            self.apri_finestra_cronologia()

# ==============================================================================
# Clear History
# Description: Clears all entries from the current history.
# ==============================================================================
    def cancella_cronologia(self):
        # Pulisce la cronologia
        if len(self.cronologia)>0:
            self.tree.delete(*self.tree.get_children())
            self.cronologia.clear()
            messagebox.showinfo("Cronologia", "Cronologia pulita con successo.")

# ==============================================================================
# Data Fetching
# Description: Manages the fetching of legal document data from external sources.
# ==============================================================================
    def fetch_act_data(self, save_xml_path=None):
        try:
            threading.Thread(target=self._fetch_act_data, args=(save_xml_path,), daemon=True).start()
        except Exception as e:
            self.break_progress(e)

# ==============================================================================
# Private Data Fetching
# Description: Performs the actual data fetching operations in a separate thread.
# ==============================================================================
    def _fetch_act_data(self, save_xml_path=None):
        # Avvia la barra di progresso nel thread principale

        act_type = self.act_type_combobox.get()  
        date = self.date_entry.get()
        act_number = self.act_number_entry.get()
        article = self.article_entry.get()
        version = self.version_var.get()
        version_date = self.version_date_entry.get()
        comma = self.comma_entry.get()
        
        if save_xml_path:
            article = None
        
        try:
            self.root.after(50, self.progress_bar.start)
            data, url, norma = sys_op.get_urn_and_extract_data(act_type=act_type, date=date, act_number=act_number, article=article, comma=comma, version=version, version_date=version_date, save_xml_path=save_xml_path)
            self.root.after(5, self.progress_bar.stop)
            self.root.after(5, lambda: self.display_results(data, url, norma, brocardi=self.brocardi))
        except Exception as e:
            self.root.after(5, lambda: self.break_progress)
            self.root.after(5, lambda error=e :messagebox.showerror("Errore", error))
            return e

# ==============================================================================
# Display Results
# Description: Displays the fetched data and related actions in the GUI.
# ==============================================================================
    def display_results(self, data, url, norma, brocardi = False):
        self.root.after(50, self.progress_bar.stop)
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, data)
        self.crea_link("Apri URL", url, 8, 2)
        self.aggiungi_a_cronologia(norma)
        if self.brocardi_but == True:
            self.check_brocardi(norma)

# ==============================================================================
# Create Hyperlink
# Description: Creates a clickable hyperlink in the output area.
# ==============================================================================                  
    def crea_link(self, text, url, row, column):
        link = tk.Label(self.mainframe, text=text, fg="blue", cursor="hand2")
        link.bind("<Button-1>", lambda e: self.apri_url(url))
        link.grid(row=row, column=column)

# ==============================================================================
# Brocardi Information Handling
# Description: Manages the retrieval and display of brocardi information based on the legal norm.
# ==============================================================================  
    def check_brocardi(self, norma):
        result = self.brocardi.get_info(norma)
        # Assicurarsi che result sia una tupla con due elementi prima di accedere
        if result == False:
            return False
        elif len(result) >= 2 and isinstance(result, tuple):
            self.output_text.insert(tk.END, result[0])
            if result[2]:  # Se c'è un URL, mostra il bottone per il link
                self.brocardi_link_button.grid()  # Mostra il pulsante
                self.brocardi_link_button.configure(command=lambda: self.apri_url(result[2]))

            #print(result[1])
            if result[1]:  # Se ci sono dati per i bottoni brocardi
                # Ritarda la creazione dei bottoni per assicurarsi che tutto il resto sia aggiornato
                self.root.after(100, lambda: self.create_brocardi_buttons(result[1]))
        else:
            return False

# ==============================================================================
# Dynamic Button Creation for Brocardi Details
# Description: Dynamically creates buttons for each brocardi detail in a Toplevel window.
# ==============================================================================
    def create_brocardi_buttons(self, data):
        """Create dynamic buttons based on the data dictionary in a Toplevel window."""
        # Check if a Toplevel already exists, if yes, clear it, otherwise create a new one
        if hasattr(self, 'brocardi_toplevel') and self.brocardi_toplevel.winfo_exists():
            # Clear existing buttons
            for widget in self.brocardi_toplevel.winfo_children():
                widget.destroy()
        else:
            # Create a new Toplevel window
            self.brocardi_toplevel = tk.Toplevel(self.root)
            self.brocardi_toplevel.title("Dettagli Brocardi")

        # Dynamically create buttons inside the Toplevel window
        row = 0
        for key, value in data.items():
            if value:
                # Utilizzare una funzione interna per creare una chiusura e catturare correttamente i valori
                def make_command(v, k):
                    return lambda: self.create_value_window(v, k)
                
                button = ttkb.Button(self.brocardi_toplevel, text=f"{key}", command=make_command(value, key))
                button.grid(row=row, column=0, sticky="ew", padx=5, pady=5)
                self.brocardi_toplevel.grid_columnconfigure(0, weight=1)
                row += 1


        # Adjust window size automatically to fit contents
        self.brocardi_toplevel.resizable(width=True, height=True)  # Allow resizing if necessary
        self.brocardi_toplevel.geometry("")  # Clear any fixed geometry settings

        # Lift the Toplevel window to make sure it is on top
        self.brocardi_toplevel.lift()
        self.brocardi_toplevel.attributes('-topmost', True)  # Ensure it stays on top until focus is changed
        self.brocardi_toplevel.after(1000, lambda: self.brocardi_toplevel.attributes('-topmost', False))  # Revert 'always on top' after 1 second

# ==============================================================================
# Value Display Window
# Description: Creates a new window to display detailed values for a selected brocardi.
# ==============================================================================
    def create_value_window(self, value, key):
        # Questa funzione crea una nuova finestra per mostrare il valore
        top = Toplevel(self.root)
        top.title(f"{key}")
        
        # Assicurati che la finestra appaia al primo livello
        top.attributes('-topmost', True)

        # Prepara il testo in base al tipo di valore
        if isinstance(value, list):
            # Se il valore è una lista, uniscila in una stringa con newline come separatore e una linea di separazione tra gli elementi
            value_str = '\n'.join(f"{item}\n__________________" for item in value[:-1]) + f"\n{value[-1]}" if value else ""
        elif isinstance(value, dict):
            # Se è un dizionario, formatta come chiave: valore
            value_str = '\n'.join(f"{key}: {val}\n__________________" for key, val in value.items())
        else:
            # Altrimenti, converti direttamente il valore in una stringa
            value_str = str(value)

        # Utilizza ScrolledText per mostrare il valore
        text_area = ttkb.ScrolledText(top, wrap='word', height=10, width=50)
        text_area.pack(padx=10, pady=10, fill='both', expand=True)
        text_area.insert('1.0', value_str)
        text_area.config(state='disabled')  # Rendi il testo non modificabile

        # Dopo un certo intervallo, rimuovi il flag 'topmost' per permettere alla finestra di andare in background se necessario
        top.after(5000, lambda: top.attributes('-topmost', False))

# ==============================================================================
# Menu Configuration
# Description: Configures the menu bar for the application, including file operations
# and accessibility options.
# ==============================================================================
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

# ==============================================================================
# Application Configuration Dialog
# Description: Opens a configuration dialog for application settings.
# ==============================================================================
    def apri_configurazione(self):
        ConfigurazioneDialog(self.root)

# ==============================================================================
# Application Control Functions
# Description: Contains various utility functions to control application behavior 
# such as restarting, exiting, and adjusting the UI theme and text size.
# ==============================================================================
    def restart_app(self):
        """Restart the app."""
        self.on_exit()
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def apply_normal_theme(self):
        """Apply normal theme for default visibility."""
        self.style.configure('TButton', background='SystemButtonFace', foreground='SystemButtonText')

    def on_exit(self):
        if messagebox.askokcancel("Uscire", "Sei sicuro di voler uscire?"):
            self.break_progress()
            self.close_driver_safely(close=True)

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