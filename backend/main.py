from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever
import os
import platform
import sys
import hashlib

# Base directory — all file paths are built relative to this so the app
# works regardless of what directory you run it from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Holds the logged-in user's ID for the current session.
# All functions that read/write user files use this.
current_user_id = None

#Functions

def hash_password(password):
    """Returns a SHA-256 hex digest of the given password."""
    return hashlib.sha256(password.encode()).hexdigest()

def start():
    print("Welcome to BookWorm")
    print("1. Login\n2. Sign Up\nQ. Quit")

    while True:
        choice = input("Enter [1], [2], or [Q]: ").strip().upper()
        match choice:
            case "1":
                clear()
                login()
                return
            case "2":
                clear()
                signup()
                return
            case "Q":
                clear()
                sys.exit(0)
            case _:
                print("Invalid input. Please enter 1, 2, or Q.")

def login():
    global current_user_id
    try:
        with open(os.path.join(BASE_DIR, "profiles.txt"), "r") as profiles:
            # Build a dict of {username: hashed_password} from the file
            accounts = {}
            for line in profiles:
                line = line.strip()
                if ":" in line:
                    stored_username, stored_hash = line.split(":", 1)
                    accounts[stored_username] = stored_hash
    except FileNotFoundError:
        print("Something went wrong. Error 1")
        sys.exit()

    # Keep asking until the user enters valid credentials
    while True:
        username = input("Username: ")
        password = input("Password: ")
        password_hash = hash_password(password)

        if accounts.get(username) == password_hash:
            current_user_id = username  # use just the username as the ID
            clear()
            homepage()
            return
        else:
            clear()
            print("Username or Password is incorrect. Try again.")

def signup():
    profiles_path = os.path.join(BASE_DIR, "profiles.txt")
    try:
        # Read existing accounts into a set of known usernames
        with open(profiles_path, "r") as profiles:
            existing_usernames = set()
            for line in profiles:
                line = line.strip()
                if ":" in line:
                    existing_usernames.add(line.split(":", 1)[0])
    except FileNotFoundError:
        existing_usernames = set()

    while True:
        username = input("Create a Username: ")
        password = input("Create a Password: ")
        confirm = input("Confirm Password: ")

        if username in existing_usernames:
            clear()
            print("That username is already taken. Try a different one.")
            continue

        if password != confirm:
            clear()
            print("Passwords do not match. Try again.")
            continue

        # Write the new account as username:hashed_password
        password_hash = hash_password(password)
        with open(profiles_path, "a") as profiles:
            profiles.write(f"{username}:{password_hash}\n")

        clear()
        print("Account created! Please log in.")
        login()
        return

def homepage():
    #Print Homepage
    print("_________________________________________________________\n"+"Welcome to your personal library!!\n")
    
    print("1.My Library\n"+"2.AI Librarian(Book Recommendations)\n"+"Q. Sign out")
    
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
            global current_user_id
            current_user_id = None  # clear the session on sign out
            clear()
            start()

def mylibrary():
    print("_____________________________________________")
    print("1. Finished Books")
    print("2. Add a Book")
    print("3. To-Be-Read List (TBR)")
    print("4. Currently Reading")
    print("H. Homepage")

    navigate = input("Enter 1, 2, 3, 4, or H to navigate: ").strip().upper()
    while navigate not in ("1", "2", "3", "4", "H"):
        navigate = input("Please enter 1, 2, 3, 4, or H: ").strip().upper()

    match navigate:
        case "1":
            clear()
            finishedbooks()
        case "2":
            clear()
            addbook()
        case "3":
            clear()
            tbr()
        case "4":
            clear()
            currently_reading()
        case "H":
            clear()
            homepage()

def finishedbooks():
    books_file = os.path.join(BASE_DIR, f"{current_user_id}_books.txt")

    try:
        with open(books_file, "r") as f:
            content = f.read()
    except FileNotFoundError:
        content = ""

    if not content.strip():
        print("_____________________________________________________")
        print("You have no finished books logged yet.")
        choice = input("Enter [1] to add a book or [H] for Homepage: ").strip().upper()
        while choice not in ("1", "H"):
            choice = input("Please enter [1] or [H]: ").strip().upper()
        if choice == "1":
            clear()
            addbook()
        else:
            clear()
            homepage()
        return

    print("_____________________________________________________")
    print("Here is a list of your finished books:\n")
    print(content)

    back = input("Enter [B] to return to the library: ").strip().upper()
    while back != "B":
        back = input("Please enter [B] to return: ").strip().upper()

    clear()
    mylibrary()

def addbook():
    print("_____________________________________________")
    print("Add to:")
    print("1. Finished Books")
    print("2. To-Be-Read List")
    print("3. Currently Reading")
    print("H. Homepage")

    choice = input("Enter [1], [2], [3], or [H]: ").strip().upper()
    while choice not in ("1", "2", "3", "H"):
        choice = input("Please enter 1, 2, 3, or H: ").strip().upper()

    match choice:
        case "1":  # Add to Finished Books
            clear()
            print("_____________________________________________")
            print("Congrats on finishing a book!")
            print("Please provide the following info about the book.\n")
            title = input("Book Title: ")
            author = input("Author: ")
            review = input("Rating 1-5: ")
            notes = input("Notes: ")
            info = [
                f"Title: {title}\n",
                f"Author: {author}\n",
                f"Rating: {review}\n",
                f"Notes: {notes}\n",
                "-" * 32 + "\n"
            ]
            books_file = os.path.join(BASE_DIR, f"{current_user_id}_books.txt")
            with open(books_file, "a+") as f:
                f.writelines(info)

            print("\nBook added to your finished list!")
            back = input("Enter [B] to return to the library: ").strip().upper()
            while back != "B":
                back = input("Please enter [B] to return: ").strip().upper()
            clear()
            mylibrary()

        case "2":  # Add to TBR
            clear()
            print("_____________________________________________")
            print("Adding to your To-Be-Read list!\n")
            title = input("Book Title: ")
            author = input("Author: ")
            theme = input("Theme: ")
            notes = input("Notes: ")
            info = [
                f"Title: {title}\n",
                f"Author: {author}\n",
                f"Theme: {theme}\n",
                f"Notes: {notes}\n",
                "-" * 32 + "\n"
            ]
            tbr_file = os.path.join(BASE_DIR, f"{current_user_id}_tbr.txt")
            with open(tbr_file, "a+") as f:
                f.writelines(info)

            print("\nBook added to your TBR!")
            back = input("Enter [B] to return to the library: ").strip().upper()
            while back != "B":
                back = input("Please enter [B] to return: ").strip().upper()
            clear()
            mylibrary()

        case "3":  # Add to Currently Reading
            clear()
            print("_____________________________________________")
            print("Adding to your Currently Reading list!\n")
            title = input("Book Title: ")
            author = input("Author: ")
            notes = input("Notes so far: ")
            info = [
                f"Title: {title}\n",
                f"Author: {author}\n",
                f"Notes: {notes}\n",
                "-" * 32 + "\n"
            ]
            reading_file = os.path.join(BASE_DIR, f"{current_user_id}_reading.txt")
            with open(reading_file, "a+") as f:
                f.writelines(info)

            print("\nBook added to Currently Reading!")
            back = input("Enter [B] to return to the library: ").strip().upper()
            while back != "B":
                back = input("Please enter [B] to return: ").strip().upper()
            clear()
            mylibrary()

        case "H":
            clear()
            homepage()

def tbr():
    tbr_file = os.path.join(BASE_DIR, f"{current_user_id}_tbr.txt")

    try:
        with open(tbr_file, "r") as f:
            content = f.read()
    except FileNotFoundError:
        content = ""

    if not content.strip():
        print("_____________________________________________________")
        print("Your TBR list is empty.")
        choice = input("Enter [1] to add a book or [H] for Homepage: ").strip().upper()
        while choice not in ("1", "H"):
            choice = input("Please enter [1] or [H]: ").strip().upper()
        if choice == "1":
            clear()
            addbook()
        else:
            clear()
            homepage()
        return

    print("_____________________________________________________")
    print("Here is your TBR:\n")
    print(content)

    back = input("Enter [B] to return to the library: ").strip().upper()
    while back != "B":
        back = input("Please enter [B] to return: ").strip().upper()

    clear()
    mylibrary() 

def currently_reading():
    reading_file = os.path.join(BASE_DIR, f"{current_user_id}_reading.txt")

    try:
        with open(reading_file, "r") as f:
            content = f.read()
    except FileNotFoundError:
        content = ""

    if not content.strip():
        print("_____________________________________________________")
        print("You are not currently reading anything.")
        choice = input("Enter [1] to add a book or [H] for Homepage: ").strip().upper()
        while choice not in ("1", "H"):
            choice = input("Please enter [1] or [H]: ").strip().upper()
        if choice == "1":
            clear()
            addbook()
        else:
            clear()
            homepage()
        return

    print("_____________________________________________________")
    print("Currently Reading:\n")
    print(content)

    back = input("Enter [B] to return to the library: ").strip().upper()
    while back != "B":
        back = input("Please enter [B] to return: ").strip().upper()

    clear()
    mylibrary()

def chatbot():
    model = OllamaLLM(model = "qwen2") # The chatbot model
    
    #This is the template of instructions for the chatbot
    template = """
    You are James, a warm and knowledgeable librarian chatbot for BookWorm, a book community app.
    You help users discover books they will love and answer questions about books and reading.

    You have access to two sources of information:
    1. A catalog of books you MAY recommend from.
    2. The user's personal reading history (books they have already read).

    STRICT RULES — follow these without exception:
    - You must ONLY recommend books that appear EXACTLY in the catalog below.
    - NEVER recommend a book that is not in the catalog, even if you know it from your training.
    - NEVER recommend a book the user has already read.
    - If the catalog contains no suitable match, say so clearly. Do NOT fill the gap with outside knowledge.
    - You may answer general factual questions (e.g. "who wrote Fahrenheit 451?") using your own knowledge.
    - BUT if the user asks for book suggestions, similar books, or recommendations in any form,
      you MUST only draw from the catalog. No exceptions.

    User reading history (use this to understand their taste — do NOT recommend these):
    {history_text}

    Available catalog (ONLY recommend books from this exact list):
    {books}

    Conversation so far:
    {chat_history}

    User message:
    {info}

    Response guidelines:
    - If recommending books: suggest up to 3, use the exact title from the catalog, and give a
      one or two sentence explanation of why each fits the user's taste.
    - If the user asks a follow-up question, use the conversation history to understand context.
    - Keep your tone friendly, concise, and enthusiastic about reading.
    - If no catalog books match the request, say so clearly and invite the user to try a different request.
    """

    #Turns the template into ChatPromptTemplate Object
    prompt = ChatPromptTemplate.from_template(template)

    #This line feeds the prompt to the model
    chain = prompt | model

    # Stores the conversation so James can answer follow-up questions
    chat_history = []

    # Load this user's reading history from their personal books file
    books_file = os.path.join(BASE_DIR, f"{current_user_id}_books.txt")
    try:
        with open(books_file, "r", encoding="utf-8") as f:
            history_text = f.read().strip() or "No reading history yet."
    except FileNotFoundError:
        history_text = "No reading history yet."

    print("Hi! I am James, your librarian chatbot!\n__________________________________________________________")

    #loop user input for talking with the chatbot
    while True:
        info = input("How can I help you?\n")

        # Search the catalog for relevant books based on the user's message
        docs = retriever.invoke(info)

        # Format catalog results into clean text for the prompt
        books = "\n\n".join(
            f"- {doc.metadata.get('title', 'Unknown Title')} by {doc.metadata.get('author', 'Unknown')}: {doc.page_content}"
            for doc in docs
        )

        # Format chat history into a readable string for the prompt
        formatted_history = "\n".join(
            f"{role}: {message}"
            for role, message in chat_history
        ) if chat_history else "No conversation yet."

        # Retrieve an answer based on the info and given list of books
        result = chain.invoke({
            "books": books,
            "history_text": history_text,
            "chat_history": formatted_history,
            "info": info
        })

        # Save this exchange to chat history
        chat_history.append(("User", info))
        chat_history.append(("James", result))

        print("\n__________________________________________________________")
        print("\n" + result)
        print("\n__________________________________________________________")
        
        # Back to Homepage
        back = input("Another message [Enter to continue] or [B] for Homepage: ")
        if back.strip().upper() == "B":
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
    clear()
    start()