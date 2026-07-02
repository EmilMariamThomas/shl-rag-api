import json

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer


CATALOG_FILE = "catalog.json"
VECTOR_DB = "vectorstore"


class LocalEmbeddings(Embeddings):
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_documents(self, texts):
        return self.model.encode(texts, convert_to_numpy=True).tolist()

    def embed_query(self, text):
        return self.model.encode(text, convert_to_numpy=True).tolist()


def clean_text(text):
    if text is None:
        return ""
    return " ".join(str(text).replace("\n", " ").split())


def load_catalog():
    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    documents = []

    for item in catalog:

        content = f"""
Name: {clean_text(item.get("name"))}

Description:
{clean_text(item.get("description"))}

Job Levels:
{", ".join(item.get("job_levels", []))}

Categories:
{", ".join(item.get("keys", []))}

Duration:
{clean_text(item.get("duration"))}

Remote:
{item.get("remote")}

Adaptive:
{item.get("adaptive")}
"""

        metadata = {
            "name": item.get("name", ""),
            "url": item.get("link", ""),
            "type": ", ".join(item.get("keys", []))
        }

        documents.append(
            Document(
                page_content=content,
                metadata=metadata
            )
        )

    return documents


def create_vectorstore():

    documents = load_catalog()

    print(f"Loaded {len(documents)} assessments...")

    embeddings = LocalEmbeddings()

    vector_db = FAISS.from_documents(
        documents,
        embeddings
    )

    vector_db.save_local(VECTOR_DB)

    print("✅ Vector database created successfully!")


if __name__ == "__main__":
    create_vectorstore()