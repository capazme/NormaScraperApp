import json
import os
from tools.map import BROCARDI_CODICI, BROCARDI_MAP, NORMATTIVA_URN_CODICI
from tools.sys_op import NormaVisitata
from tools.text_op import normalize_act_type, parse_date

CURRENT_APP_PATH = os.path.dirname(os.path.abspath(__file__))

class BrocardiScraper:
    """
    Scraper for Brocardi.it to search for legal terms and provide links.
    """
    def __init__(self):
        """
        Initialize the scraper by loading the brocardi links from a JSON file.
        """

        self.knowledge = [BROCARDI_CODICI, BROCARDI_MAP]

    def do_know(self, norma):
        if isinstance(norma, NormaVisitata):
            atts = norma.to_dict()
            data_atto = atts['data']
            numero_atto = atts['numero_atto'] 
            tipo_atto = atts['tipo_atto']
            if not tipo_atto:
                raise Exception("TIPO ATTO NON INSERITO")
            
            tipo_norm = normalize_act_type(tipo_atto, True, 'brocardi')
            components = [tipo_norm]
            if data_atto:
                components.append(data_atto)
            if numero_atto:
                components.append(f"n. {numero_atto}")
            strcmp = " ".join(components)
            
        elif isinstance(norma, str):
            strcmp = norma
        else:
            raise Exception("Formato norma non valido")
        
        for txt, link in self.knowledge[0].items():
            if strcmp.lower() in txt.lower():
                return txt, link
        return False
        
    def load_links(self, file_path):
        """
        Load brocardi links from a JSON file.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading JSON data: {e}")
            return {}

    def search_brocardi(self, search_term):
        """
        Search for a given term in the brocardi links and return the URL if available.
        """
        url = self.links.get(search_term)
        return url if url else "No brocardi link available for this term."

#brocardi_scraper = BrocardiScraper()
#count_false = []
#count_true = []
#
#dict_normattiva = NORMATTIVA_URN_CODICI
#dict_brocardi = BROCARDI_CODICI
#
#norma = NormaVisitata(tipo_atto='codice penale')
#
#print (brocardi_scraper.do_know('L. 22 dicembre 2017, n. 219'))