from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch

# ====== Charger le modèle fine-tuné et le tokenizer ======
model_dir = "./ner-archetype-model"
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForTokenClassification.from_pretrained(model_dir)

DEBUG = False  # Passe à True pour activer le debug complet

if DEBUG:
    print("📋 id2label mapping:", model.config.id2label)

# ====== Fonction d'inférence ======
def predict_archetypes(text):
    model.eval()
    inputs = tokenizer(text, return_tensors="pt", truncation=True)

    with torch.no_grad():
        outputs = model(**inputs)

    predictions = outputs.logits.argmax(-1)[0]
    tokens = tokenizer.tokenize(text)
    label_ids = predictions.tolist()
    labels = [model.config.id2label[i] for i in label_ids]

    found_archetypes = set()

    if DEBUG:
        print("\n🔍 Debug complet :\n")
        for token, label in zip(tokens, labels[1:-1]):  # Ignorer [CLS] et [SEP]
            print(f"{token:15} → {label}")

    print("\n🔍 Résultats d'inférence :\n")
    for token, label in zip(tokens, labels[1:-1]):
        if label != "O":
            print(f"{token:15} → {label}")

            if "-" in label:
                prefix, archetype = label.split("-", 1)
                found_archetypes.add(archetype)

    if found_archetypes:
        print(f"\n✅ Archetypes found: {sorted(found_archetypes)}")
    else:
        print("\n❌ No archetypes detected.")


# ====== Entrée utilisateur ======
if __name__ == "__main__":
    print("\n🧙‍♂️ Magic: The Gathering Archetype NER")
    print("Type or paste the Oracle text of a card below:\n")

    while True:
        user_input = input("📝 Text > ").strip()
        if not user_input:
            print("🚪 Exiting...")
            break

        predict_archetypes(user_input)
        print("\n---\n")