import re
from bs4 import BeautifulSoup
from tkinter import messagebox
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from .text_op import estrai_testo_articolo, parse_date, normalize_act_type, estrai_data_da_denominazione, get_annex_from_urn
from functools import lru_cache
from .map import NORMATTIVA_URN_CODICI

MAX_CACHE_SIZE = 1000

class NormaVisitata:
    def __init__(self, tipo_atto, data=None, numero_atto=None, numero_articolo=None, url=None):
        self.tipo_atto_str = normalize_act_type(tipo_atto, search=True)
        self.tipo_atto_urn = normalize_act_type(tipo_atto)
        self.data = data if data else ""
        self.numero_atto = numero_atto if numero_atto else ""
        self.numero_articolo = numero_articolo if numero_articolo else ""
        if not url:
            self.url = self.get_url()
        else:
            self.url = url

    def __str__(self):
        parts = [self.tipo_atto_str]

        if self.data:
            parts.append(f"{self.data},".strip())

        if self.numero_atto:
            num_prefix = "n."
            parts.append(f"{num_prefix} {self.numero_atto}".strip())

        if self.numero_articolo:
            # Aggiunge 'art.' solo se numero_atto o data sono presenti per evitare stringhe tipo "Tipo atto art. Numero"
            articolo_prefix = "art."
            parts.append(f"{articolo_prefix} {self.numero_articolo}".strip())

        return " ".join(parts)
    
    def get_url(self):
        self.url = generate_urn(self.tipo_atto_urn, date=self.data, act_number=self.numero_atto, article=self.numero_articolo)
        return self.url
    
    def to_dict(self):
        return {'tipo_atto': self.tipo_atto_str, 'data': self.data, 'numero_atto': self.numero_atto, 'numero_articolo': self.numero_articolo, 'url': self.url}

    @staticmethod
    def from_dict(data):
        return NormaVisitata(**data)
    
driver = None

def setup_driver():
    global driver
    if driver is None:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        driver = webdriver.Chrome(options=chrome_options)
    return driver

def close_driver():
    global driver
    if driver:
        driver.quit()
        driver = None


@lru_cache(maxsize=MAX_CACHE_SIZE)
def complete_date(act_type, date, act_number):
    try:    
        #driver = setup_driver()
        driver.get("https://www.normattiva.it/")
        search_box = driver.find_element(By.CSS_SELECTOR, ".form-control.autocomplete.bg-transparent")  # Assicurati che il selettore sia corretto
        search_criteria = f"{act_type} {act_number} {date}"
        search_box.send_keys(search_criteria)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"button-3\"]"))).click()
        elemento = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="heading_1"]/p[1]/a')))
        elemento_text = elemento.text
        #messagebox.showinfo("Completamento data", f'{elemento_text}')
        data_completa = estrai_data_da_denominazione(elemento_text)
        #driver.quit()
        return data_completa
    except Exception as e:
        return f"Errore nel completamento della data, inserisci la data completa: {e}" 

def xml_to_html(xml_file_path):
    with open(xml_file_path, 'r', encoding='utf-8') as file:
        xml_str = file.read()

    soup = BeautifulSoup(xml_str, 'xml')
    
    # Inizializzazione dell'HTML con lo stile estratto dal file XML
    style_content = soup.find('style').string if soup.find('style') else ""
    html_content = [f'<html><head><style>{style_content}</style></head><body>\n\n\n']
    
    # Estrazione ed elaborazione dei tag <articolo>
    nir = soup.find('NIR')
    if nir:
        articoli = nir.find_all('articolo')
        for articolo in articoli:
            # Pre-calcolo del testo dell'articolo per evitare l'errore nelle f-string
            articolo_text = articolo.get_text(separator="\n", strip=True)
            # Aggiunta dell'articolo all'HTML
            html_content.append(f'<div class="articolo">\n{articolo_text}\n</div>\n\n')
    
    # Chiusura dei tag HTML
    html_content.append('</body></html>')
    # Unione dei componenti HTML in una singola stringa
    return ''.join(html_content)

@lru_cache(maxsize=MAX_CACHE_SIZE)
def generate_urn(act_type, date=None, act_number=None, article=None, extension=None, version=None, version_date=None):
    """
    Genera un URL per Normattiva basandosi sui parametri forniti.
    """
    codici_urn = NORMATTIVA_URN_CODICI
    
    base_url = "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:"
    
    normalized_act_type = normalize_act_type(act_type)
    #messagebox.showinfo("log", normalized_act_type)
    if act_type in codici_urn:
        urn = codici_urn[act_type]
    else:
        try:
            if re.match(r"^\d{4}$", date) and act_number and isinstance(date, str):
                #messagebox.showinfo("log", "ricerca data completa...")
                act_type_for_search = normalize_act_type(act_type, search=True)
                #messagebox.showinfo("log", act_type_for_search)
                full_date = complete_date(act_type=act_type_for_search, date=date, act_number=act_number) 
                date = full_date
            formatted_date = parse_date(date)
        except ValueError as e:
            print(f"Errore nella formattazione della data: {e}")
            return None
        urn = f"{normalized_act_type}:{formatted_date};{act_number}"
            
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
        else:
            extension=''
                
    if version == "originale":
        urn += "@originale"
    elif version == "vigente":
        urn += "!vig="
        if version_date:
            formatted_version_date = parse_date(version_date)
            urn += formatted_version_date
    act_type_for_cron = normalize_act_type(act_type, search=True)
    norma = NormaVisitata(tipo_atto=act_type_for_cron, data=date, numero_atto=act_number, numero_articolo=article+extension if article else None, url=base_url+urn)
    return base_url + urn, norma

@lru_cache(maxsize=MAX_CACHE_SIZE)
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

@lru_cache(maxsize=MAX_CACHE_SIZE)
def save_xml(xml_data, save_xml_path):
    with open(save_xml_path, 'w', encoding='utf-8') as file:
        file.write(xml_data)
    return f"XML salvato in: {save_xml_path}"

@lru_cache(maxsize=MAX_CACHE_SIZE)
def extract_html_article(urn, article, comma):
    response = requests.get(urn)
    if response.status_code == 200:
        html_content = response.text
        return estrai_testo_articolo(atto=html_content, num_articolo=article, comma=comma, tipo='html')
    return None

@lru_cache(maxsize=MAX_CACHE_SIZE)
def get_urn_and_extract_data(act_type, date=None, act_number=None, article=None, extension=None, comma=None, version=None, version_date=None, timeout=10, save_xml_path=None):
    
    #normalized_act_type = normalize_act_type(act_type)
    
    urn, norma = generate_urn(act_type=act_type, date=date, act_number=act_number, article=article, extension=extension, version=version,version_date=version_date)
    if urn is None:
        print("Errore nella generazione dell'URN.")
        return None

    annex = get_annex_from_urn(urn)
    print(urn)

    if not article:
        #driver = setup_driver()
        try:
            xml_data = export_xml(driver, urn, timeout, annex)
            if save_xml_path:
                save_xml(xml_data, save_xml_path)
            xml_out = estrai_testo_articolo(xml_data, annesso=annex)
            return xml_out, urn, norma
        except Exception as e:
            print(f"Errore nell'esportazione XML: {e}")
            return None
        #finally:
            #driver.quit()
    else:
        try:
            html_out = extract_html_article(urn, article, comma)
            return html_out, urn, norma
        except Exception as e:
            print(f"Errore nell'esportazione HTML: {e}")
            return None
