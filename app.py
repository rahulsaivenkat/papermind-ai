import streamlit as st
import os
from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq

from styles import apply_custom_styles
from ingest import process_pdf
from rag import query_rag

load_dotenv()

st.set_page_config(
    page_title="PaperMind AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_styles()

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

@st.cache_resource
def load_chroma():
    return chromadb.PersistentClient(path="chroma_db")

embedding_model = load_embedding_model()
chroma_client = load_chroma()

def get_groq():
    key = os.getenv("GROQ_API_KEY")
    return Groq(api_key=key) if key else None

for key, default in [
    ("chat_history", []), ("papers_loaded", []), ("db_ready", False),
    ("summaries", {}), ("total_chunks", 0), ("uploader_key", 0)
]:
    if key not in st.session_state:
        st.session_state[key] = default

if "sync_done" not in st.session_state:
    try:
        col = chroma_client.get_collection("research_papers")
        count = col.count()
        if count > 0:
            st.session_state.db_ready = True
            st.session_state.total_chunks = count
            res = col.get(include=["metadatas"])
            if res and res.get("metadatas"):
                unique_papers = list(set(m["source"] for m in res["metadatas"] if m and "source" in m))
                st.session_state.papers_loaded = unique_papers
    except Exception:
        pass
    st.session_state.sync_done = True

with st.sidebar:
    st.markdown("""
    <div class="pm-header">
        <div class="pm-logo">🔬</div>
        <div>
            <p class="pm-title">PaperMind</p>
            <p class="pm-subtitle">AI Research Assistant</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    groq_client = get_groq()
    if not groq_client:
        st.markdown('<div class="section-label">🔑 API Access</div>', unsafe_allow_html=True)
        key_input = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
        if key_input:
            os.environ["GROQ_API_KEY"] = key_input
            st.success("✅ Connected")
            st.rerun()
    else:
        st.success("✅ Groq API Connected")

    st.markdown('<div class="section-label">📄 Upload Papers</div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Drop PDF files here", type=["pdf"],
                                      accept_multiple_files=True, label_visibility="collapsed",
                                      key=f"uploader_{st.session_state.uploader_key}")

    if uploaded_files:
        if not groq_client:
            st.warning("Enter your Groq API key first!")
        else:
            for uf in uploaded_files:
                if uf.name not in st.session_state.papers_loaded:
                    with st.spinner(f"Processing {uf.name[:25]}..."):
                        chunks, summary = process_pdf(uf.read(), uf.name, groq_client, chroma_client, embedding_model)
                        if chunks > 0:
                            st.session_state.papers_loaded.append(uf.name)
                            st.session_state.total_chunks += chunks
                            st.session_state.db_ready = True
                            if summary:
                                st.session_state.summaries[uf.name] = summary
                            st.success(f"✅ {chunks} chunks indexed")
                        else:
                            st.error(f"❌ Failed to extract text: {uf.name}")

    if st.session_state.papers_loaded:
        st.markdown('<div class="section-label">📚 Loaded Papers</div>', unsafe_allow_html=True)
        for paper in st.session_state.papers_loaded:
            label = paper[:35] + ("..." if len(paper) > 35 else "")
            st.markdown(f'<div class="paper-tag"><div class="paper-dot"></div>{label}</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="stats-bar">
            <div class="stat-item">Papers: <span>{len(st.session_state.papers_loaded)}</span></div>
            <div class="stat-item">Chunks: <span>{st.session_state.total_chunks}</span></div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear DB", use_container_width=True):
                try: chroma_client.delete_collection("research_papers")
                except Exception: pass
                st.session_state.papers_loaded = []
                st.session_state.db_ready = False
                st.session_state.summaries = {}
                st.session_state.total_chunks = 0
                st.session_state.uploader_key += 1
                st.rerun()
        with col2:
            if st.button("🧹 Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()

    st.markdown('<div class="section-label">💡 Try Asking</div>', unsafe_allow_html=True)
    for tip in ["What is the main contribution?","Explain the methodology",
                "What datasets were used?","Summarize the key results","Compare the approaches"]:
        st.markdown(f'<div style="font-size:0.75rem;color:#2a4a6a;padding:3px 0;font-family:JetBrains Mono,monospace;">› {tip}</div>', unsafe_allow_html=True)

if st.session_state.summaries:
    st.markdown('<div class="section-label">📋 Paper Summaries</div>', unsafe_allow_html=True)
    tabs = st.tabs([f"📄 {n[:30]}" for n in st.session_state.summaries])
    for tab, (name, summary) in zip(tabs, st.session_state.summaries.items()):
        with tab:
            st.markdown(f"""
            <div class="summary-card">
                <div class="summary-title">⚡ Auto-Generated Summary · {name}</div>
                {summary.replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)
    st.markdown("---")

st.markdown('<div class="section-label">💬 Research Chat</div>', unsafe_allow_html=True)

chat_container = st.container(height=440)
with chat_container:
    if not st.session_state.chat_history:
        st.markdown("""
        <div class="empty-state">
            <h3>🔬 PaperMind Ready</h3>
            <p>Upload a research paper from the sidebar<br>then ask anything about it below</p>
        </div>
        """, unsafe_allow_html=True)

    for turn in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(turn["user"])
        with st.chat_message("assistant", avatar="🔬"):
            st.write(turn["assistant"])
            if turn.get("sources"):
                badges = "".join(f'<span class="source-badge">📄 {s[:25]}</span>' for s in turn["sources"])
                st.markdown(badges, unsafe_allow_html=True)

# ✅ ONLY FIX: initialize answer/sources before scope, wrap query in try/except
if prompt := st.chat_input("Ask anything about your papers...", disabled=not st.session_state.db_ready):
    gc = get_groq()
    if not gc:
        st.error("Please enter your Groq API key in the sidebar!")
    else:
        answer, sources = "", []
        with chat_container:
            with st.chat_message("user"):
                st.write(prompt)
            with st.chat_message("assistant", avatar="🔬"):
                with st.spinner("🔍 Searching and generating answer..."):
                    try:
                        answer, sources = query_rag(prompt, st.session_state.chat_history, gc, chroma_client, embedding_model)
                    except Exception as e:
                        answer = f"⚠️ Error: {e}"
                        sources = []
                    st.write(answer)
                    if sources:
                        badges = "".join(f'<span class="source-badge">📄 {s[:25]}</span>' for s in sources)
                        st.markdown(badges, unsafe_allow_html=True)

        st.session_state.chat_history.append({"user": prompt, "assistant": answer, "sources": sources})

if not st.session_state.db_ready:
    st.info("⬅️ Upload at least one PDF paper from the sidebar to start chatting")
