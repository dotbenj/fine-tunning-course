import json

# Charger les données Scryfall dump (bulk file)
with open("oracle-cards-20250404090221.json", encoding="utf-8") as f:
    cards = json.load(f)

# Fonction pour filtrer les commandants
def is_commander(card):
    # Exclure les cartes sans types
    if not card.get("type_line"):
        return False

    # Inclure uniquement les créatures légendaires
    is_legendary = "Legendary" in card["type_line"]
    is_creature = "Creature" in card["type_line"]

    # Vérifie la légalité Commander
    legal_commander = card.get("legalities", {}).get("commander") == "legal"

    return is_legendary and is_creature and legal_commander

# Appliquer le filtre
commanders = [card for card in cards if is_commander(card)]

# Sauvegarder le résultat
with open("filtered_commanders.json", "w", encoding="utf-8") as f:
    json.dump(commanders, f, indent=2, ensure_ascii=False)

print(f"{len(commanders)} commandants potentiels trouvés.")