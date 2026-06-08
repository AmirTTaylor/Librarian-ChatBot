#Database hosted locally for quick search use for our chatbot
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

# Base directory — all file paths are built relative to this
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#Bring in the file containing book data
df = pd.read_csv(os.path.join(BASE_DIR, "books.csv"))

#Embedding Model
embeddings = OllamaEmbeddings(model = "nomic-embed-text")

#Chroma Database Location — stores only the book catalog
db_location = os.path.join(BASE_DIR, "chroma_langchain_db")
add_documents = not os.path.exists(db_location)

#Initialize the vector store
vector_store = Chroma(
    collection_name = "Books",
    persist_directory = db_location,
    embedding_function = embeddings,
)

if add_documents:
    # Load catalog from CSV into the vector store (one-time setup)
    documents = []
    for i, row in df.iterrows():
        document = Document(
            page_content=f"{row['Description']} Themes: {row['Themes']}",
            metadata={
                "source": "catalog",
                "title": row["Title"],
                "author": row["Author"],
                "genre": row["Genre"],
                "mood": row["Mood"]
            }
        )
        documents.append(document)

    vector_store.add_documents(documents=documents)

# Catalog retriever — searches only the book catalog
retriever = vector_store.as_retriever(
    # Fetch enough results so we always have good catalog coverage
    search_kwargs={"k": 8}
)
