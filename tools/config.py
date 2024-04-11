import yaml
import tkinter as tk 
import ttkbootstrap as ttkb

class ConfigurazioneDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # Salva l'istanza parent per accesso futuro
        self.configurazioni = self.carica_configurazioni()

        self.init_ui()

    def init_ui(self):
        self.geometry("400x300")  
        self.title("Configurazione")

        self.create_widgets()
        self.place_widgets()

        self.grid_columnconfigure(1, weight=1)
        self.resizable(False, False)

    def create_widgets(self):
        self.tipo_atto_label = ttkb.Label(self, text="Tipo di Atto Preferito:")
        self.tipo_atto_var = tk.StringVar(value=self.configurazioni.get("ultimo_tipo_atto", ""))
        self.tipo_atto_entry = ttkb.Entry(self, textvariable=self.tipo_atto_var)

        self.dimensione_font_label = ttkb.Label(self, text="Dimensione del Font:")
        self.dimensione_font_var = tk.IntVar(value=self.configurazioni.get("ultima_dimensione_font", 15))
        self.dimensione_font_spinbox = ttkb.Spinbox(self, from_=10, to_=24, textvariable=self.dimensione_font_var)

        self.tema_label = ttkb.Label(self, text="Tema:")
        self.tema_var = tk.StringVar(value=self.configurazioni.get("ultimo_tema", "normale"))
        self.tema_combobox = ttkb.Combobox(self, textvariable=self.tema_var, values=["normale", "scuro", "alto contrasto"])

        self.lingua_label = ttkb.Label(self, text="Lingua:")
        self.lingua_var = tk.StringVar(value=self.configurazioni.get("lingua", "Italiano"))
        self.lingua_combobox = ttkb.Combobox(self, textvariable=self.lingua_var, values=["Italiano", "English"])

        self.notifiche_label = ttkb.Label(self, text="Notifiche:")
        self.notifiche_var = tk.BooleanVar(value=self.configurazioni.get("notifiche", True))
        self.notifiche_checkbutton = ttkb.Checkbutton(self, text="Abilita Notifiche", variable=self.notifiche_var)

        self.salvataggio_label = ttkb.Label(self, text="Salvataggio Automatico Ricerche:")
        self.salvataggio_automatico_var = tk.BooleanVar(value=self.configurazioni.get("salvataggio_automatico", True))
        self.salvataggio_automatico_checkbutton = ttkb.Checkbutton(self, text="Abilita Salvataggio Automatico", variable=self.salvataggio_automatico_var)

        self.cronologia_label = ttkb.Label(self, text="Elementi Cronologia Ricerche:")
        self.cronologia_ricerche_var = tk.IntVar(value=self.configurazioni.get("cronologia_ricerche", 50))
        self.cronologia_ricerche_spinbox = ttkb.Spinbox(self, from_=0, to_=100, textvariable=self.cronologia_ricerche_var)

        self.salva_button = ttkb.Button(self, text="Salva", command=self.salva_configurazioni)

    def place_widgets(self):
        self.tipo_atto_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.tipo_atto_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        self.dimensione_font_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.dimensione_font_spinbox.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)

        self.tema_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.tema_combobox.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)

        self.lingua_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.lingua_combobox.grid(row=3, column=1, sticky=tk.EW, padx=5, pady=5)

        self.notifiche_label.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.notifiche_checkbutton.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)

        self.salvataggio_label.grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.salvataggio_automatico_checkbutton.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)

        self.cronologia_label.grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        self.cronologia_ricerche_spinbox.grid(row=6, column=1, sticky=tk.EW, padx=5, pady=5)

        self.salva_button.grid(row=7, column=0, columnspan=2, pady=10)

    def carica_configurazioni(self):
        try:
            with open('resources/configurazione.yaml', 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            return {}

    def salva_configurazioni(self):
        configurazioni = {
            "ultimo_tipo_atto": self.tipo_atto_var.get(),
            "ultima_dimensione_font": self.dimensione_font_var.get(),
            "ultimo_tema": self.tema_var.get(),
            "lingua": self.lingua_var.get(),
            "notifiche": self.notifiche_var.get(),
            "salvataggio_automatico": self.salvataggio_automatico_var.get(),
            "cronologia_ricerche": self.cronologia_ricerche_var.get(),
        }
        with open('resources/configurazione.yaml', 'w') as file:
            yaml.dump(configurazioni, file, default_flow_style=False)
        self.destroy()