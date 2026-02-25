import tempfile
import os

from fastapi import UploadFile

from langchain_community.document_loaders import (
    PyPDFLoader,
    CSVLoader,
    WebBaseLoader
)

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.vector_store import add_documents


# FILE INGESTION

def ingest_file(upload_file: UploadFile):

    suffix = os.path.splitext(upload_file.filename)[1].lower()

    if suffix not in [".pdf", ".csv"]:
        raise Exception("Only PDF and CSV supported")

    tmp_path = None

    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as tmp:

            content = upload_file.file.read()
            tmp.write(content)
            tmp_path = tmp.name


        # select loader
        if suffix == ".pdf":
            loader = PyPDFLoader(tmp_path)

        elif suffix == ".csv":
            loader = CSVLoader(tmp_path)


        docs = loader.load()

        # attach metadata
        for d in docs:
            d.metadata["source"] = upload_file.filename


        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        chunks = splitter.split_documents(docs)

        count = add_documents(chunks)

        return count

    finally:

        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)



# URL INGESTION

def ingest_url(url: str):

    loader = WebBaseLoader(url)

    docs = loader.load()

    for d in docs:
        d.metadata["source"] = url


    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(docs)

    return add_documents(chunks)