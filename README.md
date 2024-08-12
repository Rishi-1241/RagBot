# LawSikhoAssistant - RAGBOT

## Description

**LawSikhoAssistant** is an advanced AI-powered chatbot designed to interact with users over WhatsApp. It provides users with comprehensive information about legal courses offered by LawSikho, helping them make informed decisions about their legal education. The chatbot leverages state-of-the-art technologies to facilitate smooth communication, efficient data management, and accurate responses.

## Features

- **Natural Language Processing (NLP):** Utilizes OpenAI's GPT-3.5-turbo model to understand and generate human-like responses based on user queries.
- **Database Integration:** Uses Firebase Firestore to store and retrieve document embeddings, enabling scalable and efficient data management.
- **Text Splitting:** Automatically processes large text files by splitting them into smaller, manageable chunks to facilitate easier analysis and querying.
- **WhatsApp Integration:** Communicates with users via WhatsApp, using the Twilio API to handle sending and receiving messages.
- **Customizable Prompt Templates:** Allows for the creation of dynamic response templates tailored to specific user interactions and contexts.
- **Chat History Management:** Maintains context-aware responses by keeping track of user interactions and conversation history.

### 1. Install Required Libraries

Ensure that Python is installed on your machine. Use pip to install the necessary libraries:

    pip install firebase-admin openai langchain flask twilio python-dotenv

- **firebase-admin:** For interacting with Firebase Firestore.
- **openai:** To utilize OpenAI's GPT-3.5-turbo model for natural language processing.
- **langchain:** Provides tools for text splitting, embeddings, and managing AI functions.
- **flask:** To create a web server for handling webhook requests from Twilio.
- **twilio:** Facilitates sending and receiving messages through WhatsApp.
- **python-dotenv:** Loads environment variables from a `.env` file.

### 2. Create a .env File

Create a file named `.env` in the root directory of your project. This file will store sensitive information such as API keys and credentials:

    OPENAI_API_KEY=your_openai_api_key
    TWILIO_ACCOUNT_SID=your_twilio_account_sid
    TWILIO_AUTH_TOKEN=your_twilio_auth_token
    TWILIO_WHATSAPP_NUMBER=your_twilio_whatsapp_number

Replace the placeholders with your actual API keys and credentials.


### 3. Web Scraping, Content Extraction, and Storing in Firestore

A. **Web Scraping and Content Extraction**
   - **`fetch_and_parse_url(url)`** retrieves and parses HTML content into a BeautifulSoup object. **`extract_headings_with_content(soup)`** organizes and extracts headings with their associated content. **`extract_specific_div_content(soup)`** retrieves text from `div` elements with the class `refundPolicy`. **`extract_urls(soup, base_url)`** collects and resolves URLs from anchor tags, and **`format_extracted_content(headings_content, div_content, urls)`** combines and formats this content into a structured output.

B. **Storing Chunks in Firestore**
   - **Initialize Firestore Client and Read Data File:** Sets up the Firestore client with credentials from a JSON file and reads the text data from a file.
   - **Process and Store Text Chunks:** Splits the text data into chunks using `RecursiveCharacterTextSplitter`, embeds them with OpenAI embeddings, and stores them in Firestore. Existing documents in the collection are not re-inserted.
   - **Subsequent Steps:** After storing, the system uses indexing methods to retrieve relevant chunks based on user queries, enabling accurate and contextually appropriate responses.
  
### 4. LawSikhoAssistant Class

A. **Initialization**
   - **Overview:** The `LawSikhoAssistant` class initializes essential components for the chatbot. It loads environment variables, sets up the Firestore client with credentials, initializes OpenAI embeddings, creates a Firestore vector store, and configures a text splitter. Additionally, it initializes a retriever to fetch relevant documents from the Firestore collection based on similarity searches. The class also sets up the language model and defines prompt templates for handling user queries.

B. **Prompt Templates**
   - **Prompt for Query Handling:** 
     ```markdown
     You are the sales executive for LawSikho, a firm providing high-quality legal courses. Your role is to deliver friendly and knowledgeable customer service by answering inquiries about our courses and actively promoting enrollment in our programs. Using the context provided, answer the customer's question accurately and precisely.
     Instructions:
     Highlight the benefits and advantages of our courses based on the user’s needs.
     Engage the user by asking questions about their priorities, goals, and background related to legal education.
     Use bullet points for clarity in longer responses.
     Enhance your response with 1-3 relevant emojis to convey a friendly tone, but avoid overuse.
     Important:
     Craft responses uniquely, avoiding rhetoric or repetitive promotional statements.
     Do not include closing statements that repetitively ask for booking or enrolling.
     Contact details: For more information or immediate assistance, call +91 98186 78383.
     Example Query Handling:
     Context: {context}
     Question: {question}
     ```

   - **Prompt for Condensing Questions:**
     ```markdown
     Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question,
     in its original language.
     Chat History:
     {chat_history}
     Follow Up Input: {question}
     Standalone question:
     ```

C. **Function Descriptions**
   - **`_format_chat_history(chat_history)`**: Converts the chat history into a format suitable for processing, by transforming human and AI messages into `HumanMessage` and `AIMessage` objects.
   
   - **`_search_query()`**: Determines whether there is chat history and processes it accordingly. It condenses follow-up questions into standalone queries and prepares the data for retrieval and response generation.

   - **`_create_chain()`**: Constructs a processing chain that integrates context retrieval, question handling, and response generation. It splits text into manageable chunks, filters them, and uses a prompt template to create responses with the language model.

   - **`query(user_query)`**: Handles user queries by invoking the processing chain with the input data. It manages chat history and returns the chatbot’s response based on the processed input.
  
### 5. Flask Application for Twilio Integration

This Flask application integrates with Twilio to handle and respond to incoming WhatsApp messages using the `LawSikhoAssistant` chatbot.

### Key Components

A. **Initialization**
   - **Flask Setup:** Initializes the Flask app and loads environment variables.
   - **Chatbot Instance:** Creates an instance of `LawSikhoAssistant` to process messages.
   - **Logging Configuration:** Sets up logging for debugging and monitoring.

B. **Message Handling**
   - **Route `/twilio`:** Receives POST requests from Twilio with user messages.
     - **Process:** Extracts the message and sender details, processes the message with the chatbot, and sends a response back through Twilio.
     - **Error Handling:** Logs errors and returns a generic error message if needed.


In summary, this class encapsulates all functionalities required for the LawSikho chatbot, including data initialization, query processing, and response generation.
