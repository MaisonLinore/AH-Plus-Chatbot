import streamlit as st
import os
from openai import OpenAI

# Konfigurasi halaman
st.set_page_config(page_title="AH+ Chatbot", page_icon="🤖")
st.title("🤖 AH+ - Agentic Smart AI")

# Ambil API key dari Streamlit secrets (akan kita atur nanti)
api_key = st.secrets["OPENROUTER_API_KEY"]

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)
# Pilih model gratis populer di OpenRouter
MODEL = "mistralai/mistral-7b-instruct:free"

# Inisialisasi riwayat chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Anda adalah AH+, asisten AI yang cerdas dan membantu."}
    ]

# Tampilkan pesan sebelumnya
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Input dari pengguna
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
