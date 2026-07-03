from dotenv import load_dotenv
load_dotenv()

import os

from google import genai
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from prompts import SYSTEM_PROMPT
from utils import latest_user_message, build_recommendations


VECTOR_DB = "vectorstore"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    VECTOR_DB,
    embeddings,
    allow_dangerous_deserialization=True
)

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def search_catalog(query, k=10):
    return db.similarity_search(query, k=k)


def build_context(docs):
    context = ""
    for doc in docs:
        context += f"""
Assessment: {doc.metadata.get('name')}
URL: {doc.metadata.get('url')}
Category: {doc.metadata.get('type')}

{doc.page_content}

----------------------------------
"""
    return context


# ✅ SMARTER CLARIFICATION LOGIC
def is_really_vague(query: str) -> bool:
    query = query.lower().strip()
    words = query.split()

    vague_keywords = ["assessment", "test", "job", "role", "interview"]

    return len(words) <= 2 or query in vague_keywords


def chat(messages):

    query = latest_user_message(messages)

    # 1. smarter clarification
    if is_really_vague(query):
        return {
            "reply": (
                "Could you tell me the job role, seniority level, "
                "and whether you need technical, cognitive, personality, "
                "or behavioral assessments?"
            ),
            "recommendations": [],
            "retrieved": [],
            "end_of_conversation": False,
        }

    # 2. retrieve docs
    docs = search_catalog(query)
    context = build_context(docs)

    conversation = "\n".join(
        f"{m['role']}: {m['content']}" for m in messages
    )

    prompt = f"""
{SYSTEM_PROMPT}

Conversation:
{conversation}

Retrieved SHL Catalog:
{context}

Answer ONLY using the retrieved catalog.
"""

    # 3. Gemini call
    response = client.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    # 4. return + retrieval visibility
    return {
        "reply": response.text,
        "recommendations": build_recommendations(docs),
        "retrieved": [
            {
                "name": d.metadata.get("name"),
                "type": d.metadata.get("type"),
                "url": d.metadata.get("url"),
            }
            for d in docs
        ],
        "end_of_conversation": False,
    }