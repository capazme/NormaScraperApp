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

def normalize_act_type(input_type):
    """
    Normalizes the type of legislative act based on a variable input.
    """
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
    "cp": "codice penale",
    "c.p.": "codice penale",
    "cod. pen.": "codice penale",
    "cpc": "codice di procedura civile",
    "c.p.c": "codice di procedura civile",
    "cod. proc. civ": "codice di procedura civile",
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
        
        if annesso:
            soup = soup.find('annesso', {'id': str(annesso)})
            return soup.get_text(separator="\n", strip=True)


        if  num_articolo:
            articoli = soup.find_all('articolo', {'id': str(num_articolo)}) 
            #print(articoli) 
            if not articoli:
                return "Nessun articolo trovato."

            # Selezionare l'articolo corretto in presenza di estensioni
            if est_articolo:
                indice_estensione = estrai_numero_da_estensione(est_articolo)
                if indice_estensione >= len(articoli):
                    return "Estensione dell'articolo non trovata."
                articolo = articoli[indice_estensione-1]
            else:
                articolo = articoli[0]

            corpo = articolo.find('corpo')
            # Gestione del comma
            if comma is not None:
                comma_elements = corpo.find_all('h:p') #ERRORE nella formattazione ordinaria di Normattiva
                for p in comma_elements:
                    if p.get_text().startswith(f'{comma}. ') or p.get_text().startswith(f'{comma}. ', 2) :
                        return p.get_text(separator="\n", strip=True)
            else:
                return articolo.get_text(separator="\n", strip=True)
        else:
            arts = []
            articoli = soup.find_all('articolo')
            for a in articoli:
                for tag_num in a.find_all('num'):
                    tag_num.decompose()
                arts.append(a.get_text(separator="\n", strip=True))
            return ''.join(arts)
    except Exception as e:
        return f"Errore generico: {e}" 

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

def estrai_testi_articoli(atto_xlm):
    """
    Estrae il testo di tutti gli articoli presenti in un documento XML.

    Args:
        atto_xlm (str): I dati XML contenenti gli articoli.

    Returns:
        Una lista contenente il testo di ciascun articolo nel documento.
    """
    numero_articoli = conta_articoli(atto_xlm)
    articoli = [estrai_testo_articolo(atto_xlm, i+1) for i in range(numero_articoli)]
    return articoli