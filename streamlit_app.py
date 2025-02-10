import streamlit as st
from openai import OpenAI
import os
import chardet

# �u?ng d?n d?n thu m?c ch?a c�c file hu?n luy?n
data_folder = "data"

def detect_encoding(file_path):
    with open(file_path, "rb") as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    return result["encoding"]

def load_training_data(folder_path):
    training_content = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            try:
                encoding = detect_encoding(file_path)
                with open(file_path, "r", encoding=encoding) as file:
                    training_content.append(file.read())
            except Exception as e:
                st.warning(f"?? Kh�ng th? d?c file: {filename} - L?i: {e}")
    return "\n\n".join(training_content)

# T?i d? li?u t? t?t c? c�c file trong thu m?c data
training_content = load_training_data(data_folder)

# Hi?n th? logo ? tr�n c�ng, can gi?a
try:
    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        st.image("logo.png", use_container_width=True)
except Exception:
    pass

# T�y ch?nh n?i dung ti�u d?
title_content = "?ng d?ng ChatMekomed"
st.markdown(f"""
    <h1 style="text-align: center; font-size: 24px;">{title_content}</h1>
    """, unsafe_allow_html=True)

# L?y OpenAI API key t? st.secrets.
openai_api_key = st.secrets.get("OPENAI_API_KEY")

# T?o OpenAI client.
client = OpenAI(api_key=openai_api_key)

# Ki?m tra n?i dung training
st.text_area("?? N?i dung training t? c�c file TXT:", training_content, height=300)

INITIAL_SYSTEM_MESSAGE = {
    "role": "system",
    "content": f"""
    B?n l� m?t chatbot tu v?n y t? c?a Mekomed. Du?i d�y l� th�ng tin chi ti?t t? t�i li?u hu?ng d?n:

    {training_content}

    ?? N?u ngu?i d�ng h?i v? d?ch v?, b?ng gi� ho?c c�c g�i kh�m s?c kh?e, h�y s? d?ng th�ng tin t? tr�n d? tr? l?i m?t c�ch ch�nh x�c nh?t.
    """,
}

INITIAL_ASSISTANT_MESSAGE = {
    "role": "assistant",
    "content": "MekomedChat xin ch�o! T�i c� th? gi�p g� cho b?n h�m nay?",
}

if "messages" not in st.session_state:
    st.session_state.messages = [INITIAL_SYSTEM_MESSAGE, INITIAL_ASSISTANT_MESSAGE]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("B?n nh?p n?i dung c?n trao d?i ? d�y nh�."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    messages_with_training = [INITIAL_SYSTEM_MESSAGE] + st.session_state.messages
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": m["role"], "content": m["content"]} for m in messages_with_training],
        stream=True,
    )
    
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
