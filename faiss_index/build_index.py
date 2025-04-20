import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.embed_utils import load_context_chunks, embed_text_openai, build_faiss_index

# Load chunks from relative path
chunks = load_context_chunks("/Users/varma/Desktop/Thinkx/ThinkxLife/data/context.txt")
embeddings = embed_text_openai(chunks)
build_faiss_index(chunks, embeddings, save_path="/Users/varma/Desktop/Thinkx/ThinkxLife/faiss_index/index.pkl")

print("FAISS index built successfully at faiss_index/index.pkl")
