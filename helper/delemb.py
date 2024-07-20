from google.cloud import firestore
from google.oauth2 import service_account
import json

# Load the credentials from the JSON file
with open('package.json') as f:
    credentials_info = json.load(f)

# Create the credentials object
credentials = service_account.Credentials.from_service_account_info(credentials_info)

# Initialize the Firestore client
db = firestore.Client(project=credentials.project_id, credentials=credentials)

def delete_all_embeddings():
    try:
        embeddings_collection = db.collection('embeddings')
        # Get all documents in the collection
        docs = embeddings_collection.stream()
        # Delete each document
        for doc in docs:
            doc.reference.delete()
        print('All embeddings have been deleted successfully.')
    except Exception as e:
        print(f'Error deleting embeddings: {e}')

# Call the function to delete all embeddings
delete_all_embeddings()
