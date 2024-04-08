import re
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

# Test della funzione
denominazione_test = "DECRETO-LEGGE 21 Aprile 2022, n. 21"
data_estrapolata = estrai_data_da_denominazione(denominazione_test)
print(data_estrapolata)  # Dovrebbe stampare "21 Marzo 2022"
