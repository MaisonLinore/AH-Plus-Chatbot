import streamlit as st
from openai import OpenAI

# Judul sederhana (tanpa logo robot, tanpa "Agentic Smart AI")
st.title("AH Plus")

api_key = st.secrets["OPENROUTER_API_KEY"]

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    default_headers={
        "Authorization": f"Bearer {api_key}",          # header wajib
        "HTTP-Referer": "https://ah-plus-chatbot.streamlit.app",
        "X-Title": "AH Plus"
    }
)

MODEL = "mistralai/mistral-7b-instruct:free"

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Anda adalah AH Plus, asisten AI yang cerdas."}]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if prompt := st.chat_input("Tanyakan sesuatu ke AH Plus..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("..."):
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
                st.error(f"Error: {e}")
