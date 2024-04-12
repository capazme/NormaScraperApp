import re
import os
from tools.map import BROCARDI_CODICI, BROCARDI_MAP
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
        
    def look_up(self, norma):
        if isinstance(norma, NormaVisitata):
            # Assumendo che do_know ritorni una tupla con il link come secondo elemento
            norma_info = self.do_know(norma)
            if norma_info:
                link = norma_info[1]
                numero_articolo = norma.to_dict()['numero_articolo']
                components = [link, f"art{numero_articolo}.html"]
                
                # Costruisci il pattern usando il primo e l'ultimo componente
                start, end = components[0], components[1]
                # La regex qui sotto assume che tra l'inizio e la fine possa esserci qualsiasi cosa
                pattern = re.compile(re.escape(start) + r".*" + re.escape(end), re.DOTALL)

                # Cerca corrispondenze nel dizionario
                for key, value in self.knowledge[1].items():
                    if re.search(pattern, value):
                        print(f"Found: {value}")
                        return value

                print("No match found.")
            else:
                print("No knowledge available.")
        else:
            print("Invalid input type.")
            

    def search_brocardi(self, search_term):
        """
        Search for a given term in the brocardi links and return the URL if available.
        """
        url = self.links.get(search_term)
        return url if url else "No brocardi link available for this term."

brocardi_scraper = BrocardiScraper()


data_atto = "6 settembre 2011"
numero_atto = "159" 
articolo_atto = "1" 
tipo_atto = "D.lgs."

norma = NormaVisitata(tipo_atto=tipo_atto, numero_atto=numero_atto, numero_articolo=articolo_atto, data=data_atto)

print (brocardi_scraper.look_up(norma))