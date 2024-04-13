<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->

<p><a href="#readme-top"></a></p>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->

<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![CC0-1.0 License][license-shield]][license-url]

<!-- PROJECT LOGO -->

<br />
<div align="center">
  <a href="https://github.com/capazme/NormaScraperApp">
    <img src="resources/logo.png" alt="Logo" width="250" height="250">
  </a>

<h3 align="center">NORMASCRAPER - BETA</h3>

<p align="center">
    Semplice interfaccia per accedere al sito del governo italiano Normattiva
    <br />
    <br />
    <br />
    ·
    <a href="https://github.com/capazme/NormaScraperApp/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/capazme/NormaScraperApp/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
        <ul>
        <li><a href="#spec">Prerequisites</a></li>
      </ul>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

NormaScraperApp è un'applicazione Python che fornisce un'interfaccia utente per accedere a Normattiva, il sito del governo italiano che ospita la legislazione nazionale. L'applicazione permette agli utenti di cercare atti legislativi specifici, visualizzare i dettagli e salvare i risultati.

```markdown
  NormaScraperApp
  ├── LICENSE.txt
  ├── NormaScraper-Betav0.7.1.zip
  ├── NormaScraper.py
  ├── BrocardiScraper.py
  ├── README.md
  ├── atti_scaricati
  │   ├── cost.xml
  │   └── test.xml
  ├── resources
  │   ├── configurazione.yaml
  │   ├── icon.icns
  │   ├── logo.png
  │   ├── requirements.txt
  │   └── screen.png
  └── tools
  │   ├── __init__.py
  │   ├── config.py
  │   ├── sys_op.py
  │   ├── text_op.py
  │   ├── usr.py
  └── usr
      ├── .index
      └── cron
          ├── .index
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

### Prerequisites

**Nessun prerequisito per l'applicazione contenuta nel file .zip.**

**Python e pip sono necessari per costruire dalla fonte.**

### Easy installation (Pre-builded)

1. Scarica il file NormaScraper-vX.zip
2. Estrai il contenuto dall'archivio
3. Esegui l'app pre-buildata

### Build from source

!! Assicurati di avere python e pip installati !!

1. Clona la repository

   ```shell
   git clone https://github.com/capazme/NormaScraperApp.git
   ```
2. Installa le librerie pytho necessarie

  ```shell
     pip install -r resources/requirements.txt
  ```

    3. Avvia NormaScraper.py con python 3.12 o superiore

  ```sh
  python -m NormaScraper.py
  ```

3B. Oppure utilizza il file build.sh per ottenere un file eseguibile
   Questo script accetta vari flag che influenzano la versione e il comportamento della build:

   --up: Aumenta la versione minore di 0.1.
   --upup: Aumenta la versione maggiore di 1.
   --noup: Non aumenta la versione durante questa compilazione.
   --clean: Pulisce i file generati dalle compilazioni precedenti, senza rimuovere le versioni precedenti dell'app.
   --cleanhard: Pulisce i file generati dalle compilazioni precedenti e rimuove le versioni precedenti dell'app.
   Per eseguire una compilazione standard che incrementa automaticamente la versione patch di 0.0.1, usa il seguente comando:

  ```bash
  ./build.sh
  ```

Se desideri mantenere la stessa versione e solo ricompilare l'app, puoi usare:

  ```bash
  ./build.sh --noup
  ```

#### Incremento della Versione

Per specificare manualmente il tipo di incremento della versione:

  ```bash
  ./build.sh --up    # Incrementa la versione minore
  ./build.sh --upup  # Incrementa la versione maggiore
  ```

#### Pulizia

Per pulire la directory di build senza rimuovere le versioni precedenti:

  ```bash
  ./build.sh --clean
  ```

Per una pulizia completa che include la rimozione delle versioni vecchie:

  ```bash
  ./build.sh --cleanhard
  ```

L'app compilata verrà spostata nella directory principale del progetto, e tutti i file temporanei saranno eliminati dopo la compilazione."

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

<div align="center">
  <a href="https://github.com/capazme/NormaScraperApp">
    <img src="resources/screen.png" width="500" height="400">
  </a>
<p align="right">(<a href="#readme-top">back to top</a>)</p> </div>

## Spec

## get_urn_and_extract_data()

La funzione get_urn_and_extract_data è progettata per interrogare il sito Normattiva, utilizzando **l'URN** (Uniform Resource Name) per identificare specifici atti legislativi. Una volta ottenuto l'accesso all'atto desiderato, la funzione estrae dati rilevanti che possono includere testo dell'atto, date di promulgazione, modifiche successive, e altro ancora. I parametri principali della funzione includono:

* act_type (str): Il tipo di atto legislativo per cui si desidera generare l'URN.

  * **atto generico** (legge, decreto-legge, decreto legislativo e possibili abbreviazioni)
  * **atto specifico** tra quelli elencati (o una abbraviazione elencata):
    * Costituzione (costituzione, cost, cost., c.)
    * Codice Civile (cc, c.c., codice civile, cod. civ., disp. att. c.c.)
    * Preleggi (disp. prel., preleggi, prel.)
    * Codice Penale (cp, c.p., cod. pen.)
    * Codice di Procedura Civile (cpc, c.p.c., cod. proc. civ., disp. att. c.p.c.)
    * Codice di Procedura Penale (cpp, c.p.p., cod. proc. pen.)
    * Codice della Navigazione (cn, cod. nav.)
    * Codice Postale e delle Telecomunicazioni (cpet, cod. post. telecom.)
    * Codice della Strada (cds, cod. strada)
    * Codice del Processo Tributario (cpt, cod. proc. trib.)
    * Codice in Materia di Protezione dei Dati Personali (cpd, cod. prot. dati)
    * Codice delle Comunicazioni Elettroniche (cce, cod. com. elet.)
    * Codice dei Beni Culturali e del Paesaggio (cbc, cod. beni cult.)
    * Codice della Proprietà Industriale (cpi, cod. prop. ind.)
    * Codice dell'Amministrazione Digitale (cad, cod. amm. dig.)
    * Codice della Nautica da Diporto (cnd, cod. naut. diport.)
    * Codice del Consumo (cdc, cod. consumo)
    * Codice delle Assicurazioni Private (cap, cod. ass. priv.)
    * Norme in Materia Ambientale (camb, norme amb.)
    * Codice dei Contratti Pubblici (ccp, cod. contr. pubb.)
    * Codice delle Pari Opportunità (cpo, cod. pari opp.)
    * Codice dell'Ordinamento Militare (com, cod. ord. mil.)
    * Codice del Processo Amministrativo (cpa, cod. proc. amm.)
    * Codice del Turismo (ctu, cod. turismo)
    * Codice Antimafia (cam, cod. antimafia)
    * Codice di Giustizia Contabile (cgco, cod. giust. cont.)
    * Codice del Terzo Settore (cts, cod. ter. sett.)
    * Codice della Protezione Civile (cdpc, cod. prot. civ.)
    * Codice della Crisi d'Impresa e dell'Insolvenza (cci, cod. crisi imp.)"
    * date (str, optional): La data di pubblicazione dell'atto in formato YYYY-MM-DD.
* **act_number** (str, optional): Il numero dell'atto legislativo e la sua espansione (come "-bis" o "-ter")
* **version** (str, optional): Indica se l'atto è nella versione "originale" o "vigente".
* **version_date** (str, optional): La data della versione dell'atto in formato YYYY-MM-DD.

  ---

<!-- ROADMAP -->

## Roadmap

- [ ] Brocardi implementation
  - [ ] Aggiunta link articoli rilevanti
  - [ ] Aggiunta tasto spiegazione e massime (per i codici supportati da brocardi)
- [ ] Altalex implementation
  - [ ] Altalexpedia
- [ ]

See the [open issues](https://github.com/capazme/NormaScraperApp/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

# KNOWN ISSUES

* La ricerca con data incompleta è più lenta di quella con la data completa (ma solo al primo caricamento, in cronologia è salvata sempre la data completa)
* Lo scorrimmento degli articoli non supporta le estensioni (-bis, ter etc...)
* Alcuni codici di brocardi sono incompleti (es. titolo I codice della strada)
* Commi non supportati per i codici (e occasionalmente alcuni decreti formattati male)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the CC0-1.0 License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

Guglielmo Puzio - - guglielmo.puzio00@gmail.com - guglielmo.puzio@studenti.luiss.it (ancora per un po')

Project Link: [https://github.com/capazme/NormaScraperApp](https://github.com/capazme/NormaScraperApp)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->

<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

```

```

[contributors-url]: https://github.com/capazme/NormaScraperApp/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/capazme/NormaScraperApp.svg?style=for-the-badge
[forks-url]: https://github.com/capazme/NormaScraperApp/network/members
[stars-shield]: https://img.shields.io/github/stars/capazme/NormaScraperApp.svg?style=for-the-badge
[stars-url]: https://github.com/capazme/NormaScraperApp/stargazers
[issues-shield]: https://img.shields.io/github/issues/capazme/NormaScraperApp.svg?style=for-the-badge
[issues-url]: https://github.com/capazme/NormaScraperApp/issues
[license-shield]: https://img.shields.io/github/license/capazme/NormaScraperApp.svg?style=for-the-badge
[license-url]: https://github.com/capazme/NormaScraperApp/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[product-screenshot]: resources/screen.png
[contributors-shield]: https://img.shields.io/github/contributors/capazme/NormaScraperApp.svg?style=for-the-badge
