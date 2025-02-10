import streamlit as st
from openai import OpenAI

def rfile(name_file):
    with open(name_file, "r", encoding="utf-8") as file:
        content_sys = file.read()
    return content_sys

# Hi?n th? logo ? trên cùng, can gi?a
try:
    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        st.image("logo.png", use_container_width=True)
except Exception as e:
    pass

# Tùy ch?nh n?i dung tiêu d?
title_content = rfile("00.xinchao.txt")

st.markdown(
    f"""
    <h1 style="text-align: center; font-size: 24px;">{title_content}</h1>
    """,
    unsafe_allow_html=True
)

# L?y OpenAI API key t? st.secrets.
openai_api_key = st.secrets.get("OPENAI_API_KEY")

# T?o OpenAI client.
client = OpenAI(api_key=openai_api_key)

#user_name = st.session_state.get("customer_name", "B?n")

INITIAL_SYSTEM_MESSAGE = {
    "role": "system",
    "content": f"""
    {rfile("01.system_trainning.txt")}
    
    #?? Trong cu?c trò chuy?n này, khách hàng tên là t? thông tin khách hàng nh?p vào. Hãy luôn xung hô v?i h? theo quy t?c trên.
    #""",
}

INITIAL_ASSISTANT_MESSAGE = {
    "role": "assistant",
    "content": rfile("02.assistant.txt"),
}

if "messages" not in st.session_state:
    st.session_state.messages = [INITIAL_SYSTEM_MESSAGE, INITIAL_ASSISTANT_MESSAGE]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


if prompt := st.chat_input(f"B?n nh?p n?i dung c?n trao d?i ? dây nhé."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    stream = client.chat.completions.create(
        model=rfile("module_chatgpt.txt").strip(),
        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        stream=True,
    )
    
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
