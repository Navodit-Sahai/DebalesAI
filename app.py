import sys
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
sys.path.append(str(Path(__file__).parent))

from src.agent import run_agent
from src.rag import build_index


st.set_page_config(page_title="Debales AI", page_icon="🤖")
st.title("🤖 Debales AI Assistant")


if "messages" not in st.session_state:
    st.session_state.messages = []


with st.sidebar:
    if st.button("Rebuild Index"):
        with st.spinner("Rebuilding..."):
            build_index(force=True)
        st.success("Done!")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


if prompt := st.chat_input("Ask something..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer = run_agent(prompt)
            except Exception as e:
                answer = f"Error: {e}"

        st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})