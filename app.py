import streamlit as st
import os
from openai import OpenAI

st.set_page_config(page_title="AH+ Chatbot", page_icon="🤖")
st.title("🤖 AH+ - Agentic Smart AI")

# Cara baca API key yang lebih aman
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
except:
    api_key = None

if not api_key:
    st.error("❌ API Key tidak ditemukan. Pastikan Anda sudah mengisi OPENROUTER_API_KEY di Secrets Streamlit.")
    st.stop()

# Inisialisasi client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    default_headers={
        "HTTP-Referer": "https://ah-plus-chatbot.streamlit.app",  # ganti dengan URL app Anda
        "X-Title": "AH+ Chatbot"
    }
)

MODEL = "mistralai/mistral-7b-instruct:free"

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Anda adalah AH+, asisten AI yang cerdas dan membantu."}]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if prompt := st.chat_input("Tanyakan sesuatu ke AH+..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("AH+ sedang berpikir..."):
            try:
                completion = client.chat.completions.create(
                    model=MODEL,
                    messages=st.session_state.messages,
                    temperature=0.7,
                )
                response = completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
