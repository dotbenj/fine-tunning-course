import json
import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    DataCollatorForTokenClassification,
    TrainingArguments,
    Trainer,
    AutoConfig,
    TrainerCallback,
)
import evaluate

print(torch.cuda.is_available())  # Should print: True
print(torch.cuda.get_device_name(0))  # Should print something like: NVIDIA GeForce RTX 4070

class F1LoggerCallback(TrainerCallback):
    def __init__(self):
        self.f1_scores = []

    def on_evaluate(self, args, state, control, metrics, **kwargs):
        f1 = metrics.get("eval_overall_f1")
        if f1 is not None:
            self.f1_scores.append((state.epoch, f1))
            print(f"📊 F1 (epoch {state.epoch:.2f}): {f1:.4f}")

# ========== CHARGEMENT DU DATASET ==========
dataset = load_dataset(
    "json",
    data_files={
        "train": "ner_train.json",
        "validation": "ner_val.json",
        "test": "ner_test.json"
    },
    field=None
)

print(f"Train size: {len(dataset['train'])}")
print(f"Validation size: {len(dataset['validation'])}")
print(f"Test size: {len(dataset['test'])}")

# ========== ENCODAGE DES LABELS ==========
with open("label_list.json", "r") as f:
    label_list = json.load(f)

label_to_id = {label: i for i, label in enumerate(label_list)}
id_to_label = {i: label for label, i in label_to_id.items()}

# ========== TOKENIZER ==========
model_checkpoint = "bert-base-cased"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

def tokenize_and_align_labels(example):
    tokenized = tokenizer(
        example["tokens"],
        is_split_into_words=True,
        truncation=True,
        padding="max_length",
        max_length=128
    )

    word_ids = tokenized.word_ids()
    label_ids = []
    previous_word_idx = None

    for word_idx in word_ids:
        if word_idx is None:
            label_ids.append(-100)
        elif word_idx != previous_word_idx:
            label_ids.append(label_to_id[example["labels"][word_idx]])
        else:
            label_ids.append(label_to_id[example["labels"][word_idx]])
        previous_word_idx = word_idx

    tokenized["labels"] = label_ids
    return tokenized

tokenized_datasets = dataset.map(tokenize_and_align_labels, batched=False)

# ========== MODÈLE ==========
config = AutoConfig.from_pretrained(
    model_checkpoint,
    num_labels=len(label_list),
    id2label=id_to_label,
    label2id=label_to_id
)

model = AutoModelForTokenClassification.from_pretrained(
    model_checkpoint,
    config=config
)

# ========== DATA COLLATOR ==========
data_collator = DataCollatorForTokenClassification(tokenizer)

# ========== MÉTRIQUES ==========
metric = evaluate.load("seqeval")

def compute_metrics(p):
    predictions, labels = p
    predictions = predictions.argmax(-1)

    true_predictions = [
        [id_to_label[p] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]
    true_labels = [
        [id_to_label[l] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]

    return metric.compute(predictions=true_predictions, references=true_labels)

# ========== ARGUMENTS D'ENTRAÎNEMENT ==========
training_args = TrainingArguments(
    output_dir="./ner-archetype-model",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=5,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
    load_best_model_at_end=True,
    metric_for_best_model="eval_overall_f1",
    report_to="none"
)

f1_logger = F1LoggerCallback()

# ========== ENTRAÎNEMENT ==========
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
    callbacks=[f1_logger]
)

all_labels = set(label for example in dataset["train"] for label in example["labels"])
unknown_labels = all_labels - set(label_to_id.keys())

if unknown_labels:
    print("❌ Unrecognized labels found in dataset:", unknown_labels)
    exit(1)

trainer.train()

metrics = trainer.evaluate(eval_dataset=tokenized_datasets["test"])
print(metrics)

print("\n📈 Historique des F1-scores par epoch :")
for epoch, f1 in f1_logger.f1_scores:
    print(f"Epoch {epoch:.2f} → F1 = {f1:.4f}")

trainer.save_model("./ner-archetype-model")
tokenizer.save_pretrained("./ner-archetype-model")
