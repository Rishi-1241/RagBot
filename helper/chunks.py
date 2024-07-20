import firebase_admin
from firebase_admin import credentials, firestore
import openai
from dotenv import load_dotenv
import os
from langchain_openai import OpenAIEmbeddings
from langchain_google_firestore import FirestoreVectorStore
from dataclasses import dataclass

# Load environment variables from .env file
load_dotenv()

# Initialize Firestore
cred = credentials.Certificate('package.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize OpenAI API with API key from environment variables
openai_key = os.getenv('OPENAI_API_KEY')

# Function to count tokens by splitting text
def count_tokens(text):
    tokens = text.split()
    return len(tokens)

# Function to split file into chunks without exceeding 500 tokens
def split_file_into_chunks(filename, max_tokens=400):
    chunks = []
    with open(filename, 'r', encoding='utf-8') as file:
        current_chunk = ''
        for line in file:
            line = line.strip()
            if line.startswith('/title'):
                if current_chunk:
                    if count_tokens(current_chunk) > max_tokens:
                        # Split the current chunk if it exceeds max_tokens
                        lines = current_chunk.split('\n')
                        temp_chunk = ''
                        for l in lines:
                            if count_tokens(temp_chunk + l + '\n') > max_tokens:
                                chunks.append(temp_chunk.strip())
                                temp_chunk = l + '\n'
                            else:
                                temp_chunk += l + '\n'
                        if temp_chunk:
                            chunks.append(temp_chunk.strip())
                        current_chunk = ''
                    else:
                        chunks.append(current_chunk.strip())
                        current_chunk = ''
                current_chunk += line.replace('/title', '') + '\n'
            else:
                current_chunk += line + '\n'
        if current_chunk:
            if count_tokens(current_chunk) > max_tokens:
                lines = current_chunk.split('\n')
                temp_chunk = ''
                for l in lines:
                    if count_tokens(temp_chunk + l + '\n') > max_tokens:
                        chunks.append(temp_chunk.strip())
                        temp_chunk = l + '\n'
                    else:
                        temp_chunk += l + '\n'
                if temp_chunk:
                    chunks.append(temp_chunk.strip())
            else:
                chunks.append(current_chunk.strip())
    return chunks

# Function to store chunks in a file
# Function to store chunks in a file with --- separator
def store_chunks_to_file(chunks, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for i, chunk in enumerate(chunks, start=1):
            file.write(f"Chunk {i}:\n")
            file.write(chunk + '\n\n')  # Adding double newline to separate chunks
            file.write("---\n")


# Replace 'datafile.txt' with your actual file path
filename = 'datafile.txt'
chunks = split_file_into_chunks(filename)

# Store chunks in 'chunk.txt' file
#store_chunks_to_file(chunks, 'chunk3.txt')

#rint("Chunks have been stored in 'chunk.txt'.")

embeddings = OpenAIEmbeddings(api_key=openai_key)

# Define a Document class to hold page content and metadata
@dataclass
class Document:
    page_content: str
    metadata: dict  # Assuming metadata is a dictionary

# Convert chunks into Document objects
documents = [Document(page_content=chunk, metadata={}) for chunk in chunks]

# Store chunks and embeddings in Firestore
vectorstore = FirestoreVectorStore.from_documents(
    collection='rag_lawsikho4',
    documents=documents,
    embedding=embeddings,
)

print("Chunks and embeddings have been stored in Firestore.")
