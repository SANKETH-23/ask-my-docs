import streamlit as st

from rag_engine import (
    run_pipeline,
    search_chunks,
    ask_groq
)

# ── Page Config ─────────────────────────────────
st.set_page_config(
    page_title="Ask My Docs",
    page_icon="📄",
    layout="centered"
)

# ── Session Memory ──────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ── Header ──────────────────────────────────────
st.title("📄 Ask My Docs")

st.markdown(
    "Chat with your PDFs using AI + Memory"
)

st.divider()

# ── Load Vector Store ───────────────────────────
@st.cache_resource(
    show_spinner="🔄 Loading PDFs..."
)
def load_data():

    collection, chunks = run_pipeline()

    return collection, chunks

collection, chunks = load_data()

st.success(
    "✅ PDFs loaded successfully!"
)

# ── User Input ──────────────────────────────────
query = st.chat_input(
    "Ask something about your PDFs..."
)

# ── Display Chat History ────────────────────────
for message in st.session_state.chat_history:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ── Process Query ───────────────────────────────
if query:

    # Show user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": query
    })

    with st.chat_message("user"):
        st.markdown(query)

    with st.spinner("🤔 Thinking..."):

        relevant_chunks = search_chunks(
            query=query,
            collection=collection,
            top_k=4
        )

        answer = ask_groq(
            query=query,
            relevant_chunks=relevant_chunks,
            chat_history=st.session_state.chat_history
        )

    # Save assistant response
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": answer
    })

    with st.chat_message("assistant"):
        st.markdown(answer)

        with st.expander(
            "📚 Sources Used"
        ):

            for i, chunk in enumerate(relevant_chunks):

                st.markdown(
                    f"**Source {i+1}: "
                    f"{chunk['source']} "
                    f"— Page {chunk['page']}**"
                )

                st.caption(
                    chunk["text"][:400] + "..."
                )

                st.divider()