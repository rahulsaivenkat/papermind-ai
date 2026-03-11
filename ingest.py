import os
import tempfile
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def generate_summary(text, groq_client):
    try:
        r = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a research paper summarizer. Be concise and precise."},
                {"role": "user", "content": (
                    "Summarize this research paper in exactly 5 bullet points. "
                    "Cover: main contribution, methodology, key findings, datasets/experiments, and broader impact.\n\n"
                    f"Paper text:\n{text[:4000]}"
                )}
            ],
            temperature=0.2, max_tokens=400
        )
        return r.choices[0].message.content
    except Exception as e:
        return f"Summary unavailable: {e}"

def process_pdf(file_bytes, filename, groq_client, chroma_client, embedding_model):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    reader = PdfReader(tmp_path)
    full_text = "".join(p.extract_text() or "" for p in reader.pages)
    os.unlink(tmp_path)

    if not full_text.strip():
        return 0, None

    summary = generate_summary(full_text, groq_client)
    chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_text(full_text)
    
    collection = chroma_client.get_or_create_collection("research_papers")
    embeddings = embedding_model.encode(chunks).tolist()
    existing = collection.count()

    ids = [f"{filename}_{existing+i}" for i in range(len(chunks))]
    metadatas = [{"source": filename} for _ in range(len(chunks))]

    batch_size = 100
    for i in range(0, len(chunks), batch_size):
        collection.add(
            documents=chunks[i:i+batch_size],
            embeddings=embeddings[i:i+batch_size],
            ids=ids[i:i+batch_size],
            metadatas=metadatas[i:i+batch_size]
        )

    return len(chunks), summary