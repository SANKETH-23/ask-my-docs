# 📄 Ask My Docs — AI-Powered PDF Q&A App

## Candidate Details

- **Name:** Sanketh S
- **Email:** sanki23sanketh@gmail.com
- **Phone:** +91-9019074504
- **Role Applied For:** AI Developer Internship — Terrainfra360

---

# 🚀 Project Overview

Ask My Docs is a Retrieval-Augmented Generation (RAG) based PDF Question Answering application built using Streamlit.

The application allows users to interact with PDF documents using natural language queries. It retrieves the most relevant content from uploaded PDFs using semantic search and generates grounded responses using a Large Language Model (LLM).

The system combines:
- PDF ingestion
- text chunking
- embeddings
- vector similarity search
- conversational memory
- prompt-augmented answer generation

to provide context-aware answers with source citations.

---

# ✨ Features

## Core Features

- PDF ingestion from local folder
- Text chunking with overlap
- Semantic embeddings using Sentence Transformers
- ChromaDB vector database
- Top-k semantic retrieval
- Question answering using Groq LLM
- Streamlit web interface
- Source chunk display with filename
- Page number citations

---

## Bonus Features Implemented

- ✅ Multi-turn conversation memory
- ✅ Persistent embedding cache to disk
- ✅ Hallucination control prompt
- ✅ Page number source citations
- ✅ Cached vector database for faster startup

---

# 🧠 System Architecture

```text
PDF Documents
      ↓
Text Extraction
      ↓
Chunking
      ↓
Embeddings Generation
      ↓
ChromaDB Vector Store
      ↓
Similarity Search
      ↓
Relevant Context Retrieval
      ↓
Prompt Construction
      ↓
Groq LLM Response
```

---

# 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.10 | Core programming language |
| Streamlit | Web application UI |
| Sentence Transformers | Embedding generation |
| all-MiniLM-L6-v2 | Embedding model |
| ChromaDB | Vector database |
| Groq API | LLM inference |
| PyPDF | PDF text extraction |
| python-dotenv | Environment management |
| NumPy | Numerical operations |

---

# ⚙️ Installation & Setup

## 1. Clone Repository

```bash
git clone https://github.com/SANKETH-23/ask-my-docs.git
cd ask-my-docs
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the root directory.

```env
GROQ_API_KEY=your_groq_api_key_here
```

You can obtain a free API key from:

https://console.groq.com

---

## 5. Add PDF Files

Place at least 3 PDF files inside:

```text
/pdfs
```

---

## 6. Run the Application

```bash
streamlit run app.py
```

The application will start at:

```text
http://localhost:8501
```

---

# 🔑 Environment Variables

| Variable | Description |
|---|---|
| GROQ_API_KEY | Groq API key for LLM inference |

See `.env.example` for reference.

---

# 📂 Project Structure

```text
ask-my-docs/
│
├── .streamlit/
│   └── secrets.toml
│
├── pdfs/
├── chroma_db/
│
├── app.py
├── rag_engine.py
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

---

# ✅ Feature Completion Checklist

## Completed

- [x] PDF ingestion
- [x] Text chunking
- [x] Embeddings generation
- [x] ChromaDB vector storage
- [x] Semantic similarity retrieval
- [x] Groq LLM integration
- [x] Streamlit UI
- [x] Source chunk citations
- [x] Page number references
- [x] Multi-turn memory
- [x] Embedding cache to disk
- [x] Deployment on Streamlit Cloud

---

## Partially Completed

- [ ] Advanced OCR support for scanned PDFs

---

## Not Implemented

- [ ] Authentication
- [ ] Multi-user document isolation

---

# 💬 Sample Q&A Pairs

## Q1

### Question
What is the main topic of this document?

### Answer
The document primarily discusses statistics, including data collection, summarization, analysis, and interpretation.

---

## Q2

### Question
Summarize the key points mentioned.

### Answer
The document explains the importance of statistics in business, government, and research. It discusses descriptive statistics, data interpretation, and statistical reasoning.

---

## Q3

### Question
What important terms are explained?

### Answer
The document explains terms such as qualitative data, quantitative data, descriptive statistics, averages, correlations, and data analysis.

---

## Q4

### Question
What conclusions are discussed?

### Answer
The document explains that statistical conclusions can be highly reliable when used correctly, but misleading interpretations may distort results.

---

## Q5

### Question
Are there any important numbers or figures mentioned?

### Answer
The retrieved context referenced several page numbers and examples, though no major numerical dataset was explicitly discussed.

---

# ❗ Known Limitations

- Works best with text-based PDFs
- OCR is not supported for scanned PDFs
- Large PDFs increase embedding generation time
- Free-tier Groq API may have rate limits

---

# 🌐 Deployment

## GitHub Repository

https://github.com/SANKETH-23/ask-my-docs

---

## Live Streamlit Application

https://sanketh-ask-my-docs.streamlit.app/

---

# 🎥 Demo Recording

https://youtu.be/BtnWLJ3OKeU?si=3LKbgwARrnzEHdUw

---

# 🔮 Future Improvements

- OCR support for scanned PDFs
- Hybrid keyword + vector retrieval
- Streaming responses
- User-uploaded PDFs from UI
- Better reranking models
- Docker deployment support

---

# 🧩 Design Decisions

## Why Chunking?

LLMs have token limits. Chunking divides large PDFs into manageable sections for retrieval.

---

## Why Embeddings?

Embeddings convert text into vectors that preserve semantic meaning, enabling similarity search.

---

## Why ChromaDB?

ChromaDB provides a lightweight local vector database suitable for free-tier deployment.

---

## Why Retrieval-Augmented Generation (RAG)?

RAG reduces hallucination by grounding LLM responses using retrieved document context.

---

## Why Conversation Memory?

Memory improves multi-turn conversational flow and allows follow-up questions with context continuity.