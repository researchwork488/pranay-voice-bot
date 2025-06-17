# Pranay's Voice Bot 🎙️

A simple voice bot built using Streamlit, OpenAI GPT, and Google Text-to-Speech (gTTS).
It listens to a user's voice, transcribes it, sends it to ChatGPT with Pranay's personality, and speaks the response aloud.

## Features
- 🎤 Voice Input (SpeechRecognition)
- 🤖 GPT-4 API Integration
- 🔊 Voice Output using gTTS
- 🌐 Deployed using Streamlit Cloud

## Run Locally
1. Clone this repo
2. Create a `secrets.toml` file in `.streamlit` folder:
```
OPENAI_API_KEY = "your-api-key"
```
3. Install dependencies:
```
pip install -r requirements.txt
```
4. Run the app:
```
streamlit run voice_bot.py
```

## Submission
This bot was built for a Gen AI Engineer assignment (Home.LLC). It reflects Pranay's own responses and personality.
