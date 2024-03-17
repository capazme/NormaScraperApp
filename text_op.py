from bs4 import BeautifulSoup

def estrai_numero_da_estensione(estensione):
    estensioni_numeriche = {
        None: 0, 'bis': 1, 'tris': 2, 'ter': 3, 'quater': 4, 'quinquies': 5,
        'quinques': 5, 'sexies': 6, 'septies': 7, 'octies': 8, 'novies': 9,
    }
    return estensioni_numeriche.get(estensione, 0)

def estrai_testo_articolo(atto_xml, num_articolo=1, est_articolo=None, comma=None):
    try:
        soup = BeautifulSoup(atto_xml, 'xml')
        
        if isinstance(num_articolo, str) and "-" in num_articolo:
            parts = num_articolo.split('-')
            num_articolo, est_articolo = int(parts[0]), parts[1]
        else:
            num_articolo = int(num_articolo)
        
        # Utilizziamo BeautifulSoup per trovare gli articoli, ignorando gli spazi dei nomi
        articoli = soup.find_all('articolo', {'id': str(num_articolo)})
        
        if not articoli:
            return "Nessun articolo trovato."
        
        # Selezionare l'articolo corretto in presenza di estensioni
        if est_articolo:
            indice_estensione = estrai_numero_da_estensione(est_articolo)
            if indice_estensione >= len(articoli):
                return "Estensione dell'articolo non trovata."
            articolo = articoli[indice_estensione]
        else:
            articolo = articoli[0]
        
        # Gestione specifica del comma
        if comma is not None:
            comma_elements = articolo.find_all('comma', {'id': f'art{num_articolo}-com{comma}'})
            if comma_elements:
                return ''.join([element.get_text() for element in comma_elements])
            else:
                # Cerca nel testo degli elementi p senza considerare gli spazi dei nomi
                p_out = []
                for p in articolo.find_all('p'):
                    if p.get_text(strip=True).startswith(f"{comma}"):
                        p_out.append(p.get_text(strip=True))
                return ' '.join(p_out) if p_out else "Comma specificato non trovato."
        else:
            return articolo.get_text(strip=True)

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