import streamlit as st
from io import BytesIO
import tempfile
import os
from model import translate_text
from ttsmodel import text_speech
import uuid
from pathlib import Path
from speech_recog import recognise_speech


LANGUAGE_CODES = {
    "English": "en_XX",
    "Hindi": "hi_IN",
    "Tamil": "ta_IN",
}
whisper_languages = {
    "Tamil": "ta",
    "Hindi": "hi",
    "English": "en"
}

import re

def preprocess_text(text, target_lang="ta"):

    unicode_ranges = {
        "ta": r'[\u0B80-\u0BFF]',  
        "hi": r'[\u0900-\u097F]',  
        "en": r'[A-Za-z]'           
    }

    if target_lang not in unicode_ranges:
        raise ValueError("Target language not supported. Use 'ta', 'hi', or 'en'.")

    pattern = unicode_ranges[target_lang]
    
    # Split into words and keep only words containing target language characters
    words = text.split()
    filtered_words = [word for word in words if re.search(pattern, word)]
    
    return " ".join(filtered_words)


def transcribe_audio(audio_file, source_lang="en"):
    return "This is a transcribed example from audio input."

def synthesize_speech(text, lang="en"):
    dummy_audio = BytesIO()
    dummy_audio.write(b"FAKEAUDIO")
    dummy_audio.seek(0)
    return dummy_audio

st.set_page_config(page_title="Universal Translator", page_icon="🌐", layout="centered")

st.title("🌐 Universal Language Translator")
st.write("Translate text or speech across languages with natural native-style audio output.")


feature = st.radio(
    "Select Translation Mode:",
    [
        "Text ➜ Text",
        "Text ➜ Audio",
        "Audio ➜ Text",
        "Audio ➜ Audio"
    ]
)

col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox(
        label="Source Language",
        options=list(LANGUAGE_CODES.keys()),
        index=list(LANGUAGE_CODES.keys()).index("English") 
    )

with col2:
    target_lang = st.selectbox(
        label="Target Language",
        options=list(LANGUAGE_CODES.keys()),
        index=list(LANGUAGE_CODES.keys()).index("Tamil")
    )

if source_lang != target_lang:
    if feature == "Text ➜ Text":
        text_input = st.text_area("Enter text to translate:")
        if st.button("Translate"):
            with st.spinner("Translating..."):
                if text_input.strip():
                    translation = translate_text(text_input, LANGUAGE_CODES[source_lang], LANGUAGE_CODES[target_lang])
                    st.success(f"**Translated Text:** {translation}")
                else:
                    st.warning("Please enter text to translate.")

    elif feature == "Text ➜ Audio":
        text_input = st.text_area("Enter text to translate & speak:")
        if st.button("Translate & Speak"):
            with st.spinner("Translating & Speaking..."):
                if text_input.strip():
                    translation = translate_text(text_input, LANGUAGE_CODES[source_lang], LANGUAGE_CODES[target_lang])
                    file_name = str(uuid.uuid4()) + ".wav"
                    audio_data = text_speech(translation, location=file_name, lang=target_lang)
                    st.audio(audio_data, format="audio/wav")
                else:
                    st.warning("Please enter text to translate.")


    elif feature == "Audio ➜ Text":
        uploaded_audio = st.file_uploader("Upload an audio file", type=["wav", "mp3", "m4a"])
        if uploaded_audio and st.button("Transcribe & Translate"):

            with st.spinner("Transcribing & Translating..."):
                upload_folder = "./uploaded_audio"
                os.makedirs(upload_folder, exist_ok=True)  

                file_path = os.path.join(upload_folder, uploaded_audio.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_audio.read())


                text_from_audio = recognise_speech(file_path,whisper_languages[source_lang])
                translation = translate_text(text_from_audio, LANGUAGE_CODES[source_lang], LANGUAGE_CODES[target_lang])
                st.success(f"**Transcribed Text:** {text_from_audio}")
                st.success(f"**Translated Text:** {translation}")

                # Optionally, remove the file after processing
                os.remove(file_path)


    elif feature == "Audio ➜ Audio":
        uploaded_audio = st.file_uploader("Upload an audio file", type=["wav", "mp3", "m4a"])
        if uploaded_audio and st.button("Transcribe & Translate"):

            with st.spinner("Transcribing & Translating..."):
                upload_folder = "./uploaded_audio"
                os.makedirs(upload_folder, exist_ok=True)  

                file_path = os.path.join(upload_folder, uploaded_audio.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_audio.read())


                text_from_audio = recognise_speech(file_path,whisper_languages[source_lang])
                translation = translate_text(text_from_audio, LANGUAGE_CODES[source_lang], LANGUAGE_CODES[target_lang])
                file_name = str(uuid.uuid4()) + ".wav"
                audio_data = text_speech(translation, location=file_name, lang=target_lang)
                st.audio(audio_data, format="audio/wav")

                # Optionally, remove the file after processing
                os.remove(file_path)
else:
    st.warning("Source and target languages cannot be the same.")