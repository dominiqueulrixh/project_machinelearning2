import os
import requests
from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import tempfile
import shutil

# URL der Seite mit dem PDF
url = "https://www.fedlex.admin.ch/eli/cc/24/233_245_233/de"

# Verzeichnis, in dem das PDF gespeichert wird
script_dir = os.path.dirname(os.path.abspath(__file__))
pdf_directory = os.path.join(script_dir, '../data')
pdf_filename = "Zivilgesetzbuch.pdf"
pdf_path = os.path.join(pdf_directory, pdf_filename)

# Funktion zum Herunterladen des PDFs
def download_pdf(pdf_url, save_path):
    response = requests.get(pdf_url, stream=True)
    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

# Funktion zum Überprüfen der Webseite
def check_for_update():
    # WebDriver konfigurieren (hier wird Chrome verwendet)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    prefs = {'download.default_directory': pdf_directory}
    options.add_experimental_option('prefs', prefs)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    driver.get(url)
    time.sleep(5)  # Warten, bis die Seite vollständig geladen ist

    # Finden des relevanten Tabellenabschnitts
    try:
        table_row = driver.find_element(By.CSS_SELECTOR, 'tr.page0.visible')
        date_cell = table_row.find_element(By.CSS_SELECTOR, 'td.no-padding-right.is-active')
        last_modified_str = date_cell.text.strip()
        last_modified_date = datetime.strptime(last_modified_str, '%d.%m.%Y')
        
        # Klicken Sie auf den PDF-Button
        pdf_button = table_row.find_element(By.XPATH, ".//button[contains(text(), 'PDF')]")
        pdf_button.click()
        time.sleep(5)  # Warten, bis das iframe geladen ist

        # Finden des iframe mit dem PDF-Link
        iframe = driver.find_element(By.XPATH, "//iframe[@type='application/pdf']")
        pdf_link = iframe.get_attribute('src')
        
    except Exception as e:
        print("PDF-Link oder Datum der letzten Änderung nicht gefunden.")
        print(e)
        driver.quit()
        return

    driver.quit()

    # Basis-URL entfernen, falls vorhanden
    if pdf_link.startswith("https://www.fedlex.admin.ch"):
        pdf_link_full = pdf_link
    else:
        pdf_link_full = f"https://www.fedlex.admin.ch{pdf_link}"
    
    # Altes PDF löschen
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    
    # Temporäre Datei für den Download
    temp_pdf_path = os.path.join(tempfile.gettempdir(), "temp_zivilgesetzbuch.pdf")
    print(f"Neues PDF gefunden. Herunterladen von {pdf_link_full}")
    download_pdf(pdf_link_full, temp_pdf_path)
    
    # Verschieben des heruntergeladenen PDFs ins Zielverzeichnis
    shutil.move(temp_pdf_path, pdf_path)
    print("PDF erfolgreich heruntergeladen und verschoben.")

    # Löschen von verbleibenden .crdownload-Dateien
    for file in os.listdir(pdf_directory):
        if file.endswith(".crdownload"):
            os.remove(os.path.join(pdf_directory, file))

# Hauptfunktion
def main():
    # Sicherstellen, dass das Verzeichnis existiert
    if not os.path.exists(pdf_directory):
        os.makedirs(pdf_directory)
    
    while True:
        try:
            check_for_update()
        except Exception as e:
            print(f"Fehler beim Überprüfen der Webseite: {e}")
        # Warten Sie eine Stunde, bevor Sie erneut überprüfen
        time.sleep(3600)

if __name__ == "__main__":
    main()
