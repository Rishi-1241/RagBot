# Project Overview

This project is an end-to-end implementation of a LawSikho Assistant chatbot that integrates with WhatsApp via Twilio. The project includes web scraping, content processing, and a Flask application to handle WhatsApp interactions. It leverages Google Firestore for storage and OpenAI's GPT model for generating responses.

## Table of Contents

- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)
- [Functionality](#functionality)
- [Usage](#usage)
- [License](#license)

## Installation

To get started, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/yourrepository.git
   cd yourrepository
Create a Virtual Environment:

bash
Copy code
python -m venv myenv
source myenv/bin/activate  # On Windows use: myenv\Scripts\activate
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Download the required service account key for Firebase Firestore.

Set Up Environment Variables:
Create a .env file in the root directory of your project and add the following variables:

dotenv
Copy code
OPENAI_API_KEY=your_openai_api_key
FCM_API_KEY=your_fcm_api_key
FIREBASE_SERVICE_ACCOUNT_KEY=path_to_your_service_account_key
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=your_twilio_whatsapp_number
Project Structure
webscrape.py: Contains functions for scraping content from a URL, extracting headings, specific div content, and URLs, and formatting the extracted content into a text file.
firestore.py: Handles interactions with Firebase Firestore, including splitting text into chunks and storing them along with embeddings.
main.py: Defines the LawSikhoAssistant class, which initializes the chatbot with OpenAI and Firestore, handles query processing, and manages chat history.
twilio.py: Implements a Flask application to handle incoming WhatsApp messages via Twilio, process them with the LawSikhoAssistant, and respond accordingly.
Functionality
webscrape.py
fetch_and_parse_url(url): Fetches the content from the given URL and parses it using BeautifulSoup.
extract_headings_with_content(soup): Extracts headings (h1, h2, h3) and associated content from the parsed HTML.
extract_specific_div_content(soup): Extracts and returns content from div elements with a specific class (refundPolicy).
extract_urls(soup, base_url): Extracts and returns URLs from anchor tags, resolving relative URLs to absolute ones.
format_extracted_content(headings_content, div_content, urls): Formats the extracted headings, div content, and URLs into a structured text format.
main(): Coordinates the scraping, extraction, formatting, and saving of content to a text file.
firestore.py
count_tokens(text): Counts the number of tokens in a given text.
split_file_into_chunks(filename, max_tokens=400): Splits the content of a file into chunks, ensuring that no chunk exceeds the specified token limit.
store_chunks_to_file(chunks, filename): Saves the chunks into a file, separating them with a custom separator.
Document class: Represents a document with page content and metadata.
Storing chunks and embeddings: Converts text chunks into Document objects and stores them in Firestore along with their embeddings.
main.py
LawSikhoAssistant class: The core class for the chatbot, which initializes necessary components, handles queries, and maintains chat history.
_load_env(): Loads environment variables.
_initialize_firestore(): Initializes Firebase Firestore with credentials.
_initialize_embeddings(): Sets up OpenAI embeddings.
_initialize_vectorstore(): Initializes FirestoreVectorStore with the embeddings.
_initialize_text_splitter(): Sets up the text splitter for chunking content.
_initialize_retriever(): Initializes the retriever for fetching relevant documents.
_search_query(): Handles the query processing logic.
_create_chain(): Creates the processing chain for handling queries.
query(user_query: str): Processes a user query and returns a response.
twilio.py
webhook(): Handles incoming messages from Twilio, processes them with the LawSikhoAssistant, and responds via Twilio.
Usage
Run the Web Scraping Script:

bash
Copy code
python webscrape.py
Run the Firestore Processing Script:

bash
Copy code
python firestore.py
Start the Flask Application:

bash
Copy code
python twilio.py
Interact with the WhatsApp Bot:
Send messages to the Twilio WhatsApp number to interact with the chatbot.

License
This project is licensed under the MIT License. See the LICENSE file for details.

css
Copy code

Feel free to adjust any specifics to better fit your project or personal preferences!
