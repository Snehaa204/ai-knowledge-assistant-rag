from pathlib import Path

# ===========================
# Project Paths
# ===========================

BASE_DIR = Path(__file__).resolve().parent

PDF_DIR = BASE_DIR / "data" / "pdfs"

VECTORSTORE_DIR = BASE_DIR / "vectorstore"

# ===========================
# Embedding Model
# ===========================

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ===========================
# Chunking Configuration
# ===========================

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200

# ===========================
# Retrieval Configuration
# ===========================

TOP_K = 4