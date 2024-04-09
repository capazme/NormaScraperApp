 
newlist =[]
act_types = [
    "Costituzione",
    "Codice Civile",
    "Preleggi",
    "Codice Penale",
    "Codice di Procedura Civile",
    "Codice di Procedura Penale",
    "Codice della Navigazione",
    "Codice Postale e delle Telecomunicazioni",
    "Codice della Strada",
    "Codice del Processo Tributario",
    "Codice in Materia di Protezione dei Dati Personali",
    "Codice delle Comunicazioni Elettroniche",
    "Codice dei Beni Culturali e del Paesaggio",
    "Codice della Proprietà Industriale",
    "Codice dell'Amministrazione Digitale",
    "Codice della Nautica da Diporto",
    "Codice del Consumo",
    "Codice delle Assicurazioni Private",
    "Norme in Materia Ambientale",
    "Codice dei Contratti Pubblici",
    "Codice delle Pari Opportunità",
    "Codice dell'Ordinamento Militare",
    "Codice del Processo Amministrativo",
    "Codice del Turismo",
    "Codice Antimafia",
    "Codice di Giustizia Contabile",
    "Codice del Terzo Settore",
    "Codice della Protezione Civile",
    "Codice della Crisi d'Impresa e dell'Insolvenza"
]
for val in act_types:
    newlist.append(val.lower())

print(newlist)