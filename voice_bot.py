import streamlit as st
import openai
from gtts import gTTS
import tempfile

# Load API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Pranay Voice Bot", layout="centered")
st.title("🎙️ Pranay's Voice Bot")

# JavaScript: Voice Input using Web Speech API (browser mic)
st.markdown("""
    <script>
    function startDictation() {
      if (window.hasOwnProperty('webkitSpeechRecognition')) {
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = "en-US";
        recognition.start();
        recognition.onresult = function(e) {
          document.getElementById('input-text').value = e.results[0][0].transcript;
          document.getElementById('input-form').dispatchEvent(new Event('submit', { bubbles: true }));
          recognition.stop();
        };
        recognition.onerror = function(e) {
          recognition.stop();
        };
      }
    }
    </script>
""", unsafe_allow_html=True)

# System prompt based on Pranay's resume and personality
system_prompt = {
    "role": "system",
    "content": (
        "You are a voice-based AI assistant speaking as Gaddam Pranay — a calm, grounded, and technically sharp R&D Engineer currently working at Enspar Energy Solutions. "
        "Pranay has hands-on experience in building AI-powered systems for industrial automation and predictive maintenance. "
        "At Enspar, he works on applied ML and collaborates with CSIR-CSIO to deploy optimized models on hardware-constrained devices. "
        "He completed his Bachelor of Technology in Electronics and Communication Engineering from Vel Tech University, Chennai, graduating in May 2023 with a CGPA of 8.39. "
        "His side projects include Seetha (a local LLM assistant with memory and web search), MathAgent (a RAG-based reasoning tutor), and Code Iterator (an AI-powered code refactoring tool using AST). "
        "Academic projects include a YOLO-based traffic signal detector, deep learning for oral cancer detection, and a hybrid quantum-classical ECG classifier. "
        "He speaks in first person, naturally and clearly, like a human — with humility, curiosity, and confidence. Avoid sounding robotic or generic. Respond like Pranay would in a real interview. "
        "He was born and raised in Kadapa, Andhra Pradesh."
    )
}

# Input form with a browser-based mic interface
with st.form(key='input-form'):
    st.markdown('<input type="text" id="input-text" name="query" placeholder="Click mic and speak..." '
                'style="width: 100%; padding: 10px; font-size: 16px;" />', unsafe_allow_html=True)
    submit_button = st.form_submit_button(label='🔊 Ask with Voice')

    st.markdown('<button onclick="startDictation()" style="margin-top: 10px; padding: 8px 16px; font-size: 16px;">🎤 Start Recording</button>',
                unsafe_allow_html=True)

# Response processing
if submit_button:
    query = st.experimental_get_query_params().get('query', [st.session_state.get('query', '')])[0]
    if not query:
        query = st.text_input("Or type your question:")

    if query:
        st.subheader("You asked:")
        st.write(query)

        with st.spinner("🤖 Thinking..."):
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    system_prompt,
                    {"role": "user", "content": query}
                ]
            )
            answer = response.choices[0].message.content
            st.subheader("Pranay says:")
            st.write(answer)

            tts = gTTS(answer)
            tts_path = tempfile.mktemp(suffix=".mp3")
            tts.save(tts_path)
            st.audio(tts_path, format="audio/mp3")
