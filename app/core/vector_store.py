import os
import pickle
import faiss
import numpy as np
from threading import Lock

from sentence_transformers import SentenceTransformer
from langchain.schema import Document

from app.retrieval.hybrid import build_bm25_index


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

INDEX_PATH = os.path.join(DATA_DIR, "faiss_index.bin")
DOC_PATH = os.path.join(DATA_DIR, "documents.pkl")

os.makedirs(DATA_DIR, exist_ok=True)

lock = Lock()

print("Loading embedding model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
print("Embedding model loaded")


# LOAD DOCUMENTS
if os.path.exists(DOC_PATH):

    try:
        with open(DOC_PATH, "rb") as f:
            documents = pickle.load(f)

    except:
        documents = []

else:
    documents = []


# LOAD INDEX
if os.path.exists(INDEX_PATH):

    try:
        index = faiss.read_index(INDEX_PATH)

    except:
        index = faiss.IndexFlatL2(384)

else:
    index = faiss.IndexFlatL2(384)


bm25_index = build_bm25_index(documents)


def add_documents(chunks):

    global documents, index, bm25_index

    if not chunks:
        return 0

    with lock:

        texts = [chunk.page_content for chunk in chunks]

        embeddings = embedding_model.encode(texts)

        embeddings = np.array(embeddings).astype("float32")

        index.add(embeddings)

        for chunk in chunks:

            documents.append(
                Document(
                    page_content=chunk.page_content,
                    metadata=chunk.metadata
                )
            )

        bm25_index = build_bm25_index(documents)

        faiss.write_index(index, INDEX_PATH)

        with open(DOC_PATH, "wb") as f:
            pickle.dump(documents, f)

    return len(chunks)


def get_index():
    return index


def get_documents():
    return documents


def get_bm25():
    return bm25_index


def get_embedding_model():
    return embedding_model