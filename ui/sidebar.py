from pathlib import Path
import streamlit as st
from core.ingest import build_knowledge_base


def render_sidebar(vector_store):

    st.sidebar.title("📄 Knowledge Base")
    st.sidebar.success("Status: Ready")
    st.sidebar.markdown("---")

    # Upload PDFs
    uploaded_files = st.sidebar.file_uploader(
        "Upload PDF Documents",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        pdf_dir = Path("data/pdfs")
        pdf_dir.mkdir(parents=True, exist_ok=True)

        for uploaded_file in uploaded_files:
            save_path = pdf_dir / uploaded_file.name

            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

        st.sidebar.success("✅ PDFs uploaded successfully!")

    # Rebuild Knowledge Base
    if st.sidebar.button("🔄 Rebuild Knowledge Base"):

        with st.spinner("Building Knowledge Base..."):
            build_knowledge_base()

        st.cache_resource.clear()
        st.sidebar.success("✅ Knowledge Base Updated!")
        st.rerun()

    st.sidebar.markdown("---")

    pdf_count = len(list(Path("data/pdfs").glob("*.pdf")))
    chunk_count = vector_store.index.ntotal

    st.sidebar.metric("📄 Documents", pdf_count)
    st.sidebar.metric("🧩 Chunks", chunk_count)

    st.sidebar.write("**LLM:** Gemini 2.5 Flash")
    st.sidebar.write("**Embedding:** all-MiniLM-L6-v2")
    st.sidebar.write("**Vector DB:** FAISS")

    st.sidebar.markdown("---")

    if st.sidebar.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()