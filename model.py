import torch
import warnings
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
import streamlit as st

@st.cache_resource
def load_model(device:torch.device):
    model_path = "./model/mbart"
    tokeniser_path = "./model/mbart-tokenizer"
    
    model = MBartForConditionalGeneration.from_pretrained(model_path).to(device)  # pyright: ignore[reportArgumentType]
    tokenizer = MBart50TokenizerFast.from_pretrained(tokeniser_path)
    return model, tokenizer
    

warnings.filterwarnings("ignore", message="Moving the following attributes")

@st.cache_data
def translate_text(text, source_lang:str, target_lang:str) -> str:

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Running on: {device}")

    model, tokenizer = load_model(device=device)

    article_hi = "संयुक्त राष्ट्र के प्रमुख का कहना है कि सीरिया में कोई सैन्य समाधान नहीं है"

    tokenizer.src_lang = source_lang
    encoded = tokenizer(text, return_tensors="pt").to(device)
    generated_hi = model.generate(
        **encoded,
        forced_bos_token_id=tokenizer.lang_code_to_id[target_lang],
        max_length=256,
        num_beams=5,
        early_stopping=True
    )
    return tokenizer.batch_decode(generated_hi, skip_special_tokens=True)[0]
