# Imports

from pathlib import Path
import re
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from config import (
    PDF_DIR,
    VECTORSTORE_DIR,
    EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)

# Function 1
def load_documents():
    loader = PyPDFDirectoryLoader(PDF_DIR)
    documents = loader.load()

    print(f"Loaded {len(documents)} document pages.")

    return documents



def split_documents(documents):
    """
    Split documents into smaller overlapping chunks.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = text_splitter.split_documents(documents)
    for chunk in chunks:
        chunk.page_content = clean_text(chunk.page_content)

    print(f"Created {len(chunks)} chunks.\n")

    return chunks

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_huggingface import HuggingFaceEmbeddings

def create_embeddings():
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    return embeddings

 
def create_vector_store(chunks, embeddings):
    print(f"Creating FAISS index from {len(chunks)} chunks...")

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    return vector_store

def save_vector_store(vector_store):
    """
    Save FAISS index locally.
    """

    vector_store.save_local(VECTORSTORE_DIR)

    print("\nVector Store saved successfully!")

def clean_text(text: str) -> str:
    """
    Clean extracted PDF text before embedding.
    """

    # Remove null bytes
    text = text.replace("\x00", "")

    # Remove invalid Unicode surrogates
    text = text.encode("utf-8", "ignore").decode("utf-8")

    # Collapse excessive whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()

def build_knowledge_base():

    documents = load_documents()

    chunks = split_documents(documents)

    embeddings = create_embeddings()

    vector_store = create_vector_store(
        chunks,
        embeddings
    )

    save_vector_store(vector_store)
    
if __name__ == "__main__":
    documents = load_documents()

    chunks = split_documents(documents)

    embeddings = create_embeddings()

    vector_store = create_vector_store(
        chunks,
        embeddings
    )

    save_vector_store(vector_store)

    print("\n✅ Ingestion completed successfully!")