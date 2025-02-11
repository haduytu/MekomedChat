import streamlit as st
from openai import OpenAI

# Đọc nội dung từ file 01.system_training.txt
def load_training_data():
    try:
        with open("01.system_trainning.txt", "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        st.error(f"Lỗi khi đọc file huấn luyện: {e}")
        return ""

# Tải dữ liệu từ file huấn luyện duy nhất
training_content = load_training_data()

# Hiển thị logo ở trên cùng, căn giữa
try:
    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        st.image("logo.png", use_container_width=True)
except Exception:
    pass

# Tùy chỉnh nội dung tiêu đề
title_content = "Ứng dụng ChatMekomed"
st.markdown(f"""
    <h1 style="text-align: center; font-size: 24px;">{title_content}</h1>
    """, unsafe_allow_html=True)

# Lấy OpenAI API key từ st.secrets.
openai_api_key = st.secrets.get("OPENAI_API_KEY")

# Tạo OpenAI client.
client = OpenAI(api_key=openai_api_key)

INITIAL_SYSTEM_MESSAGE = {
    "role": "system",
    "content": f"""
    Bạn là một chatbot tư vấn y tế của Mekomed. Dưới đây là thông tin chi tiết từ tài liệu hướng dẫn:

    {training_content}

    📌 Nếu người dùng hỏi về dịch vụ, bảng giá hoặc các gói khám sức khỏe, hãy sử dụng thông tin từ trên để trả lời một cách chính xác nhất.
    """,
}

INITIAL_ASSISTANT_MESSAGE = {
    "role": "assistant",
    "content": "MekomedChat xin chào! Tôi có thể giúp gì cho bạn hôm nay?",
}

if "messages" not in st.session_state:
    st.session_state.messages = [INITIAL_SYSTEM_MESSAGE, INITIAL_ASSISTANT_MESSAGE]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Bạn nhập nội dung cần trao đổi ở đây nhé."):
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
