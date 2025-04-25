import os
import pickle
import faiss
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

load_dotenv()
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def load_context_chunks(filepath, chunk_size=300):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def embed_text_openai(chunks):
    embeddings = []
    for chunk in chunks:
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=chunk
        )
        embeddings.append(response.data[0].embedding)
    return embeddings

def build_faiss_index(chunks, embeddings, save_path="faiss_index/index.pkl"):
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))
    with open(save_path, "wb") as f:
        pickle.dump((index, chunks), f)

def search_faiss_index(query, save_path="faiss_index/index.pkl", top_k=3):
    if not os.path.exists(save_path):
        return ["(No knowledge base available yet. Please build and upload FAISS index.)"]

    try:
        with open(save_path, "rb") as f:
            index, chunks = pickle.load(f)
    except Exception as e:
        print(f"Failed to load FAISS index from {save_path}: {e}")
        return ["(Knowledge base error.)"]

    try:
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=query
        )
        query_vec = np.array(response.data[0].embedding, dtype=np.float32).reshape(1, -1)
    except Exception as e:
        print("Embedding generation error:", e)
        return ["(Failed to process your question.)"]

    try:
        if query_vec.shape[1] != index.d:
            print(f"Dimension mismatch: query_vec {query_vec.shape[1]} vs index {index.d}")
            return ["(Knowledge base dimension mismatch.)"]

        D, I = index.search(query_vec, top_k)
        return [chunks[i] for i in I[0]]
    except Exception as e:
        print("FAISS search error:", e)
        return ["(Failed to find related info.)"]
