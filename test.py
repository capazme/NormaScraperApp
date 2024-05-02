from tools import sys_op

def check_tree(url, skeleton = False):
    tree = sys_op.get_tree(url)[0]
    sequenza_articoli_ghst = [stringa if any(carattere.isdigit() for carattere in stringa) else '' for stringa in tree]
    sequenza_titoli_ghts = [stringa if any(carattere.isupper() for carattere in stringa) else '' for stringa in tree]
    sequenza_articoli = list(filter(None, sequenza_articoli_ghst))
    sequenza_articoli = [stringa.replace(' ', '-') for stringa in sequenza_articoli]

    sequenza_titoli = list(filter(None, sequenza_titoli_ghts))
    
    if skeleton == False:
        return sequenza_articoli, sequenza_titoli
    else:
        return sequenza_articoli_ghst, sequenza_titoli_ghts
    
url = 'https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:1990-08-07;241~art1!vig='

print(check_tree(url=url))