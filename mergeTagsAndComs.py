# import json

# # Fichiers d'entrée
# CARDS_FILE = "filtered_commanders.json"
# TAGS_FILE = "commander_tags.json"
# OUTPUT_FILE = "ner_dataset_raw.json"

# # Charger les cartes
# with open(CARDS_FILE, encoding="utf-8") as f:
#     cards = json.load(f)

# # Charger les tags
# with open(TAGS_FILE, encoding="utf-8") as f:
#     tags_by_name = json.load(f)

# merged = []

# for card in cards:
#     name = card.get("name")
#     oracle_text = card.get("oracle_text", "").strip()
#     type_line = card.get("type_line", "").strip()
#     tags = tags_by_name.get(name, [])

#     if not oracle_text or not type_line or not tags:
#         continue  # On ne garde que les cartes avec toutes les infos utiles

#     merged.append({
#         "name": name,
#         "text": f"{oracle_text} {type_line}",
#         "tags": tags
#     })

# # Sauvegarde
# with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
#     json.dump(merged, f, indent=2, ensure_ascii=False)

# print(f"✅ Merge terminé : {len(merged)} entrées sauvegardées dans {OUTPUT_FILE}")


import json
import re
from tqdm import tqdm

# Load files
with open("oracle-cards-20250404090221.json", "r", encoding="utf-8") as f:
    scryfall_cards = json.load(f)

with open("edhrec_tags_to_cards.json", "r", encoding="utf-8") as f:
    edhrec_tags_to_cards = json.load(f)

with open("archetype_to_keywords.json", "r", encoding="utf-8") as f:
    archetype_to_keywords = json.load(f)

# Preprocess: map card names to tags from EDHREC
card_name_to_tags = {}
for tag, card_names in edhrec_tags_to_cards.items():
    for name in card_names:
        name_lower = name.lower()
        card_name_to_tags.setdefault(name_lower, []).append(tag)

# Process Scryfall cards
ner_dataset_raw = []
for card in tqdm(scryfall_cards):
    name = card.get("name")
    oracle_text = card.get("oracle_text", "")
    type_line = card.get("type_line", "")
    full_text = f"{oracle_text}\n{type_line}".strip()

    name_lower = name.lower()

    tags = set()

    # Tags from EDHREC
    tags.update(card_name_to_tags.get(name_lower, []))

    # Tags from keywords found in card text
    text_lower = full_text.lower()
    for archetype, keywords in archetype_to_keywords.items():
        for keyword in keywords:
            # Escape the keyword for safe regex matching
            escaped_keyword = re.escape(keyword.lower())

            # Match full words or phrases only, not partial words
            pattern = r'\b' + escaped_keyword + r'\b'

            if re.search(pattern, text_lower):
                tags.add(archetype)
                break

    if tags:
        ner_dataset_raw.append({
            "name": name,
            "text": full_text,
            "tags": sorted(tags)
        })

# Save final NER dataset
with open("ner_dataset_raw.json", "w", encoding="utf-8") as f:
    json.dump(ner_dataset_raw, f, indent=2, ensure_ascii=False)
