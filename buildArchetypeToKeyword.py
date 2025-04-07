import json

INPUT_FILE = "edhrec_tags_to_cards.json"
OUTPUT_FILE = "archetype_to_keywords.json"

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        tag_to_cards = json.load(f)

    archetype_to_keywords = {tag: [] for tag in tag_to_cards.keys()}

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(archetype_to_keywords, f, indent=2, ensure_ascii=False)

    print(f"✅ Fichier {OUTPUT_FILE} généré avec {len(archetype_to_keywords)} tags, prêt à remplir à la main.")

if __name__ == "__main__":
    main()
