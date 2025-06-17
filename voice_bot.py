import streamlit as st
import openai
from gtts import gTTS
import tempfile

# Load your OpenAI API Key from secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Pranay Voice Bot")
st.title("🎙️ Pranay's Voice Bot")

# JS + HTML for voice input using browser mic
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
      document.getElementById('input-box').value = e.results[0][0].transcript;
      document.getElementById('submit-button').click();
      recognition.stop();
    };
    recognition.onerror = function(e) {
      recognition.stop();
    };
  }
}
</script>
""", unsafe_allow_html=True)

# HTML form
st.markdown("""
<input id="input-box" type="text" name="query" placeholder="Click mic and speak" style="width:100%;padding:10px;font-size:16px;" />
<button onclick="startDictation()" style="margin-top:10px;padding:10px 20px;font-size:16px;">🎤 Start Recording</button>
""", unsafe_allow_html=True)

query = st.text_input("Or type here (fallback):", key="query_input")
submit = st.button("🔊 Submit", key="submit-button")

if submit and query:
    st.subheader("You asked:")
    st.write(query)

    with st.spinner("Thinking..."):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": (
                    "You are Gaddam Pranay, a calm and technically strong R&D ML Engineer at Enspar AI. "
                    "You work on applied ML for industrial automation and GenAI systems. "
                    "You’ve built projects like Seetha, MathAgent, and CodeIterator. "
                    "You graduated from Vel Tech University with a B.Tech in ECE (CGPA 8.39). "
                    "Speak in first person — honest, natural, not robotic. Born in Kadapa, Andhra Pradesh."
                )},
                {"role": "user", "content": query}
            ]
        )
        reply = response.choices[0].message.content
        st.subheader("Pranay says:")
        st.write(reply)

        # Convert reply to audio
        tts = gTTS(reply)
        temp_path = tempfile.mktemp(suffix=".mp3")
        tts.save(temp_path)
        st.audio(temp_path, format="audio/mp3")
