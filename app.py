import streamlit as st
# from dotenv import load_dotenv

from src.ui import render_chat_page
from src.prompts import DEFAULT_SYSTEM_PROMPT, DEFAULT_MODEL


def init_session_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "system_prompt" not in st.session_state:
        st.session_state.system_prompt = DEFAULT_SYSTEM_PROMPT
    if "model" not in st.session_state:
        st.session_state.model = DEFAULT_MODEL
    if "temperature" not in st.session_state:
        st.session_state.temperature = 0.7


def main() -> None:
    # .env 파일 로드 (OPENAI_API_KEY 등)
    #load_dotenv()
    st.set_page_config(
        page_title="Streamlit Web Chatbot",
        page_icon="🤖",
        layout="wide",
    )

    init_session_state()
    render_chat_page()


if __name__ == "__main__":
    main()

