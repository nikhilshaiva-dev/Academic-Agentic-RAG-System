from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils.policy_loader import load_policies


def split_documents():

    policies = load_policies()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = []

    for filename, text in policies.items():

        docs = splitter.create_documents(
            [text],
            metadatas=[{"source": filename}]
        )

        chunks.extend(docs)

    return chunks


if __name__ == "__main__":

    chunks = split_documents()

    print(f"\nTotal Chunks: {len(chunks)}\n")

    for i, chunk in enumerate(chunks[:5], start=1):
        print("=" * 60)
        print(f"Chunk {i}")
        print("Source:", chunk.metadata["source"])
        print(chunk.page_content[:300])