import streamlit as st
import requests
import json

st.set_page_config(page_title="AH+ Chatbot", page_icon="🤖")
st.title("🤖 AH+ - Agentic Smart AI")

# Ambil API key dari secrets
api_key = st.secrets["OPENROUTER_API_KEY"]

# Pastikan API key tidak kosong
if not api_key:
    st.error("API key tidak ditemukan. Periksa kembali Secrets Anda.")
    st.stop()

# --- Fungsi untuk memanggil API OpenRouter secara manual ---
def call_openrouter(messages):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": messages,
        }
    )
    # Kembalikan respons JSON atau error jika terjadi
    return response.json()

# --- Inisialisasi riwayat chat ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Anda adalah AH+, asisten AI yang cerdas dan membantu."}]

# Tampilkan pesan sebelumnya
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Input pengguna
if prompt := st.chat_input("Tanyakan sesuatu ke AH+..."):
    # Tambahkan pesan pengguna ke riwayat
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Tampilkan pesan pengguna di chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Panggil API dan dapatkan respons
    with st.chat_message("assistant"):
        with st.spinner("AH+ sedang berpikir..."):
            try:
                # Panggil fungsi yang telah kita buat
                result = call_openrouter(st.session_state.messages)
                
                # Cek apakah respons mengandung error
                if 'error' in result:
                    st.error(f"Error dari API: {result['error'].get('message', 'Unknown error')}")
                else:
                    # Ambil isi pesan dari respons yang berhasil
                    response_content = result['choices'][0]['message']['content']
                    st.markdown(response_content)
                    # Simpan respons asisten ke riwayat
                    st.session_state.messages.append({"role": "assistant", "content": response_content})
            except Exception as e:
                st.error(f"Terjadi kesalahan saat memanggil API: {e}")
