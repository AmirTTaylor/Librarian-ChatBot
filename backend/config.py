from dotenv import load_dotenv
import os
#This file processes the .env file into use for the other files that need its config data

#Read the .env file to populate the os.environ value used to retrive configurable variables
load_dotenv()

BOOKWORM_MODEL= os.environ.get('BOOKWORM_MODEL','phi3:mini')
BOOKWORM_EMBED_MODEL = os.environ.get('BOOKWORM_EMBED_MODEL','nomic-embed-text')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))