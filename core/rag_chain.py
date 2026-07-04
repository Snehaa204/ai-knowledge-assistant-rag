import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_core import chat_history
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from torchgen import context

from prompts import RAG_SYSTEM_PROMPT
from config import VECTORSTORE_DIR, EMBEDDING_MODEL

load_dotenv(dotenv_path=Path(".env"))

print("API Key:", os.getenv("GOOGLE_API_KEY"))

def load_embeddings():
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    return embeddings

def load_vector_store():
    """
    Load the saved FAISS vector database.
    """

    embeddings = load_embeddings()

    vector_store = FAISS.load_local(
        folder_path=VECTORSTORE_DIR,
        embeddings=embeddings,
        allow_dangerous_deserialization=True,
    )

    return vector_store

def retrieve_documents(query: str, k: int = 3):
    """
    Retrieve the top-k most relevant chunks for a query.
    """

    vector_store = load_vector_store()

    results = vector_store.similarity_search(
        query=query,
        k=k
    )

    return results

print("API Key Loaded:", os.getenv("GOOGLE_API_KEY") is not None)
print("First 10 chars:", os.getenv("GOOGLE_API_KEY")[:10])

def load_llm():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    return llm
def ask_question(
    question,
    vector_store,
    chat_history
):
    history = ""

    for message in chat_history:

        history += f"{message['role']}: {message['content']}\n"

    retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 3,
        "fetch_k": 8,
    },
)

    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    prompt = RAG_SYSTEM_PROMPT.format(
        context=context,
        history=history,
        question=question
)

    llm = load_llm()

    response = llm.invoke(prompt)

    return response.content, docs


if __name__ == "__main__":

    question = input("Ask a question: ")

    answer = ask_question(question)

    print("\n")
    print("=" * 70)
    print(answer)