import datetime
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from text_op import estrai_testo_articolo

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
    act_types = {
        "decreto legge": "decreto.legge",
        "dl": "decreto.legge",
        "legge": "legge",
        "costituzione": "costituzione"
    }
    
    input_type = input_type.lower().strip()
    # Improved logic to ensure accurate mapping
    for key, value in act_types.items():
        if input_type == key or input_type == key.replace(" ", ""): 
            return value
    raise ValueError("Tipo di atto non riconosciuto")


def generate_urn(act_type, date, act_number, article=None, extension=None, version=None, version_date=None):
    """
    Genera un URL per Normattiva basandosi sui parametri forniti.
    """
    try:
        formatted_date = parse_date(date)
        normalized_type = normalize_act_type(act_type)
    except ValueError as e:
        print(f"Errore nella formattazione dei parametri: {e}")
        return None

    base_url = "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:"
    urn = f"{normalized_type}:{formatted_date};{act_number}"
        
    if article:
        urn += f"~art{article}"
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

def get_urn_and_extract_data(driver, act_type, date, act_number, article=None, extension=None, comma = None, version=None, version_date=None, timeout=10):
    """
    Funzione principale per generare l'URN, visitare la pagina e, in base all'esigenza, esportare in XML o estrarre testo HTML.
    """
    urn = generate_urn(act_type, date, act_number, article, extension, version, version_date)
    if urn is None:
        print("Errore nella generazione dell'URN.")
        return None

    act_link = urn  
    driver.get(act_link)
    try:
        export_button_selector = "#mySidebarRight > div > div:nth-child(2) > div > div > ul > li:nth-child(2) > a"
        export_xml_selector = "generaXml"
            
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, export_button_selector))).click()
        driver.switch_to.window(driver.window_handles[-1])
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.NAME, export_xml_selector))).click()
        driver.switch_to.window(driver.window_handles[-1])
        WebDriverWait(driver, timeout)
        xml_data = driver.page_source
        driver.close()
        xlm_out = estrai_testo_articolo(xml_data, article, extension, comma)
        return xlm_out
    except Exception as e:
        print(f"Errore nell'esportazione XML: {e}")
        return None