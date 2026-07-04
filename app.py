import streamlit as st

from core.rag_chain import load_vector_store
from ui.sidebar import render_sidebar
from ui.chat import render_chat
from ui.styles import load_css

st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="🧠",
    layout="wide",
)

load_css()

st.title("🧠 AI Knowledge Assistant")

st.markdown("""
Chat intelligently with your documents using **Retrieval-Augmented Generation (RAG)**.

Built with **Gemini 2.5 Flash**, **LangChain**, **FAISS**, and **Hugging Face Embeddings**.
""")

st.divider()

@st.cache_resource
def get_vector_store():
    return load_vector_store()

vector_store = get_vector_store()

render_sidebar(vector_store)
render_chat(vector_store)