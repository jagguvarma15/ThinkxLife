import os
import json
import pandas as pd
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from app.config import OPENAI_API_KEY

# Initialize embedding model
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

def load_context_txt(path, chunk_size=300):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    return [Document(page_content=chunk, metadata={"source": "context.txt"}) for chunk in chunks]

def load_knowledge_json(path, chunk_size=300):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    docs = []
    for item in data:
        question = item.get("question", "")
        answer = item.get("answer", "")
        category = item.get("category", "general")
        for i in range(0, len(answer), chunk_size):
            chunk = answer[i:i+chunk_size]
            docs.append(Document(
                page_content=f"{question}\n{chunk}",
                metadata={"source": "knowledge_base", "category": category}
            ))
    return docs

def load_empathy_docs(csv_path="data/empathetic_dialogues_train.csv", max_examples=500):
    df = pd.read_csv(csv_path)
    docs = []

    for _, row in df.head(max_examples).iterrows():
        situation = row['Situation']
        emotion = row['emotion']
        dialogue = row['empathetic_dialogues']
        response = row['labels']

        text = (
            f"Emotion: {emotion}\n"
            f"Situation: {situation}\n"
            f"Dialogue: {dialogue.strip()}\n"
            f"Agent Response: {response.strip()}"
        )

        docs.append(Document(
            page_content=text,
            metadata={"source": "empathetic_dialogues", "emotion": emotion}
        ))

    return docs

if __name__ == "__main__":
    context_docs = load_context_txt("data/context.txt")
    kb_docs = load_knowledge_json("data/knowledge_base.json")
    empathy_docs = load_empathy_docs("data/empathetic_dialogues_train.csv")

    all_docs = context_docs + kb_docs + empathy_docs

    vectorstore = Chroma.from_documents(
        all_docs,
        embedding=embeddings,
        persist_directory="chroma_db"
    )
    vectorstore.persist()

    print(f"Chroma DB built successfully with {len(all_docs)} documents.")
