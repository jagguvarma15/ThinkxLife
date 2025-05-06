import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.embed_utils import load_context_chunks, build_chroma_index

# Load chunks from text file
chunks = load_context_chunks("/Users/varma/Desktop/Thinkx/ThinkxLife/data/context.txt")

# Build Chroma DB
build_chroma_index(chunks, persist_dir="chroma_db")

print("Chroma index built successfully at chroma_db/")

