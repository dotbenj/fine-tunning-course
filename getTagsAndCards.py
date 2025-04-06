import requests
from bs4 import BeautifulSoup
import time
import random
import re
from urllib.parse import urljoin
from tqdm import tqdm
import json
import os

BASE_URL = "https://edhrec.com"
TAGS_URL = f"{BASE_URL}/tags"
CACHE_FILE = "edhrec_tags_to_cards.json"
PAUSE_RANGE = (3.0, 6.0)  # Repos entre les requêtes pour éviter d'être bloqué

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def get_all_tags():
    print("🔍 Récupération des tags depuis edhrec.com/tags...")
    response = requests.get(TAGS_URL, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    tag_entries = soup.select("div.Card_container__Ng56K")
    print(f"✅ {len(tag_entries)} tags trouvés.")
    tags = []

    for entry in tag_entries:
        name_span = entry.select_one("div.CardLabel_label__iAM7T")
        # Voici une exemple du contenu du span 184367 Artifacts decks il faut extraire le nom du tag
        tag_name = re.sub(r"^\d+\s+|\s+decks$", "", name_span.text.strip().lower())
        print(f"✅ {tag_name} tags")
        link_a = f"/tags/{tag_name.replace(' ', '-')}"
        print(f"✅ {link_a} link")

        if name_span and link_a:
            tag_name = tag_name
            tag_url = urljoin(BASE_URL, link_a)
            tags.append({"name": tag_name, "url": tag_url})

    return tags

# def extract_card_names_from_tag_url(tag_url):
#     response = requests.get(tag_url, headers=HEADERS)
#     response.raise_for_status()
#     soup = BeautifulSoup(response.text, "html.parser")

#     card_links = soup.select('div[class^="CardImage_container"] > a[href]')
#     card_names = []

#     for a in card_links:
#         href = a["href"]
#         if href.startswith("/commanders/") or href.startswith("/cards/"):
#             name_part = href.split("/")[-1]
#             card_name = name_part.replace("-", " ").strip()
#             card_names.append(card_name)

#     return list(set(card_names))  # remove duplicates

def extract_card_names_from_tag_url(tag_url):
    response = requests.get(tag_url, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    card_names = [span.get_text(strip=True) for span in soup.select('span[class^="Card_name"]')]
    print(f"✅ {len(card_names)} card_names")
    return list(set(card_names))  # remove duplicates


def main():
    # Charger le cache s'il existe
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            tag_map = json.load(f)
    else:
        tag_map = {}

    tags = get_all_tags()
    print(f"✅ {len(tags)} tags trouvés.")

    for tag in tqdm(tags, desc="🔄 Traitement des tags"):
        tag_name = tag["name"]
        tag_url = tag["url"]
        print(f"🔄 Traitement de {tag_name}...")

        # Sauter les tags déjà traités
        if tag_name in tag_map:
            continue
        try:
            cards = extract_card_names_from_tag_url(tag_url)
            tag_map[tag_name] = cards
            # print(f"✅ {tag_name} → {len(cards)} cartes")
        except Exception as e:
            print(f"[Erreur] {tag_name} → {e}")

        # Sauvegarder après chaque tag
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(tag_map, f, indent=2, ensure_ascii=False)

        # Pause "humaine"
        pause = random.uniform(*PAUSE_RANGE)
        print(f"   ⏸️ Pause de {pause:.1f} secondes...\n")
        time.sleep(pause)

    print(f"📦 Terminé. Fichier sauvegardé dans {CACHE_FILE}")

if __name__ == "__main__":
    main()
