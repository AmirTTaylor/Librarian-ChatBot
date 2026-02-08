# 📚 AI Librarian – Personal Book Recommendation System

An interactive, terminal-based AI librarian that recommends books based on a curated catalog **and** the user’s personal reading history. Built with **LangChain**, **Ollama**, and **ChromaDB**, this project demonstrates retrieval-augmented generation (RAG) and personalized recommendations using vector embeddings.

---
## 🛠️ Development Status

This project is still under active development.

- Additional testing is planned to further validate retrieval accuracy, grounding, and recommendation quality
- New features are planned, including:
  - A graphical user interface (GUI)
  - Improved personalization and filtering
  - Expanded library database

## 🚀 Features

- 📖 **Personal Library Management**
  - Add books you’ve finished reading
  - View your completed books list
  - Store reading history locally in a text file

- 🤖 **AI Book Recommendations**
  - Ask for recommendations by genre, themes, mood, or preferences
  - Recommendations are restricted to books in the provided catalog
  - User reading history is used to infer taste and avoid re-recommendations

- 🧠 **Retrieval-Augmented Generation (RAG)**
  - Book catalog and reading history are embedded into a local vector database
  - Semantic search retrieves relevant context before generation
  - Prevents hallucinated book recommendations

- 💾 **Local & Offline**
  - Runs fully locally using Ollama
  - No external APIs required
  - Vector database persisted on disk

---

## 🧱 Project Structure
  - main.py # App entry point and terminal UI
  -  vector.py # Vector store creation and retriever logic
  -  books.csv # Book catalog
  -  yourbooks.txt # User reading history (created at runtime)
  -  chroma_langchain_db/ # Persisted Chroma vector database
  -  requirements.txt # Python dependencies
  -  README.md
  ---

## 🖥️ Running the Project

### Prerequisites
- Python 3.10+
- Ollama installed and running  
  https://ollama.com/download

### Install dependencies
- bash
- pip install -r requirements.txt
- ollama pull phi3:mini
- ollama pull nomic-embed-text
