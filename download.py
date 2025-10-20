from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
from pathlib import Path

model_name = "facebook/mbart-large-50-many-to-many-mmt"
tokenizer = MBart50TokenizerFast.from_pretrained(model_name)
model = MBartForConditionalGeneration.from_pretrained(model_name)

# 🔹 Save both model and tokenizer to a local folder
model_path = Path('model/mbart')
tokeniser_path = Path('model/mbart-tokenizer')
if not model_path.exists():
    model_path.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(model_path)
else:
    print("Model already exists. Skipping saving.")
if not tokeniser_path.exists():
    Path(tokeniser_path).mkdir(parents=True, exist_ok=True)
    tokenizer.save_pretrained(tokeniser_path)
else:
    print("Tokeniser already exists. Skipping saving.")
