#Database hosted locally for quick search use for our chatbot
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

df = pd.read_csv("books.csv") #Bring in the file containing book data
embeddings = OllamaEmbeddings(model = "nomic-embed-text") # Define the embeddings model

db_location = "./chroma_langchain_db"
add_documents = not os.path.exists(db_location) # Check is database location exist

if add_documents: #if it doesn't prepare data by converting it into documents
    documents = []

    for i, row in df.iterrows():
        document = Document(
            page_content=f"{row['Description']} Themes: {row['Themes']}",
            metadata={
                "title": row["Title"],
                "author": row["Author"],
                "genre": row["Genre"],
                "mood": row["Mood"]
            }
        )
        documents.append(document)
        
vector_store = Chroma( #Intialize the vectore store
    collection_name = "Books",
    persist_directory = db_location,
    embedding_function = embeddings
)

if add_documents: # Add data to the vectore store
    vector_store.add_documents(documents = documents)

retriever = vector_store.as_retriever( # Connect vector store to chatbot
    search_kwargs = { "k": 3} #Number of books recommendations outputted}
)