from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever
import os
import platform
import sys
#Functions
def homepage():
    #Print Homepage
    print("_________________________________________________________\n"+"Welcome to your personal libary!!\n")
    
    print("1.My Library\n"+"2.AI Librarian(Book Recommendations)\n"+"Q. Quit")
    
    #Take user input for app navigation
    navigate = input("Enter 1 or 2 to navigate: ")
    
    #Ensure user inputs 1 or 2
    while navigate not in ("1","2","Q"):
        navigate = input("Please make sure your input is a 1 or 2: ")
    
    match navigate:
        case "1":
            clear()
            mylibrary()
        case "2":
            clear()
            chatbot()
        case "Q":
            sys.exit(0)

def mylibrary():
    #Menu
    print("_____________________________________________\n"+"1.Finished Books\n"+"2.Add a Book\n"+"3.To-Be-Read (TBR) List\n"+"H. Hompage")

    #Navigate menu
    navigate = input("Enter 1, 2, 3, or H to navigate: ")
    while navigate not in ("1","2","3","H"):
        navigate = input("Please make sure your input is a 1, 2, 3, or H: ")
    
    match navigate:
        case "1":
            clear()
            finishedbooks()
        case "2":
            clear()
            addbook()
        case "3":
            pass
        case "H":
            clear()
            homepage()

def finishedbooks():
    print("_____________________________________________________\n"+"Here is a list of your finished books:\n")
    
    #Access or create a text file to store the users previously read books
    try:
        with open("yourbooks.txt","r") as yourbooks:
            content = yourbooks.read()
            print(content)
    #Handle errors
    except FileNotFoundError:
        print("Soemthing went wrong. Error 1")   
        sys.exit()
    
    #Back to Library
    back = input("Enter [B] to return to the library page:")
    while back not in("B"):
        back = input("To return to library please enter [B]")
    
    clear()
    mylibrary()

def addbook():
    print("_____________________________________________\n"+"Congrats on finishing a book!!!!\n"+"Please porvide the following info about the book.")
    # Book info
    title = input("Book Title: ")
    author = input("Author :")
    review = input("Rating 1-5: ")
    notes = input("Notes: ")
    info = [
        f"Title: {title}\n",
        f"Author: {author}\n",
        f"Rating: {review}\n",
        f"Notes: {notes}\n",
        "-" * 32 + "\n"
    ]
    #Access or create a text file to store the users previously read books
    try:
        with open("yourbooks.txt","a+") as yourbooks:
            yourbooks.writelines(info)
    #Handle errors
    except FileNotFoundError:
        print("Soemthing went wrong. Error 1")   
        sys.exit()
        
    #Back to Library
    back = input("Enter [B] to return to the library page:")
    while back not in("B"):
        back = input("To return to library please enter [B]")
    
    clear()
    mylibrary()

def chatbot():
    model = OllamaLLM(model = "phi3:mini") # The chatbot model
    
    #This is the template of instructions for the chatbot
    template = """
    You are an expert librarian and book recommendation assistant.

    You are given:
    1. A catalog of available books you MAY recommend from.
    2. A history of books the user has already read.

    STRICT RULES:
    - You must ONLY recommend books from the catalog.
    - DO NOT recommend books the user has already read.
    - Use the user's reading history ONLY to infer preferences.
    - If no suitable recommendations exist, clearly say so.

    You will recommend up to 3 books.

    User reading history (for preference inference only):
    {history}

    Available catalog (recommend ONLY from this list):
    {books}

    User request:
    {info}

    Instructions:
    - Infer themes, genres, or styles the user prefers based on reading history
    - Select the best matching books from the catalog
    - Use book titles exactly as written
    - Briefly explain why each recommendation fits the user's interests
    - Format your response clearly and readably
    """


    #Turns the template into ChatPromptTemplate Object, this parses the string for placeholders and required inputs and formats it for the chatbot
    prompt = ChatPromptTemplate.from_template(template)

    #This line feeds the prompt to the model
    chain = prompt | model

    #loop user input for talking with the chatbot
    while True:
        
        print("Hi! I am James, your librarian chatbot!\n__________________________________________________________")
        info = input("How can I help you?\n")

        # Search book database to answer based on user info provided
        docs = retriever.invoke(info) 

        #Seperate Library Catalog and User History
        catalog = [doc for doc in docs if doc.metadata.get("source") == "catalog"]
        history = [doc for doc in docs if doc.metadata.get("source") == "history"]
        
        # Format the data retrieved into cleaner text
        books = "\n\n".join(
            f"- {doc.metadata.get('title', 'Unknown Title')}: {doc.page_content}"
        for doc in catalog
        )
        history_text = "\n\n".join(
            f"- {doc.page_content}"
            for doc in history
        ) 


        
        # Retireve an answer based on the info and given list of books
        result = chain.invoke({"books": books, "history": history, "info": info})

        print("\n__________________________________________________________")
        print("\n"+result)
        print("\n__________________________________________________________")
        
        #Back to Homepage
        back = input("Another recommendation[Y]? or enter [B] for Homepage:")
        if back in ("B"):
            clear()
            homepage()
    
        clear()
        
def clear():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')
#Run
if __name__ == "__main__":
    homepage()