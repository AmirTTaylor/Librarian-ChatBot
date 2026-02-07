#Database hosted locally for quick search use for our chatbot
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

#Bring in the file containing book data
df = pd.read_csv("books.csv")

#Load the yourbooks file
loader = TextLoader("yourbooks.txt", encoding = "utf-8")
txtDocuments = loader.load()

#Splitting text file into chunks (Hard to embed large chunks)
textSplitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)
txtChunks = textSplitter.split_documents(txtDocuments)

#Embedding Model
embeddings = OllamaEmbeddings(model = "nomic-embed-text") # Define the embeddings model

#Chroma Database Location
db_location = "./chroma_langchain_db"
add_documents = not os.path.exists(db_location) # Check is database location exist

#Intitalize an empty vector store
vector_store = Chroma( #Intialize the vectore store
    collection_name = "Books",
    persist_directory = db_location,
    embedding_function = embeddings,
)

if add_documents: #if it doesn't prepare data by converting it into documents
    documents = []

    #Turning CSV contents into docs
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

    #Turn txt contents into docs
    for chunk in txtChunks:
        chunk.metadata["source"] = "history"
        documents.append(chunk)
        
    # Add data to the vectore store
    vector_store.add_documents(documents = documents)
    
# Connect vector store to chatbot
retriever = vector_store.as_retriever(
    #Number of books recommendations outputted
    search_kwargs = { "k": 3} 
)