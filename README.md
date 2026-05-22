# 📄 Ask My Docs — AI-Powered PDF Q&A App

## Candidate Details
- **Name:** Sanketh S
- **Email:** sanki23sanketh@gmail.com
- **Phone:** 9019074504
- **Role Applied For:** AI Developer Internship — Terrainfra360

---

## 📌 Project Overview
Ask My Docs is a Retrieval-Augmented Generation (RAG) web application
built with Streamlit. Users can upload PDF documents and ask questions
in natural language. The app retrieves the most relevant chunks from
the PDFs and generates accurate answers using a free LLM API (Groq),
along with the source file and page number.

---

## 🛠️ Technology Stack
- **Python** 3.10+
- **Streamlit** — Web UI
- **sentence-transformers** (all-MiniLM-L6-v2) — Local embeddings
- **FAISS** — Vector store for similarity search
- **Groq API** (llama-3.3-70b-versatile) — Free LLM for answer generation
- **pypdf** — PDF text extraction
- **LangChain** — Text splitting utilities
- **python-dotenv** — Environment variable management

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/SANKETH-23/ask-my-docs.git
cd ask-my-docs
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install Dependencies
```bash
pip install streamlit pypdf sentence-transformers faiss-cpu langchain langchain-community groq python-dotenv
```

### 4. Configure API Key
- Copy `.env.example` to `.env`
- Get free API key from https://console.groq.com
- Add your key to `.env`:

GROQ_API_KEY=your_actual_key_here

### 5. Add PDF Files
- Place at least 3 PDF files inside the `/pdfs` folder

### 6. Run the App
```bash
streamlit run app.py
```
- App opens at: http://localhost:8501

---

## 🔑 Environment Variables
| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Free API key from console.groq.com |

See `.env.example` for reference.

---

## ✅ Features Checklist

### Completed ✅
- [x] PDF ingestion from local /pdfs folder
- [x] Text chunking (800 chars with 100 char overlap)
- [x] Sentence-transformer embeddings (all-MiniLM-L6-v2)
- [x] FAISS vector store
- [x] Top 4 relevant chunks retrieval
- [x] Groq LLM answer generation
- [x] Source filename + page number display
- [x] Expandable source chunks in UI
- [x] "I don't know" response when context is insufficient
- [x] Streamlit single-page UI

### Partially Completed ⏳
- [ ] Deployment on Streamlit Cloud (in progress)

### Not Implemented ❌
- [ ] Multi-turn conversation memory
- [ ] Embedding cache to disk

---

## 🎁 Bonus Features Attempted
- ✅ Page number shown in source citations
- ✅ Prompt instructs LLM to say "I don't know based on these documents"
  when context is insufficient

---

## ❗ Known Issues & Assumptions
- App works best with text-based PDFs (not scanned images)
- All PDFs must be placed in /pdfs folder before starting the app
- Groq free tier has rate limits on heavy usage

---

## 💬 5 Sample Q&A Pairs

**Q1: What is the main topic of this document?**
> Based on the context, the main topic of this document appears to be
> statistics, specifically the collection, analysis, and use of
> statistical data in various fields such as government planning,
> business operations, and research.

**Q2: Summarise the key points mentioned**
> The key points include: Statistics involves three critical tasks —
> collecting, summarizing, and analyzing data. Understanding data is
> essential for personal and professional decisions. Descriptive
> statistics summarizes raw observations using statistical values and
> graphical methods.

**Q3: What are the important terms explained?**
> Important terms include: Qualitative information (e.g. good, bad,
> beautiful), Quantitative information (e.g. income, expenditure,
> savings), Nature of Data, Statistics, and Statistical methods
> such as averages and correlations.

**Q4: What conclusions are mentioned?**
> Statistical conclusions are mentioned as being reliable and accurate
> by statisticians, but also potentially misleading if not properly
> contextualized. Some believe statistics can distort truth, leading
> to distrust in its findings.

**Q5: Any specific data or numbers mentioned?**
> There are no specific data or numbers mentioned in the context,
> except for some page numbers: Page 9, Page 7, Page 14, and Page 20.

---

## 🎥 Demo Recording
[Link will be added after recording]

## 🌐 Live Deployed URL
[https://sanketh-ask-my-docs.streamlit.app/]