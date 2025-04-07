import json
import re
import random
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer

INPUT_FILE = "ner_dataset_raw.json"
KEYWORD_FILE = "archetype_to_keywords.json"
LABEL_LIST_FILE = "label_list.json"
TOKENIZER_NAME = "bert-base-cased"
DEBUG = False

# Load files
with open(INPUT_FILE, encoding="utf-8") as f:
    raw_data = json.load(f)

with open(KEYWORD_FILE, encoding="utf-8") as f:
    archetype_to_keywords = json.load(f)

with open(LABEL_LIST_FILE, encoding="utf-8") as f:
    label_list = json.load(f)
valid_labels = set(label_list)

# Initialize tokenizer
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_NAME)

def normalize_archetype(archetype):
    return archetype.replace(" ", "_").replace("-", "_")

def annotate_tokens(text, tags):
    encoding = tokenizer(text, return_offsets_mapping=True, return_tensors="pt", truncation=True)
    tokens = tokenizer.convert_ids_to_tokens(encoding["input_ids"][0])[1:-1]  # Skip [CLS] and [SEP]
    offsets = encoding["offset_mapping"][0].tolist()[1:-1]

    labels = ["O"] * len(tokens)
    token_tagged = [False] * len(tokens)
    text_lower = text.lower()

    for tag in tags:
        if tag not in archetype_to_keywords:
            continue  # Tag has no keywords
        norm_tag = normalize_archetype(tag)
        b_label = f"B-{norm_tag}"
        i_label = f"I-{norm_tag}"

        if b_label not in valid_labels:
            continue  # Skip if tag is not in label list

        for keyword in archetype_to_keywords[tag]:
            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            for match in re.finditer(pattern, text_lower):
                start, end = match.start(), match.end()
                matched_tokens = []

                for i, (tok_start, tok_end) in enumerate(offsets):
                    if tok_end <= start:
                        continue
                    if tok_start >= end:
                        break
                    if tok_start < end and tok_end > start and not token_tagged[i]:
                        matched_tokens.append(i)

                if matched_tokens:
                    labels[matched_tokens[0]] = b_label
                    for i in matched_tokens[1:]:
                        labels[i] = i_label
                    for i in matched_tokens:
                        token_tagged[i] = True

                    if DEBUG:
                        print(f"[DEBUG] Matched '{keyword}' as '{text[start:end]}' for tag '{tag}'")

    return tokens, labels

# Build the dataset
ner_examples = []
print("🔍 Annotating NER data...")
for entry in tqdm(raw_data):
    text = entry["text"]
    tags = entry["tags"]
    tokens, labels = annotate_tokens(text, tags)
    ner_examples.append({"tokens": tokens, "labels": labels})

# Shuffle and split
random.seed(42)
random.shuffle(ner_examples)

n = len(ner_examples)
train_split = int(n * 0.7)
val_split = int(n * 0.85)

train = ner_examples[:train_split]
val = ner_examples[train_split:val_split]
test = ner_examples[val_split:]

# Save the datasets
print("💾 Saving datasets...")
with open("ner_train.json", "w", encoding="utf-8") as f:
    json.dump(train, f, indent=2, ensure_ascii=False)

with open("ner_val.json", "w", encoding="utf-8") as f:
    json.dump(val, f, indent=2, ensure_ascii=False)

with open("ner_test.json", "w", encoding="utf-8") as f:
    json.dump(test, f, indent=2, ensure_ascii=False)

print(f"✅ Done! Dataset sizes — train: {len(train)}, val: {len(val)}, test: {len(test)}")
