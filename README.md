📄 PaperMind AI
Intelligent Research Paper Assistant using Retrieval-Augmented Generation (RAG)

PaperMind AI is an AI-powered research assistant that allows users to upload academic papers and interact with them using natural language.
It uses Retrieval-Augmented Generation (RAG) to retrieve relevant sections from research papers and generate accurate answers using a large language model.

The system combines semantic search, vector databases, and LLM reasoning to provide context-aware answers grounded in the uploaded documents.

🚀 Features

• 📄 Upload research papers (PDF)
• 🧠 Automatic paper summarization
• 🔍 Semantic document retrieval using vector search
• 💬 Conversational chat with research papers
• 📚 Source citation for every answer
• ⚡ Fast LLM responses using Groq API
• 🎨 Clean interactive interface built with Streamlit

🧠 Architecture

PaperMind AI follows a Retrieval-Augmented Generation (RAG) architecture.

User Uploads PDF
        ↓
PDF Parsing (pypdf)
        ↓
Text Chunking
        ↓
Embedding Generation (SentenceTransformers)
        ↓
ChromaDB Vector Database
        ↓
Semantic Retrieval
        ↓
Groq LLM (Llama-3)
        ↓
Generated Answer

This approach ensures the AI answers based only on the uploaded research papers rather than hallucinating.

🛠 Tech Stack
Programming

Python

AI & NLP

Sentence Transformers

Groq LLM API (Llama-3)

LangChain Text Splitters

Vector Database

ChromaDB

Interface

Streamlit

PDF Processing

PyPDF

📂 Project Structure
papermind-ai
│
├── app.py          # Streamlit web application
├── ingest.py       # PDF processing and vector indexing
├── rag.py          # Retrieval-Augmented Generation logic
├── styles.py       # Custom UI styling
│
├── chroma_db/      # Vector database (generated)
├── requirements.txt
├── .gitignore
└── README.md
⚙️ Installation

Clone the repository:

git clone https://github.com/rahulsaivenkat/papermind-ai.git

Go into the project folder:

cd papermind-ai

Install dependencies:

pip install -r requirements.txt
🔑 Environment Setup

Create a .env file in the project root.

GROQ_API_KEY=your_api_key_here

You can get your API key from:

https://console.groq.com

▶️ Run the Application

Start the Streamlit app:

streamlit run app.py

The app will open in your browser.

💡 Example Questions

After uploading research papers, try asking:

What is the main contribution of this paper?

Explain the methodology used.

What datasets were used in the experiments?

Summarize the key results.

What are the limitations of this approach?
📊 Example Use Cases

• Research paper exploration
• Literature review assistance
• Understanding complex academic papers
• Comparing research methods

🔒 Security

Sensitive credentials such as API keys are stored in .env and excluded using .gitignore.

📈 Future Improvements

• Research paper comparison
• Multi-document reasoning
• Citation highlighting
• Paper recommendation system

👨‍💻 Author

Rahul Sai Venkat

GitHub:
https://github.com/rahulsaivenkat

⭐ If You Like This Project

Consider giving the repository a star.
