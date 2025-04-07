import json

# Load the archetype definitions
with open("edhrec_tags_to_cards.json", "r", encoding="utf-8") as f:
    archetype_to_keywords = json.load(f)

# Create a label list with BIO format
label_list = ["O"]  # Start with 'O' for Outside

for archetype in archetype_to_keywords:
    formatted = archetype.strip().replace(" ", "_").replace("-", "_")
    label_list.append(f"B-{formatted}")
    label_list.append(f"I-{formatted}")

# Optional: Sort for consistency (excluding 'O')
label_list = ["O"] + sorted(label_list[1:])

# Save to file
with open("label_list.json", "w", encoding="utf-8") as f:
    json.dump(label_list, f, indent=2)

# Print preview
print("✅ Generated label_list:")
print(label_list)