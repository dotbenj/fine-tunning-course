import json
import time
import random
import os
import urllib.parse
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ====== CONFIG ======
INPUT_FILE = "filtered_commanders.json"
CACHE_FILE = "commander_tags.json"
PAUSE_RANGE = (3.0, 6.0)  # pause entre chaque commandeur
TAG_THRESHOLD = 5  # nombre min. de decks pour inclure un tag

# ====== SELENIUM SETUP ======
chrome_options = Options()
chrome_options.binary_location = "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"
chrome_options.add_argument("--headless=new")  # ✅ safer for WSL
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

def format_name_for_url(name):
    return urllib.parse.quote(name.lower().replace(" ", "-").replace(",", "").replace("'", "").replace("!", ""))

def fetch_edhrec_tags(commander_name):
    formatted_name = format_name_for_url(commander_name)
    url = f"https://edhrec.com/commanders/{formatted_name}"

    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        # Clic sur "More Tags..."
        try:
            input_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[placeholder="More Tags..."]')))
            input_field.click()
            time.sleep(1.5)
        except:
            print(f"[!] Pas de champ 'More Tags' pour {commander_name}")
            driver.quit()
            return []

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        tags = []

        print(soup.find_all("span", class_="me-4")[:5])  # Affiche les 5 premiers span
        
        tag_spans = soup.find_all("span", class_="me-4")
        for tag_span in tag_spans:
            count_span = tag_span.find_next_sibling("span")
            if not count_span:
                continue

            try:
                count_text = count_span.get_text(strip=True).replace(",", "")
                count = int(re.sub(r"[^\d]", "", count_text))
                if count > TAG_THRESHOLD:
                    tags.append(tag_span.get_text(strip=True))
            except ValueError:
                continue

        return list(set(tags))

    except Exception as e:
        print(f"[Erreur Selenium] {commander_name} : {e}")
        return []

# ====== SCRIPT PRINCIPAL ======

# Charger les commandants
with open(INPUT_FILE, encoding="utf-8") as f:
    commanders = json.load(f)

# Charger le cache si présent
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, encoding="utf-8") as f:
        cache = json.load(f)
else:
    cache = {}

# Filtrer les commandants déjà traités
remaining = [c for c in commanders if c["name"] not in cache]
print(f"➡️ {len(remaining)} commandants à traiter ({len(cache)} déjà en cache)")

# Scraping en mode "safe"
for i, card in enumerate(remaining, 1):
    name = card["name"]
    print(f"[{i}/{len(remaining)}] Traitement de {name}...")

    tags = fetch_edhrec_tags(name)
    cache[name] = tags

    print(f"   → {tags}")
    
    # Sauvegarder après chaque carte (résilient)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)

    # Pause entre les requêtes
    pause = random.uniform(*PAUSE_RANGE)
    print(f"   ⏸️ Pause de {pause:.2f} sec\n")
    time.sleep(pause)

print("✅ Scraping terminé et sauvegardé dans commander_tags.json.")
