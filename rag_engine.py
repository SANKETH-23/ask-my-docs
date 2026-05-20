import os
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

embedder = SentenceTransformer("all-MiniLM-L6-v2")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
chroma_client = chromadb.Client()


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


def build_vector_store(chunks):
    collection = chroma_client.get_or_create_collection("docs")
    texts = [c["text"] for c in chunks]
    embeddings = embedder.encode(texts).tolist()
    ids = [str(i) for i in range(len(chunks))]
    metadatas = [{"source": c["source"], "page": c["page"]} 
                 for c in chunks]
    collection.add(
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas,
        ids=ids
    )
    return collection, chunks


def search_chunks(query, collection, chunks, top_k=4):
    query_embedding = embedder.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )
    retrieved = []
    for i, doc in enumerate(results["documents"][0]):
        meta = results["metadatas"][0][i]
        retrieved.append({
            "text": doc,
            "source": meta["source"],
            "page": meta["page"]
        })
    return retrieved


def ask_groq(query, relevant_chunks):
    context = "\n\n".join([
        f"[Source: {c['source']} | Page {c['page']}]\n{c['text']}"
        for c in relevant_chunks
    ])
    prompt = f"""You are a helpful assistant. Answer the question 
based ONLY on the context below.
If the answer is not found in the context, say 
"I don't know based on these documents."

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


def run_pipeline():
    print("📄 Loading PDFs...")
    documents = load_pdfs()
    print(f"✅ Loaded {len(documents)} pages")

    print("✂️  Splitting into chunks...")
    chunks = split_into_chunks(documents)
    print(f"✅ Created {len(chunks)} chunks")

    print("🔢 Building vector store...")
    collection, chunks = build_vector_store(chunks)
    print("✅ Vector store ready!")

    return collection, chunks