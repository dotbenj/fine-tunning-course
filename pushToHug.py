from huggingface_hub import HfApi
from huggingface_hub.utils import HfHubHTTPError
from huggingface_hub import upload_folder


api = HfApi()
model_name = "ner-mtg-archetype"
user = api.whoami()["name"]
repo_id = f"{user}/{model_name}"

try:
    api.create_repo(repo_id=repo_id, private=False)
    print(f"✅ Repository created: https://huggingface.co/{repo_id}")
except HfHubHTTPError as e:
    if "already exists" in str(e):
        print(f"⚠️ Repository already exists: https://huggingface.co/{repo_id}")
    else:
        raise

upload_folder(
    repo_id=repo_id,
    folder_path="./ner-archetype-model",
    commit_message="Initial commit of NER MTG archetype model"
)

print(f"📦 Model uploaded to: https://huggingface.co/{repo_id}")