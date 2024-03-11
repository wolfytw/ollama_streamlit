import streamlit as st
import ollama
from typing import Dict, Generator


def ollama_generator(model_name: str, messages: Dict) -> Generator:
    stream = ollama.chat(
        model=model_name, messages=messages, stream=True)
    for chunk in stream:
        yield chunk['message']['content']


st.title("Ollama 使用 Streamlit應用 demo")
# 儲存網頁狀態
if "selected_model" not in st.session_state:
    st.session_state.selected_model = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
# 透過st.selectbox建立語言模型選單（電腦內有pull過的模型）
st.session_state.selected_model = st.selectbox(
    "請選擇己下載的模型:", [model["name"] for model in ollama.list()["models"]])

# 顯示使用者訊息和儲存語言模型輸出
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if prompt := st.chat_input("能為您做些什麼?"):
    # 儲存使用者訊息
    st.session_state.messages.append({"role": "user", "content": prompt})
    # 顯示對話窗
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.write_stream(ollama_generator(
            st.session_state.selected_model, st.session_state.messages))
    # 儲存語言模型輸出
    st.session_state.messages.append(
        {"role": "assistant", "content": response})
    
    