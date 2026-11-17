from langchain_community.vectorstores import FAISS

from utils.text_splitter import split_documents
from utils.embeddings import embeddings


def create_vector_store():

    print("Creating document chunks...")

    chunks = split_documents()

    print(f"Total chunks: {len(chunks)}")


    print("Creating FAISS index...")

    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )


    vector_store.save_local(
        "vectorstore/faiss_index"
    )


    print("[OK] FAISS index created successfully")


if __name__ == "__main__":

    create_vector_store()