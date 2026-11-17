from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

# Free local embeddings — no API key required, no PyTorch needed
# Downloads the model once (~60MB), then runs fully offline
embeddings = FastEmbedEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

if __name__ == "__main__":

    text = "The passing grade is 50."

    vector = embeddings.embed_query(text)

    print(f"Embedding Length: {len(vector)}")

    print("\nFirst 10 Values:")

    print(vector[:10])