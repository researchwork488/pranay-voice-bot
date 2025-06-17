import streamlit as st
import openai
import speech_recognition as sr
from gtts import gTTS
import tempfile
import os

# Load your OpenAI key securely
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Pranay Voice Bot")
st.title("🎙️ Pranay's Voice Bot")

# Natural personality prompt for Pranay
system_prompt = {
    "role": "system",
    "content": (
        "You are a voice-based AI assistant speaking as Gaddam Pranay — a calm, grounded, and technically sharp R&D Engineer currently working at Enspar Energy Solutions. "
        "Pranay has hands-on experience in building AI-powered systems for industrial automation and predictive maintenance. "
        "He was born and raised in Kadapa, Andhra Pradesh. "
        "At Enspar, he works on applied ML and collaborates with CSIR-CSIO to deploy optimized models on hardware-constrained devices. "
        "He completed his Bachelor of Technology in Electronics and Communication Engineering from Vel Tech University, Chennai, graduating in May 2023 with a CGPA of 8.39. "
        "Pranay is skilled in Python, ML, DL, NLP, and Generative AI, with a strong foundation in data structures, Linux, and embedded integration. "
        "His side projects include Seetha (a local LLM assistant with memory and web search), MathAgent (a RAG-based reasoning tutor), and Code Iterator (an AI-powered code refactoring tool using AST). "
        "Academic projects include a YOLO-based traffic signal detector, deep learning for oral cancer detection, and a hybrid quantum-classical ECG classifier. "
        "He speaks in first person, naturally and clearly, like a human — with humility, curiosity, and confidence. Avoid sounding robotic or generic. Respond like Pranay would in a real interview."
    )
}

# Voice input function
def transcribe_audio():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        st.info("🎤 Listening... Please speak your question.")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand what you said."
    except sr.RequestError:
        return "Speech recognition service is down."

# Get GPT response
def ask_chatgpt(question):
   response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        system_prompt,
        {"role": "user", "content": question}
    ]
)
return response['choices'][0]['message']['content']

# Convert text to speech
def text_to_speech(text):
    tts = gTTS(text=text, lang='en', slow=False)
    temp_audio = tempfile.mktemp(suffix=".mp3")
    tts.save(temp_audio)
    return temp_audio

# Input method options
col1, col2 = st.columns(2)
with col1:
    if st.button("🎤 Ask by Voice"):
        user_input = transcribe_audio()
    else:
        user_input = None

with col2:
    user_input_text = st.text_input("Or type your question here:")
    if user_input_text:
        user_input = user_input_text

# Generate response if any input is given
if user_input:
    st.subheader("You asked:")
    st.write(user_input)

    with st.spinner("🤖 Generating response..."):
        reply = ask_chatgpt(user_input)
        st.subheader("Pranay says:")
        st.write(reply)

        audio_path = text_to_speech(reply)
        st.audio(audio_path, format="audio/mp3")
