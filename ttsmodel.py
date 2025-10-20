import asyncio
import edge_tts
from pathlib import Path
import streamlit as st


#https://tts.travisvn.com/s

@st.cache_data
def text_speech(text:str, location:str,lang:str) -> Path :


    output_dir = Path("tts-output")
    output_dir.mkdir(parents=True, exist_ok=True)


    VOICE_CODES = {
        "English": "en-US-AriaNeural",
        "Hindi": "hi-IN-SwaraNeural",
        "Tamil": "ta-IN-PallaviNeural"
    }

    async def tts(text, file="output.wav", voice="en-US-AriaNeural"):
        communicate = edge_tts.Communicate(text, voice=voice)
        await communicate.save(file)

    out_file = output_dir / location
    asyncio.run(tts(text=text, file=str(out_file), voice=VOICE_CODES[lang]))

    return out_file
