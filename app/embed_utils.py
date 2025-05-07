import os
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st
import numpy as np
from app.config import OPENAI_API_KEY
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema.document import Document


embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)


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


def build_chroma_index(chunks, persist_dir="chroma_db"):
    #embeddings = OpenAIEmbeddings()
    docs = [Document(page_content=chunk) for chunk in chunks]
    vectorstore = Chroma.from_documents(docs, embedding=embeddings, persist_directory=persist_dir)
    vectorstore.persist()
    print(f"Chroma index persisted at: {persist_dir}")

def search_chroma_index(query, persist_dir="chroma_db", top_k=3):
    #embeddings = OpenAIEmbeddings()
    vectorstore = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})
    docs = retriever.get_relevant_documents(query)
    return [doc.page_content for doc in docs]

