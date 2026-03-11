from sentence_transformers import SentenceTransformer
from groq import Groq


def query_rag(question, chat_history, groq_client, chroma_client, embedding_model):
    # ── Get collection ────────────────────────────────────────────────────────
    try:
        collection = chroma_client.get_collection("research_papers")
        count = collection.count()
        if count == 0:
            return "⚠️ Database is empty. Please upload PDFs first.", []
    except Exception:
        return "⚠️ No papers loaded yet. Please upload PDFs first.", []

    # ── Embed question ────────────────────────────────────────────────────────
    q_emb = embedding_model.encode(question).tolist()
    n_res = min(4, count)

    # ── Query ChromaDB ────────────────────────────────────────────────────────
    results = collection.query(query_embeddings=[q_emb], n_results=n_res)

    if not results.get("documents") or not results["documents"][0]:
        return "I couldn't find relevant context in the uploaded papers.", []

    context = "\n\n".join(results["documents"][0])

    # ✅ Safe metadata extraction
    meta = results.get("metadatas")
    sources = list(set(
        m["source"] for m in (meta[0] if meta and meta[0] else [])
        if m and "source" in m
    ))

    # ── Build messages ────────────────────────────────────────────────────────
    messages = [{"role": "system", "content": (
        "You are PaperMind, an expert AI research assistant. "
        "Answer using ONLY the provided context. Be precise, insightful, and structured. "
        "If the answer is not in the context, say so honestly."
    )}]

    for turn in chat_history[-4:]:
        messages += [
            {"role": "user",      "content": turn["user"]},
            {"role": "assistant", "content": turn["assistant"]}
        ]

    messages.append({
        "role": "user",
        "content": f"Context:\n{context}\n\nQuestion: {question}"
    })

    # ── Call Groq ─────────────────────────────────────────────────────────────
    try:
        r = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.3,
            max_tokens=1024
        )
        return r.choices[0].message.content, sources
    except Exception as e:
        return f"⚠️ Error communicating with AI: {e}", []