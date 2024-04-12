from bs4 import BeautifulSoup
import re
import datetime
from functools import lru_cache

def nospazi(text):
    textlist = text.split()
    for t in textlist:
        t.strip
    textout = ' '.join(textlist)
    return textout

def parse_date(input_date):
    """
    Converte una stringa di data in formato esteso o YYYY-MM-DD al formato YYYY-MM-DD.
    Supporta mesi in italiano.
    """
    month_map = {
        "gennaio": "01", "febbraio": "02", "marzo": "03", "aprile": "04",
        "maggio": "05", "giugno": "06", "luglio": "07", "agosto": "08",
        "settembre": "09", "ottobre": "10", "novembre": "11", "dicembre": "12"
    }

    # Tenta la conversione per formati con mesi per esteso
    pattern = r"(\d{1,2})\s+([a-zA-Z]+)\s+(\d{4})"
    match = re.search(pattern, input_date)
    if match:
        day, month, year = match.groups()
        month = month_map.get(month.lower())
        if not month:
            raise ValueError("Mese non valido")
        return f"{year}-{month}-{day.zfill(2)}"
    
    # Gestione del formato standard YYYY-MM-DD
    try:
        datetime.datetime.strptime(input_date, "%Y-%m-%d")
        return input_date
    except ValueError:
        raise ValueError("Formato data non valido")

def normalize_act_type(input_type, search = False):
    """
    Normalizes the type of legislative act based on a variable input.
    """
    if search==True:
            act_types  = {
        "d.lgs.": "decreto legislativo",
        "decreto legge": "decreto legge",
        "decreto legislativo": "decreto legislativo",
        "decreto.legge": "decreto legge",
        "decreto.legislativo": "decreto legislativo",
        "dl": "decreto legge",
        "dlgs": "decreto legislativo",
        "l": "legge",
        "l.": "legge",
        "legge": "legge",
        "c.c.": "codice civile",
        "c.p.": "codice penale",
        "c.p.c": "codice di procedura civile",
        "c.p.p.": "codice di procedura penale",
        "cad": "codice dell'amministrazione digitale",
        "cam": "codice antimafia",
        "camb": "norme in materia ambientale",
        "cap": "codice delle assicurazioni private",
        "cbc": "codice dei beni culturali e del paesaggio",
        "cc": "codice civile",
        "cce": "codice delle comunicazioni elettroniche",
        "cci": "codice della crisi d'impresa e dell'insolvenza",
        "ccp": "codice dei contratti pubblici",
        "cdc": "codice del consumo",
        "cdpc": "codice della protezione civile",
        "cds": "codice della strada",
        "cgco": "codice di giustizia contabile",
        "cn": "codice della navigazione",
        "cnd": "codice della nautica da diporto",
        "cod. amm. dig.": "codice dell'amministrazione digitale",
        "cod. antimafia": "codice antimafia",
        "cod. ass. priv.": "codice delle assicurazioni private",
        "cod. beni cult.": "codice dei beni culturali e del paesaggio",
        "cod. civ.": "codice civile",
        "cod. com. elet.": "codice delle comunicazioni elettroniche",
        "cod. consumo": "codice del consumo",
        "cod. contr. pubb.": "codice dei contratti pubblici",
        "cod. crisi imp.": "codice della crisi d'impresa e dell'insolvenza",
        "cod. giust. cont.": "codice di giustizia contabile",
        "cod. naut. diport.": "codice della nautica da diporto",
        "cod. nav.": "codice della navigazione",
        "cod. ord. mil.": "codice dell'ordinamento militare",
        "cod. pari opp.": "codice delle pari opportunità",
        "cod. pen.": "codice penale",
        "cod. post. telecom.": "codice postale e delle telecomunicazioni",
        "cod. proc. amm.": "codice del processo amministrativo",
        "cod. proc. civ": "codice di procedura civile",
        "cod. proc. pen.": "codice di procedura penale",
        "cod. proc. trib.": "codice del processo tributario",
        "cod. prop. ind.": "codice della proprietà industriale",
        "cod. prot. civ.": "codice della protezione civile",
        "cod. prot. dati": "codice in materia di protezione dei dati personali",
        "cod. strada": "codice della strada",
        "cod. ter. sett.": "codice del Terzo settore",
        "cod. turismo": "codice del turismo",
        "codice antimafia": "codice antimafia",
        "codice civile": "codice civile",
        "codice dei beni culturali e del paesaggio": "codice dei beni culturali e del paesaggio",
        "codice dei contratti pubblici": "codice dei contratti pubblici",
        "codice del Terzo settore": "codice del Terzo settore",
        "codice del consumo": "codice del consumo",
        "codice del processo amministrativo": "codice del processo amministrativo",
        "codice del processo tributario": "codice del processo tributario",
        "codice del turismo": "codice del turismo",
        "codice dell'amministrazione digitale": "codice dell'amministrazione digitale",
        "codice dell'ordinamento militare": "codice dell'ordinamento militare",
        "codice della crisi d'impresa e dell'insolvenza": "codice della crisi d'impresa e dell'insolvenza",
        "codice della nautica da diporto": "codice della nautica da diporto",
        "codice della navigazione": "codice della navigazione",
        "codice della proprietà industriale": "codice della proprietà industriale",
        "codice della protezione civile": "codice della protezione civile",
        "codice della strada": "codice della strada",
        "codice delle assicurazioni private": "codice delle assicurazioni private",
        "codice delle comunicazioni elettroniche": "codice delle comunicazioni elettroniche",
        "codice delle pari opportunità": "codice delle pari opportunità",
        "codice di giustizia contabile": "codice di giustizia contabile",
        "codice di procedura civile": "codice di procedura civile",
        "codice di procedura penale": "codice di procedura penale",
        "codice in materia di protezione dei dati personali": "codice in materia di protezione dei dati personali",
        "codice penale": "codice penale",
        "codice postale e delle telecomunicazioni": "codice postale e delle telecomunicazioni",
        "com": "codice dell'ordinamento militare",
        "cost": "costituzione",
        "cost.": "costituzione",
        "costituzione": "costituzione",
        "cp": "codice penale",
        "cpa": "codice del processo amministrativo",
        "cpc": "codice di procedura civile",
        "cpd": "codice in materia di protezione dei dati personali",
        "cpet": "codice postale e delle telecomunicazioni",
        "cpi": "codice della proprietà industriale",
        "cpo": "codice delle pari opportunità",
        "cpp": "codice di procedura penale",
        "cpt": "codice del processo tributario",
        "cts": "codice del Terzo settore",
        "ctu": "codice del turismo",
        "disp. att. c.c.": "disposizioni per l'attuazione del Codice civile e disposizioni transitorie",
        "disp. att. c.p.c.": "disposizioni per l'attuazione del Codice di procedura civile e disposizioni transitorie",
        "disp. prel.": "preleggi",
        "disposizioni per l'attuazione del Codice civile e disposizioni transitorie": "disposizioni per l'attuazione del Codice civile e disposizioni transitorie",
        "disposizioni per l'attuazione del Codice di procedura civile e disposizioni transitorie": "disposizioni per l'attuazione del Codice di procedura civile e disposizioni transitorie",
        "norme amb.": "norme in materia ambientale",
        "norme in materia ambientale": "norme in materia ambientale",
        "prel.": "preleggi",
        "preleggi": "preleggi"}
    elif search==False:
        act_types  = {
        "d.lgs.": "decreto.legislativo",
        "decreto legge": "decreto.legge",
        "decreto legislativo": "decreto.legislativo",
        "decreto.legge": "decreto.legge",
        "decreto.legislativo": "decreto.legislativo",
        "dl": "decreto.legge",
        "dlgs": "decreto.legislativo",
        "l": "legge",
        "l.": "legge",
        "legge": "legge",
        "c.c.": "codice civile",
        "c.p.": "codice penale",
        "c.p.c": "codice di procedura civile",
        "c.p.p.": "codice di procedura penale",
        "cad": "codice dell'amministrazione digitale",
        "cam": "codice antimafia",
        "camb": "norme in materia ambientale",
        "cap": "codice delle assicurazioni private",
        "cbc": "codice dei beni culturali e del paesaggio",
        "cc": "codice civile",
        "cce": "codice delle comunicazioni elettroniche",
        "cci": "codice della crisi d'impresa e dell'insolvenza",
        "ccp": "codice dei contratti pubblici",
        "cdc": "codice del consumo",
        "cdpc": "codice della protezione civile",
        "cds": "codice della strada",
        "cgco": "codice di giustizia contabile",
        "cn": "codice della navigazione",
        "cnd": "codice della nautica da diporto",
        "cod. amm. dig.": "codice dell'amministrazione digitale",
        "cod. antimafia": "codice antimafia",
        "cod. ass. priv.": "codice delle assicurazioni private",
        "cod. beni cult.": "codice dei beni culturali e del paesaggio",
        "cod. civ.": "codice civile",
        "cod. com. elet.": "codice delle comunicazioni elettroniche",
        "cod. consumo": "codice del consumo",
        "cod. contr. pubb.": "codice dei contratti pubblici",
        "cod. crisi imp.": "codice della crisi d'impresa e dell'insolvenza",
        "cod. giust. cont.": "codice di giustizia contabile",
        "cod. naut. diport.": "codice della nautica da diporto",
        "cod. nav.": "codice della navigazione",
        "cod. ord. mil.": "codice dell'ordinamento militare",
        "cod. pari opp.": "codice delle pari opportunità",
        "cod. pen.": "codice penale",
        "cod. post. telecom.": "codice postale e delle telecomunicazioni",
        "cod. proc. amm.": "codice del processo amministrativo",
        "cod. proc. civ": "codice di procedura civile",
        "cod. proc. pen.": "codice di procedura penale",
        "cod. proc. trib.": "codice del processo tributario",
        "cod. prop. ind.": "codice della proprietà industriale",
        "cod. prot. civ.": "codice della protezione civile",
        "cod. prot. dati": "codice in materia di protezione dei dati personali",
        "cod. strada": "codice della strada",
        "cod. ter. sett.": "codice del Terzo settore",
        "cod. turismo": "codice del turismo",
        "codice antimafia": "codice antimafia",
        "codice civile": "codice civile",
        "codice dei beni culturali e del paesaggio": "codice dei beni culturali e del paesaggio",
        "codice dei contratti pubblici": "codice dei contratti pubblici",
        "codice del Terzo settore": "codice del Terzo settore",
        "codice del consumo": "codice del consumo",
        "codice del processo amministrativo": "codice del processo amministrativo",
        "codice del processo tributario": "codice del processo tributario",
        "codice del turismo": "codice del turismo",
        "codice dell'amministrazione digitale": "codice dell'amministrazione digitale",
        "codice dell'ordinamento militare": "codice dell'ordinamento militare",
        "codice della crisi d'impresa e dell'insolvenza": "codice della crisi d'impresa e dell'insolvenza",
        "codice della nautica da diporto": "codice della nautica da diporto",
        "codice della navigazione": "codice della navigazione",
        "codice della proprietà industriale": "codice della proprietà industriale",
        "codice della protezione civile": "codice della protezione civile",
        "codice della strada": "codice della strada",
        "codice delle assicurazioni private": "codice delle assicurazioni private",
        "codice delle comunicazioni elettroniche": "codice delle comunicazioni elettroniche",
        "codice delle pari opportunità": "codice delle pari opportunità",
        "codice di giustizia contabile": "codice di giustizia contabile",
        "codice di procedura civile": "codice di procedura civile",
        "codice di procedura penale": "codice di procedura penale",
        "codice in materia di protezione dei dati personali": "codice in materia di protezione dei dati personali",
        "codice penale": "codice penale",
        "codice postale e delle telecomunicazioni": "codice postale e delle telecomunicazioni",
        "com": "codice dell'ordinamento militare",
        "cost": "costituzione",
        "cost.": "costituzione",
        "costituzione": "costituzione",
        "cp": "codice penale",
        "cpa": "codice del processo amministrativo",
        "cpc": "codice di procedura civile",
        "cpd": "codice in materia di protezione dei dati personali",
        "cpet": "codice postale e delle telecomunicazioni",
        "cpi": "codice della proprietà industriale",
        "cpo": "codice delle pari opportunità",
        "cpp": "codice di procedura penale",
        "cpt": "codice del processo tributario",
        "cts": "codice del Terzo settore",
        "ctu": "codice del turismo",
        "disp. att. c.c.": "disposizioni per l'attuazione del Codice civile e disposizioni transitorie",
        "disp. att. c.p.c.": "disposizioni per l'attuazione del Codice di procedura civile e disposizioni transitorie",
        "disp. prel.": "preleggi",
        "disposizioni per l'attuazione del Codice civile e disposizioni transitorie": "disposizioni per l'attuazione del Codice civile e disposizioni transitorie",
        "disposizioni per l'attuazione del Codice di procedura civile e disposizioni transitorie": "disposizioni per l'attuazione del Codice di procedura civile e disposizioni transitorie",
        "norme amb.": "norme in materia ambientale",
        "norme in materia ambientale": "norme in materia ambientale",
        "prel.": "preleggi",
        "preleggi": "preleggi"}
    
    input_type = input_type.lower().strip()
    # Improved logic to ensure accurate mapping
    for key, value in act_types.items():
        if input_type == key or input_type == key.replace(" ", ""): 
            return value
    raise ValueError("Tipo di atto non riconosciuto")

def estrai_data_da_denominazione(denominazione):
    # Pattern per cercare una data nel formato "21 Marzo 2022"
    pattern = r"\b(\d{1,2})\s([Gg]ennaio|[Ff]ebbraio|[Mm]arzo|[Aa]prile|[Mm]aggio|[Gg]iugno|[Ll]uglio|[Aa]gosto|[Ss]ettembre|[Oo]ttobre|[Nn]ovembre|[Dd]icembre)\s(\d{4})\b"
    
    # Ricerca della data all'interno della stringa utilizzando il pattern
    match = re.search(pattern, denominazione)
    
    # Se viene trovata una corrispondenza, estrai e ritorna la data
    if match:
        return match.group(0)  # Ritorna l'intera corrispondenza
    else:
    # Se non viene trovata alcuna corrispondenza, ritorna None o una stringa vuota
        return None

def estrai_numero_da_estensione(estensione):
    estensioni_numeriche = {
        None: 0, 'bis': 2, 'tris': 3, 'ter': 3, 'quater': 4, 'quinquies': 5,
        'quinques': 5, 'sexies': 6, 'septies': 7, 'octies': 8, 'novies': 9, 'decies': 10, 'undecies': 11, 'duodecies': 12, 'terdecies': 13, 'quaterdecies': 14,
        'quindecies': 15, 'sexdecies': 16, 'septiesdecies': 17, 'duodevicies': 18, 'undevicies': 19,
        'vices': 20, 'vicessemel': 21, 'vicesbis': 22, 'vicester': 23, 'vicesquater': 24,
        'vicesquinquies': 25, 'vicessexies': 26, 'vicessepties': 27, 'duodetricies': 28, 'undetricies': 29,
        'tricies': 30, 'triciessemel': 31, 'triciesbis': 32, 'triciester': 33, 'triciesquater': 34,
        'triciesquinquies': 35, 'triciessexies': 36, 'triciessepties': 37, 'duodequadragies': 38, 'undequadragies': 39,
        'quadragies': 40, 'quadragiessemel': 41, 'quadragiesbis': 42, 'quadragiester': 43, 'quadragiesquater': 44,
         'quadragiesquinquies': 45, 'quadragiessexies': 46, 'quadragiessepties': 47, 'duodequinquagies': 48, 'undequinquagies': 49,
    }
    return estensioni_numeriche.get(estensione, 0)

def get_annex_from_urn(urn):
    ann_num = re.search(r":(\d+)(!vig=|@originale)$", urn)
    if ann_num:
        return ann_num.group(1)
    return None

@lru_cache(maxsize=100)
def estrai_testo_articolo(atto, num_articolo=None, est_articolo=None, comma=None, tipo="xml", annesso=None):
    if tipo == 'xml' and atto:
        return estrai_da_xml(atto, num_articolo, est_articolo, comma, annesso)
    elif tipo == "html" and atto:
        return estrai_da_html(atto, comma)
    else:
        return "Tipo di atto non supportato o atto non fornito."

@lru_cache(maxsize=100)
def estrai_da_xml(atto, num_articolo, est_articolo, comma, annesso):
    try:
        soup = BeautifulSoup(atto, 'xml')
        
        # Handling 'annesso' extraction
        if annesso:
            annesso_soup = soup.find('annesso', {'id': str(annesso)})
            return annesso_soup.get_text(separator="\n", strip=True) if annesso_soup else "Annesso non trovato."

        articoli_text = []
        # Handling 'articolo' extraction
        if num_articolo:
            articoli = soup.find_all('articolo', {'id': str(num_articolo)})
            if not articoli:
                return "Nessun articolo trovato."

            # Selezionare l'articolo corretto in presenza di estensioni
            articolo = None
            if est_articolo:
                indice_estensione = estrai_numero_da_estensione(est_articolo)
                if indice_estensione > len(articoli):
                    return "Estensione dell'articolo non trovata."
                articolo = articoli[indice_estensione-1]
            else:
                articolo = articoli[0]

            corpo = articolo.find('corpo')
            # Handling 'comma' extraction
            if comma is not None:
                comma_elements = corpo.find_all('h:p')  # Assuming 'h:p' is the correct tag for 'comma'
                commi_text = []
                for p in comma_elements:
                    if p.get_text().strip().startswith(f'{comma}.'):
                        commi_text.append(p.get_text(separator="\n", strip=True))
                return "\n".join(commi_text) if commi_text else "Comma non trovato."
            else:
                return corpo.get_text(separator="\n", strip=True) if corpo else "Corpo dell'articolo non trovato."
        else:
            # If no specific article is requested, return all articles' text
            articoli = soup.find_all('articolo')
            for articolo in articoli:
                for tag_num in articolo.find_all('num'):
                    tag_num.decompose()
                articoli_text.append(articolo.get_text(separator="\n", strip=True))
            return "\n".join(articoli_text) if articoli_text else "Nessun articolo presente."

    except Exception as e:
        return f"Errore durante l'estrazione: {e}"


@lru_cache(maxsize=100)
def estrai_da_html(atto, comma):
    try:
        soup = BeautifulSoup(atto, 'html.parser')
        corpo = soup.find('div', class_='bodyTesto')
        #print(corpo.text)
        if not comma:
            return corpo.text
        else:
            parsedcorpo = corpo.find('div', class_='art-commi-div-akn')
            commi = parsedcorpo.find_all('div', class_='art-comma-div-akn')
            for c in commi:
                if f'{comma}.'in c.find('span', class_='comma-num-akn').text:
                    return c.text.strip()
    except Exception as e:
        return f"Errore generico: {e}"

def conta_articoli(atto_xlm):
    """
    Conta il numero di articoli presenti in un documento XML.

    Args:
        atto_xlm (str): I dati XML contenenti gli articoli.

    Returns:
        Il numero di articoli presenti nel documento.
    """
    soup = BeautifulSoup(atto_xlm, 'lxml-xml')
    return len(soup.find_all('articolo'))
