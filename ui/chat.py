
import streamlit as st

from core.rag_chain import ask_question


def render_chat(vector_store):

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    question = st.chat_input("Ask anything about your uploaded documents...")

    if not question:
        return

    # User message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Assistant response
    with st.chat_message("assistant"):

        status = st.status(
            "🧠 Processing your request...",
            expanded=True,
        )

        status.write("🔍 Searching relevant document chunks...")

        answer, docs = ask_question(
            question,
            vector_store,
            st.session_state.messages,
        )

        status.write("📚 Retrieved relevant context")
        status.write("🤖 Generating response with Gemini")

        status.update(
            label="✅ Response Ready",
            state="complete",
        )

        st.markdown(answer)

        st.divider()

        st.markdown("### 📚 Sources")

        for doc in docs:

            source = doc.metadata.get("source", "Unknown")
            filename = source.split("/")[-1]
            page = doc.metadata.get("page", 0)

            with st.expander(f"📄 {filename} (Page {page + 1})"):
                st.write(doc.page_content)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )