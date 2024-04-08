import datetime
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from text_op import estrai_testo_articolo
from functools import lru_cache

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
    
    # Se non viene trovata alcuna corrispondenza, ritorna None o una stringa vuota
    return None

def complete_date(act_type, date, act_number):
        driver = setup_driver()
        driver.get("https://www.normattiva.it/")
        search_box = driver.find_element(By.CLASS_NAME, "form-control.autocomplete.bg-transparent")  # Assicurati che il selettore sia corretto
        search_criteria = f"{act_type} {act_number} {date}"  # Formatta i criteri di ricerca come preferisci
        search_box.send_keys(search_criteria)
        search_box.send_keys(Keys.ENTER)
        elemento = driver.find_element(By.XPATH, '//*[@id="heading_1"]/p[1]/a')
        elemento_text = elemento.text
        data_completa = estrai_data_da_denominazione(elemento_text)
        driver.quit()
        return data_completa

def generate_urn(act_type, date=None, act_number=None, article=None, extension=None, version=None, version_date=None):
    """
    Genera un URL per Normattiva basandosi sui parametri forniti.
    """
    codici_urn = {
    "costituzione": "/uri-res/N2Ls?urn:nir:stato:costituzione",
    "codice penale": "/uri-res/N2Ls?urn:nir:stato:regio.decreto:1930-10-19;1398:1",
    "codice di procedura civile": "/uri-res/N2Ls?urn:nir:stato:regio.decreto:1940-10-28;1443:1",
    "disposizioni per l'attuazione del Codice di procedura civile e disposizioni transitorie": "/uri-res/N2Ls?urn:nir:stato:regio.decreto:1941-08-25;1368:1",
    "codici penali militari di pace e di guerra": "/uri-res/N2Ls?urn:nir:stato:relazione.e.regio.decreto:1941-02-20;303",
    "disposizioni di coordinamento, transitorie e di attuazione dei Codici penali militari di pace e di guerra": "/uri-res/N2Ls?urn:nir:stato:regio.decreto:1941-09-09;1023",
    "codice civile": "/uri-res/N2Ls?urn:nir:stato:regio.decreto:1942-03-16;262:2",
    "preleggi": "/uri-res/N2Ls?urn:nir:stato:regio.decreto:1942-03-16;262:1",
    "disposizioni per l'attuazione del Codice civile e disposizioni transitorie": "/uri-res/N2Ls?urn:nir:stato:regio.decreto:1942-03-30;318:1",
    "codice della navigazione": "/uri-res/N2Ls?urn:nir:stato:regio.decreto:1942-03-30;327:1",
    "approvazione del Regolamento per l'esecuzione del Codice della navigazione (Navigazione marittima)": "/uri-res/N2Ls?urn:nir:stato:decreto.del.presidente.della.repubblica:1952-02-15;328",
    "codice postale e delle telecomunicazioni": "/uri-res/N2Ls?urn:nir:stato:decreto.del.presidente.della.repubblica:1973-03-29;156",
    "codice di procedura penale": "/uri-res/N2Ls?urn:nir:stato:decreto.del.presidente.della.repubblica:1988-09-22;447",
    "norme di attuazione, di coordinamento e transitorie del codice di procedura penale": "/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:1989-07-28;271",
    "regolamento per l'esecuzione del codice di procedura penale": "/uri-res/N2Ls?urn:nir:ministero.grazia.e.giustizia:decreto:1989-09-30;334",
    "codice della strada": "/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:1992-04-30;285",
    "regolamento di esecuzione e di attuazione del nuovo codice della strada.": "/uri-res/N2Ls?urn:nir:stato:decreto.del.presidente.della.repubblica:1992-12-16;495",
    "codice del processo tributario": "/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:1992-12-31;546",
    "codice in materia di protezione dei dati personali": "/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2003-06-30;196",
    "codice delle comunicazioni elettroniche": "/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2003-08-01;259",
    "codice dei beni culturali e del paesaggio": "/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2004-01-22;42",
    "codice della proprietà industriale": "/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-02-10;30",
    "regolamento di attuazione del Codice della proprietà industriale": "/uri-res/N2Ls?urn:nir:ministero.sviluppo.economico:decreto:2010-01-13;33",
    "codice dell'amministrazione digitale": "/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-03-07;82",
    "codice della nautica da diporto": "/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-07-18;171",
    "codice del consumo": "/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-09-06;206",
    "codice delle assicurazioni private": "/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-09-07;209",
    "norme in materia ambientale": "/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2006-04-03;152",
    "nuovo Codice dei contratti pubblici": "/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2016-04-18;50",
    "codice dei contratti pubblici (in vigore fino al 18 aprile 2016)": "/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2006-04-12;163",
    "regolamento di esecuzione ed attuazione del Codice dei contratti pubblici": "/uri-res/N2Ls?urn:nir:stato:decreto.del.presidente.della.repubblica:2010-10-05;207",
    "codice delle pari opportunità": "/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2006-04-11;198",
    "codice dell'ordinamento militare": "/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2010-03-15;66",
    "codice del processo amministrativo": "/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2010-07-02;104:2",
    "codice del turismo": "/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2011-05-23;79",
    "codice antimafia": "/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2011-09-06;159",
    "codice di giustizia contabile": "/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2016-08-26;174",
    "codice del Terzo settore": "/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2017-07-03;117",
    "codice della protezione civile": "/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2018-01-02;1",
    "codice della crisi d'impresa e dell'insolvenza": "/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2019-01-12;14"
}
    base_url = "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:"
    
    normalized_type = normalize_act_type(act_type)
    
    if normalized_type in codici_urn:
        urn = codici_urn[normalized_type]
    else:
        try:
            if re.match(r"^\d{4}$", date) and act_number:
                full_date = complete_date(act_type=act_type, date=date, act_number=act_number) 
                date = full_date
            formatted_date = parse_date(date)
        except ValueError as e:
            print(f"Errore nella formattazione della data: {e}")
            return None
        urn = f"{normalized_type}:{formatted_date};{act_number}"
            
    if article:
        if "-" in article: 
            parts = article.split("-")
            article = parts[0]
            extension = parts[1]
    
        if article is str:
            re.sub(r'\b[Aa]rticoli?\b|\b[Aa]rt\.?\b', "", article)  
        
        urn += f"~art{str(article)}"
        
        if extension:
            urn += extension
                
    if version == "originale":
        urn += "@originale"
    elif version == "vigente":
        urn += "!vig="
        if version_date:
            formatted_version_date = parse_date(version_date)
            urn += formatted_version_date
            
    return base_url + urn

def get_annex_from_urn(urn):
    ann_num = re.search(r":(\d+)(!vig=|@originale)$", urn)
    if ann_num:
        return ann_num.group(1)
    return None

def export_xml(driver, urn, timeout, annex):
    driver.get(urn)
    export_button_selector = "#mySidebarRight > div > div:nth-child(2) > div > div > ul > li:nth-child(2) > a"
    export_xml_selector = "generaXml"
        
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, export_button_selector))).click()
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.NAME, export_xml_selector))).click()
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, timeout)
    xml_data = driver.page_source
    return xml_data

def save_xml(xml_data, save_xml_path):
    with open(save_xml_path, 'w', encoding='utf-8') as file:
        file.write(xml_data)
    return f"XML salvato in: {save_xml_path}"

def extract_html_article(urn, article, comma):
    response = requests.get(urn)
    if response.status_code == 200:
        html_content = response.text
        return estrai_testo_articolo(atto=html_content, num_articolo=article, comma=comma, tipo='html')
    return None

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

@lru_cache(maxsize=100)
def get_urn_and_extract_data(act_type, date=None, act_number=None, article=None, extension=None, comma=None, version=None, version_date=None, timeout=10, save_xml_path=None):
    
    urn = generate_urn(act_type, date, act_number, article, extension, version, version_date)
    if urn is None:
        print("Errore nella generazione dell'URN.")
        return None

    annex = get_annex_from_urn(urn)
    print(urn)

    if not article:
        driver = setup_driver()
        try:
            xml_data = export_xml(driver, urn, timeout, annex)
            if save_xml_path:
                save_xml(xml_data, save_xml_path)
            xml_out = estrai_testo_articolo(xml_data, annesso=annex)
            return xml_out, urn
        except Exception as e:
            print(f"Errore nell'esportazione XML: {e}")
            return None
        finally:
            driver.quit()
    else:
        try:
            html_out = extract_html_article(urn, article, comma)
            return html_out, urn
        except Exception as e:
            print(f"Errore nell'esportazione HTML: {e}")
            return None
