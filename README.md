📌 SHL Assessment Recommendation System
🧠 Overview

This project is a Retrieval-Augmented Generation (RAG) system that recommends relevant SHL assessments based on user queries. It combines FAISS-based semantic search with Gemini 2.5 Flash to generate accurate, context-aware recommendations.

🏗️ System Architecture
Frontend / API Layer: FastAPI / Streamlit
Retrieval System: FAISS vector database with SentenceTransformers embeddings
Embedding Model: all-MiniLM-L6-v2
Generation Model: Gemini 2.5 Flash
Approach: Retrieval-Augmented Generation (RAG)                                                                                                                                                                                                                                                      

🔎 Retrieval Design We use a FAISS vector store to perform semantic search over SHL assessment data.

Embeddings generated using SentenceTransformers
Efficient similarity search using FAISS
Top-K retrieval ensures most relevant assessments are fetched
Each result includes metadata:
Assessment name
Type
URL
Description
🧾 Prompt Design

The prompt is structured to ensure grounded and reliable responses:

System instructions define behavior
Retrieved FAISS context is injected
Chat history is included
Model is restricted to SHL catalog only

This ensures no hallucinated assessments.
