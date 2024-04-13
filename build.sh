#!/bin/bash

# Nome costante dell'applicazione
APP_NAME="NormaScraper"

# Carica l'ultima versione o imposta quella di default
if [ -f "version.txt" ]; then
    VERSION=$(cat version.txt)
else
    VERSION="0.9.0"
fi

increment_version() {
    if [ "$1" == "--noup" ]; then
        echo "Mantenimento della versione attuale: $VERSION"
        return
    fi

    major=$(echo $VERSION | cut -d. -f1)
    minor=$(echo $VERSION | cut -d. -f2)
    patch=$(echo $VERSION | cut -d. -f3)

    if [ "$1" == "--upup" ]; then
        major=$((major+1))
        minor=0
        patch=0
    elif [ "$1" == "--up" ]; then
        minor=$((minor+1))
        patch=0
    else
        patch=$((patch+1))
    fi

    VERSION="$major.$minor.$patch"
    echo $VERSION > version.txt
}

# Funzione per pulire i file generati
clean_up() {
    echo "Pulizia dei file generati..."
    rm -f *.zip
    rm -rf build dist "${APP_NAME}-*.spec" $APP_NAME

    # Specifica per cleanhard
    if [ "$1" == "--cleanhard" ]; then
        rm -rf "${APP_NAME}"*.app
    else
        zip -r old_version/"${APP_NAME}-${VERSION}.zip" "${APP_NAME}"*.app
        rm -rf "${APP_NAME}"*.app 
    fi

    echo "Pulizia completata."
}

# Gestione delle opzioni da riga di comando
case "$1" in
    --clean|--cleanhard)
        clean_up $1
        exit 0
        ;;
    --noup|--up|--upup)
        increment_version $1
        ;;
    *)
        increment_version
        ;;
esac

FULL_APP_NAME="${APP_NAME}-${VERSION}"

# Creazione dell'applicazione con PyInstaller
pyinstaller --name "$FULL_APP_NAME" --onedir --windowed -i resources/icon.icns \
--add-data "atti_scaricati:atti_scaricati" \
--add-data "resources:resources" \
--add-data "usr:usr" \
--add-data "usr/cron:usr" \
--add-data "README.md:." \
--add-data "tools:tools" \
--noconfirm "NormaScraper.py"
mv *.app old_version

# Verifica e gestione del risultato finale
if [ -d "dist/$FULL_APP_NAME" ]; then
    mv "dist/$FULL_APP_NAME.app" .
    echo "Applicazione spostata con successo nella directory principale"
    #zip -r $FULL_APP_NAME.zip $FULL_APP_NAME.app
    rm -rf build dist "${FULL_APP_NAME}.spec" 
    echo "Cartelle build, dist e file .spec eliminati con successo"
    chmod 777 $FULL_APP_NAME
    echo "File reso eseguibile"
else
    echo "Errore: la cartella di distribuzione non esiste."
fi