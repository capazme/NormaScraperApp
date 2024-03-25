from bs4 import BeautifulSoup
def nospazi(text):
    textlist = text.split()
    for t in textlist:
        t.strip
    textout = ' '.join(textlist)
    return textout

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


def estrai_testo_articolo(atto, num_articolo=None, est_articolo=None, comma=None, tipo = "xml", annesso=None):
    
    if tipo == 'xml' and atto:
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
    elif tipo == "html" and atto:
        try:
            soup = BeautifulSoup(atto, 'html.parser')
            corpo = soup.find('div', class_='bodyTesto')
            print(corpo.text)
            if not comma:
                return corpo.text
            else:
                parsedcorpo = corpo.find('div', class_='art-commi-div-akn')
                commi = parsedcorpo.find_all('div', class_='art-comma-div-akn')
                
                for c in commi:
                    if f'{comma}.'in c.find('span', class_='comma-num-akn').text.strip():
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