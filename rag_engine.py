import os
try:
    import faiss
except ImportError:
    import subprocess
    subprocess.run(["pip", "install", "faiss-cpu"])
    import faiss
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ── 1. Read all PDFs from /pdfs folder ──────────────────────────
def load_pdfs(pdf_folder="pdfs"):
    documents = []
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            filepath = os.path.join(pdf_folder, filename)
            reader = PdfReader(filepath)
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if text and text.strip():
                    documents.append({
                        "text": text,
                        "source": filename,
                        "page": page_num + 1
                    })
    return documents


# ── 2. Split text into chunks ────────────────────────────────────
def split_into_chunks(documents, chunk_size=800, overlap=100):
    chunks = []
    for doc in documents:
        text = doc["text"]
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            if chunk.strip():
                chunks.append({
                    "text": chunk,
                    "source": doc["source"],
                    "page": doc["page"]
                })
            start += chunk_size - overlap
    return chunks


# ── 3. Build FAISS vector store ──────────────────────────────────
def build_vector_store(chunks):
    texts = [c["text"] for c in chunks]
    embeddings = embedder.encode(texts, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index, embeddings, chunks


# ── 4. Search top relevant chunks ───────────────────────────────
def search_chunks(query, index, chunks, top_k=4):
    query_embedding = embedder.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, top_k)
    results = []
    for i in indices[0]:
        if i < len(chunks):
            results.append(chunks[i])
    return results


# ── 5. Ask LLM with retrieved chunks ────────────────────────────
def ask_groq(query, relevant_chunks):
    context = "\n\n".join([
        f"[Source: {c['source']} | Page {c['page']}]\n{c['text']}"
        for c in relevant_chunks
    ])

    prompt = f"""You are a helpful assistant. Answer the question based ONLY on the context below.
If the answer is not found in the context, say "I don't know based on these documents."

Context:
{context}

Question: {query}

Answer:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content


# ── 6. Main pipeline function ────────────────────────────────────
def run_pipeline():
    print("📄 Loading PDFs...")
    documents = load_pdfs()
    print(f"✅ Loaded {len(documents)} pages")

    print("✂️  Splitting into chunks...")
    chunks = split_into_chunks(documents)
    print(f"✅ Created {len(chunks)} chunks")

    print("🔢 Building vector store...")
    index, embeddings, chunks = build_vector_store(chunks)
    print("✅ Vector store ready!")

    return index, chunks