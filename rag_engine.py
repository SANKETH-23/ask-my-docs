# ── SQLite Fix For Streamlit Cloud ───────────────
__import__("pysqlite3")
import sys
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

# ── Imports ─────────────────────────────────────
import os

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
from groq import Groq
from dotenv import load_dotenv

# ── Load Environment Variables ──────────────────
load_dotenv()

# ── Validate API Key ────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing."
    )

# ── Embedding Model ─────────────────────────────
embedder = SentenceTransformer(
    "all-MiniLM-L6-v2",
    device="cpu"
)

# ── Groq Client ─────────────────────────────────
groq_client = Groq(
    api_key=GROQ_API_KEY
)

# ── ChromaDB Client ─────────────────────────────
chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

# ── Load PDFs ───────────────────────────────────
def load_pdfs(pdf_folder="pdfs"):

    documents = []

    if not os.path.exists(pdf_folder):
        raise FileNotFoundError(
            f"Folder '{pdf_folder}' not found."
        )

    for filename in os.listdir(pdf_folder):

        if filename.endswith(".pdf"):

            filepath = os.path.join(
                pdf_folder,
                filename
            )

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

# ── Split Into Chunks ───────────────────────────
def split_into_chunks(
    documents,
    chunk_size=800,
    overlap=100
):

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

# ── Build Vector Store ──────────────────────────
def build_vector_store(chunks):

    collection = chroma_client.get_or_create_collection(
        name="docs"
    )

    # Prevent duplicate inserts
    if collection.count() == 0:

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        embeddings = embedder.encode(
            texts
        ).tolist()

        ids = [
            str(i)
            for i in range(len(chunks))
        ]

        metadatas = [
            {
                "source": chunk["source"],
                "page": chunk["page"]
            }
            for chunk in chunks
        ]

        collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )

    return collection

# ── Search Relevant Chunks ──────────────────────
def search_chunks(
    query,
    collection,
    top_k=4
):

    query_embedding = embedder.encode(
        [query]
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    retrieved_chunks = []

    for i, doc in enumerate(results["documents"][0]):

        metadata = results["metadatas"][0][i]

        retrieved_chunks.append({
            "text": doc,
            "source": metadata["source"],
            "page": metadata["page"]
        })

    return retrieved_chunks

# ── Ask Groq ────────────────────────────────────
def ask_groq(
    query,
    relevant_chunks
):

    context = "\n\n".join([
        f"[Source: {chunk['source']} | "
        f"Page {chunk['page']}]\n"
        f"{chunk['text']}"
        for chunk in relevant_chunks
    ])

    prompt = f"""
You are a helpful assistant.

Answer ONLY from the provided context.

If the answer is not found,
say:
"I don't know based on these documents."

Context:
{context}

Question:
{query}

Answer:
"""

    try:

        response = groq_client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Groq API Error: {str(e)}"

# ── Run Full Pipeline ───────────────────────────
def run_pipeline():

    print("📄 Loading PDFs...")
    documents = load_pdfs()

    print(f"✅ Loaded {len(documents)} pages")

    print("✂️ Splitting into chunks...")
    chunks = split_into_chunks(documents)

    print(f"✅ Created {len(chunks)} chunks")

    print("🔢 Building vector store...")
    collection = build_vector_store(chunks)

    print("✅ Vector store ready!")

    return collection, chunks