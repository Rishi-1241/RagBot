import os
import json
from dotenv import load_dotenv
from google.cloud import firestore
from google.oauth2 import service_account
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain_google_firestore import FirestoreVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize Firestore client
try:
    with open('package.json') as f:
        credentials_info = json.load(f)

    credentials = service_account.Credentials.from_service_account_info(credentials_info)
    project_id = credentials_info.get("project_id")

    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "package.json"

    db = firestore.Client(project=project_id, credentials=credentials)
except Exception as e:
    print(f'Error initializing Firestore client: {e}')
    exit(1)

# Read the data file
try:
    with open('datafile.txt', 'r', encoding='utf-8') as file:
        data = file.read()
except Exception as e:
    print(f'Error reading data file: {e}')
    exit(1)

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(api_key=openai_api_key)

# Initialize text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    length_function=len,
    is_separator_regex=False,
)

# Split the text
chunk_text = text_splitter.split_text(data)

# Create documents by splitting the text
documents = text_splitter.create_documents([data])
print(f"Type of documents: {type(documents)}")  # Debug output: check type of documents


# Initialize FirestoreVectorStore
def initialize_vectorstore(documents, embeddings, collection='embedd_test'):
    try:
        # Check if the collection already contains documents
        collection_ref = db.collection(collection)
        docs = collection_ref.stream()
        if any(docs):

            print("Documents already exist in Firestore.")
            return FirestoreVectorStore(collection=collection, embedding_service=embeddings)

        vectorstore = FirestoreVectorStore.from_documents(
            collection=collection,
            documents=documents,
            embedding=embeddings
        )
        print(f"Stored {len(documents)} documents in Firestore.")
        return vectorstore
    except Exception as e:
        print(f'Error creating FirestoreVectorStore: {e}')
        return None
