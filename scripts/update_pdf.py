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

        # Finden des iframe mit dem PDF-Li