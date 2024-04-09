act_types  = {
    "decreto legge": "decreto.legge",
    "decreto legislativo": "decreto.legislativo",
    "d.lgs.":"decreto.legislativo",
    "dlgs": "decreto.legislativo",
    "dl": "decreto.legge",
    "legge": "legge",
    "l": "legge",
    "l.": "legge",
    "costituzione":"costituzione",
    "cost": "costituzione",
    "cost.": "costituzione",
    "c.": "costituzione",
    "cc": "codice civile",
    "c.c.": "codice civile",
    "codice civile":"codice civile",
    "cod. civ.": "codice civile",
    "disp. prel.": "preleggi",
    "preleggi": "preleggi",
    "prel.": "preleggi",
    "codice penale":"codice penale",
    "cp": "codice penale",
    "c.p.": "codice penale",
    "cod. pen.": "codice penale",
    "codice di procedura civile":"codice di procedura civile",
    "cpc": "codice di procedura civile",
    "c.p.c": "codice di procedura civile",
    "cod. proc. civ": "codice di procedura civile",
    "codice di procedura penale":"codice di procedura penale",
    "cpp": "codice di procedura penale",
    "c.p.p.": "codice di procedura penale",
    "cod. proc. pen.": "codice di procedura penale",
    "cn": "codice della navigazione",
    "cod. nav.": "codice della navigazione",
    "cpet": "codice postale e delle telecomunicazioni",
    "cod. post. telecom.": "codice postale e delle telecomunicazioni",
    "cds": "codice della strada",
    "cod. strada": "codice della strada",
    "cpt": "codice del processo tributario",
    "cod. proc. trib.": "codice del processo tributario",
    "cpd": "codice in materia di protezione dei dati personali",
    "cod. prot. dati": "codice in materia di protezione dei dati personali",
    "cce": "codice delle comunicazioni elettroniche",
    "cod. com. elet.": "codice delle comunicazioni elettroniche",
    "cbc": "codice dei beni culturali e del paesaggio",
    "cod. beni cult.": "codice dei beni culturali e del paesaggio",
    "cpi": "codice della proprietà industriale",
    "cod. prop. ind.": "codice della proprietà industriale",
    "cad": "codice dell'amministrazione digitale",
    "cod. amm. dig.": "codice dell'amministrazione digitale",
    "cnd": "codice della nautica da diporto",
    "cod. naut. diport.": "codice della nautica da diporto",
    "cdc": "codice del consumo",
    "cod. consumo": "codice del consumo",
    "cap": "codice delle assicurazioni private",
    "cod. ass. priv.": "codice delle assicurazioni private",
    "camb": "norme in materia ambientale",
    "norme amb.": "norme in materia ambientale",
    "ccp": "codice dei contratti pubblici",
    "cod. contr. pubb.": "codice dei contratti pubblici",
    "cpo": "codice delle pari opportunità",
    "cod. pari opp.": "codice delle pari opportunità",
    "com": "codice dell'ordinamento militare",
    "cod. ord. mil.": "codice dell'ordinamento militare",
    "cpa": "codice del processo amministrativo",
    "cod. proc. amm.": "codice del processo amministrativo",
    "ctu": "codice del turismo",
    "cod. turismo": "codice del turismo",
    "cam": "codice antimafia",
    "cod. antimafia": "codice antimafia",
    "cgco": "codice di giustizia contabile",
    "cod. giust. cont.": "codice di giustizia contabile",
    "cts": "codice del Terzo settore",
    "cod. ter. sett.": "codice del Terzo settore",
    "cdpc": "codice della protezione civile",
    "cod. prot. civ.": "codice della protezione civile",
    "cci": "codice della crisi d'impresa e dell'insolvenza",
    "cod. crisi imp.": "codice della crisi d'impresa e dell'insolvenza",
    "disp. att. c.c.": "disposizioni per l'attuazione del Codice civile e disposizioni transitorie",
    "disp. att. c.p.c.": "disposizioni per l'attuazione del Codice di procedura civile e disposizioni transitorie"
}

# Estrai i valori unici dal dizionario
valori_unici = set(act_types.values())

# Controlla e aggiunge le mappature mancanti
for valore in valori_unici:
    if valore not in act_types:
        act_types[valore] = valore

# Verifica (dopo l'aggiunta) che ogni valore unico nel dizionario abbia una chiave corrispondente che mappa a se stesso
for valore in valori_unici:
    if act_types[valore] != valore:
        print(f"Errore di mappatura per: {valore}")
    else:
        print(f"Mappatura corretta per: {valore}")

# Stampa il dizionario aggiornato per confermare le aggiunte
print("\nDizionario aggiornato:")
for chiave, valore in sorted(act_types.items()):
    print(f'"{chiave}": "{valore}",')
