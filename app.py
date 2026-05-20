import streamlit as st
from rag_engine import run_pipeline, search_chunks, ask_groq

# ── Page Config ──────────────────────────────────
st.set_page_config(
    page_title="Ask My Docs",
    page_icon="📄",
    layout="centered"
)

# ── Header ───────────────────────────────────────
st.title("📄 Ask My Docs")
st.markdown("Upload PDFs and ask questions — get answers with sources!")
st.divider()

# ── Load & Index PDFs ────────────────────────────
@st.cache_resource(show_spinner="🔄 Loading and indexing PDFs...")
def load_data():
    collection, chunks = run_pipeline()
    return collection, chunks

collection, chunks = load_data()

st.success("✅ PDFs loaded and indexed successfully!")

# ── Question Input ───────────────────────────────
st.subheader("💬 Ask a Question")

query = st.text_input(
    "Type your question here",
    placeholder="e.g. What is the main topic of the document?"
)

# ── Answer Section ───────────────────────────────
if query:

    with st.spinner("🤔 Thinking..."):

        relevant_chunks = search_chunks(
            query,
            collection,
            chunks,
            top_k=4
        )

        answer = ask_groq(query, relevant_chunks)

    st.subheader("🤖 Answer")
    st.write(answer)

    st.divider()

    with st.expander("📚 View Source Chunks Used"):

        for i, chunk in enumerate(relevant_chunks):

            st.markdown(
                f"**Source {i+1}: "
                f"{chunk['source']} "
                f"— Page {chunk['page']}**"
            )

            st.caption(chunk["text"][:400] + "...")
            st.divider()