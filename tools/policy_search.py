import os
from langchain_community.vectorstores import FAISS
from utils.embeddings import embeddings
from config import VECTOR_DB_DIR


def load_vector_store():
    index_path = os.path.join(VECTOR_DB_DIR, "faiss_index")
    vector_store = FAISS.load_local(
        index_path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store


def search_policy(query, k=3):

    vector_store = load_vector_store()

    results = vector_store.similarity_search(
        query,
        k=k
    )

    return results


if __name__ == "__main__":

    query = "What is the minimum attendance requirement?"

    docs = search_policy(query)

    for i, doc in enumerate(docs, start=1):

        print("\nResult", i)

        print("Source:",
              doc.metadata["source"])

        print(doc.page_content)
