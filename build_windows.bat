# Nome costante dell'applicazione
$APP_NAME = "NormaScraper"

# Versione dell'applicazione
$VERSION = "0.9.0"
$FULL_APP_NAME = "$APP_NAME-$VERSION"

# Path di output per PyInstaller
$distPath = "dist/$FULL_APP_NAME"

# Esegue PyInstaller
pyinstaller --name "$FULL_APP_NAME" --onedir --windowed -i "resources/icon.ico" `
--add-data "atti_scaricati;atti_scaricati" `
--add-data "resources;resources" `
--add-data "usr;usr" `
--add-data "usr/cron;usr" `
--add-data "README.md;." `
--add-data "tools;tools" `
--noconfirm "$APP_NAME.py"

# Verifica se la cartella di distribuzione esiste
if (Test-Path $distPath) {
    # Sposta l'applicazione nella directory principale
    Move-Item "$distPath.app" -Destination "."

    # Pulizia delle cartelle e file non più necessari
    Remove-Item "build", "dist", "$FULL_APP_NAME.spec" -Recurse -Force

    Write-Host "Applicazione spostata con successo e pulizia completata."
} else {
    Write-Host "Errore: la cartella di distribuzione non esiste."
}
