from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever
import sys
def homepage():
    #Print Homepage
    print("_________________________________________________________\n"+"Welcome to your personal libary!!\n")
    
    print("""
          1.My Library
          2.AI Librarian(Book Recommendations)""")
    
    #Take user input for app navigation
    navigate = input("Enter 1 or 2 to navigate: ")
    
    #Ensure user inputs 1 or 2
    while(navigate != 1 or navigate != 2):
        navigate = input("Please make sure your input is a 1 or 2: ")
    
    match navigate:
        case 1:
            mylibrary()
        case 2:
            chatbot()

def mylibrary():
    #Menu
    print("""_____________________________________________\n
          1.Finished Books
          2.Add a Book
          3.To-Be-Read (TBR) List""")
    
    #Navigate menu
    navigate = input("Enter 1 or 2 to navigate: ")
    while(navigate != 1 or navigate != 2 or navigate != 3):
        navigate = input("Please make sure your input is a 1, 2, or 3: ")
    
    match navigate:
        case 1:
            finishedbooks()
        case 2:
            addbook()
            pass
        case 3:
            pass

def finishedbooks():
    print(""""_____________________________________________________
          Here is a list of your finished books:\n""")
    
    #Access or create a text file to store the users previously read books
    try:
        with open("yourbooks.txt","a+") as yourbooks:
            content = yourbooks.read()
            print(content)
    #Handle errors
    except FileNotFoundError:
        print("Soemthing went wrong. Error 1")   
        sys.exit()

def addbook():
    print("""_____________________________________________\n
          Congrats on finishing a book!!!!\n
          Please porvide the following info about the book.
          """)
    #Access or create a text file to store the users previously read books
    try:
        with open("yourbooks.txt","a+") as yourbooks:
            
    #Handle errors
    except FileNotFoundError:
        print("Soemthing went wrong. Error 1")   
        sys.exit()

def chatbot():
    model = OllamaLLM(model = "phi3:mini") # The chatbot model
    
    #This is the template of instructions for the chatbot
    template = """
    You are an expert librarian and book recommendation assistant.

    You are given a library of books.
    You must ONLY recommend books that appear in the provided library.
    Do NOT invent or mention books that are not listed.
    If no suitable recommendations exist, clearly say so.

    You will recommend up to 3 books.

    Library (titles, genres, and descriptions):
    {books}

    User context and preferences:
    {info}

    Instructions:
    - Select the most relevant books from the library
    - Use the book titles exactly as written
    - Explain briefly why each book matches the user's interests
    - Format your response with clear spacing and readability
    - Ask user if they have follow up questions on any of the books
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
        books = retriever.invoke(info) 

        # Format the data retrieved into cleaner text
        books_text = "\n\n".join( 
        f"- {doc.page_content}"
        for doc in books
        )
        
        # Retireve an answer based on the info and given list of books
        result = chain.invoke({"books": books_text, "info": info})

        print("\n__________________________________________________________")
        print("\n"+result)
        print("\n__________________________________________________________")
