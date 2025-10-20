import whisper
import streamlit as st
import torch

@st.cache_resource
def get_model():
    # Load Whisper model
    model = whisper.load_model("small")  
    model.to("cuda" if torch.cuda.is_available() else "cpu")
    return model

@st.cache_data
def recognise_speech(audio_file,code):
    model = get_model()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    result = model.transcribe(audio_file,language=code)
    print(result["text"])
    return result['text'] if 'text' in result else ""
