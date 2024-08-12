# LawSikhoAssistant - Detailed README

## Description

**LawSikhoAssistant** is an advanced AI-powered chatbot designed to interact with users over WhatsApp. It provides users with comprehensive information about legal courses offered by LawSikho, helping them make informed decisions about their legal education. The chatbot leverages state-of-the-art technologies to facilitate smooth communication, efficient data management, and accurate responses. 

## Features

- **Natural Language Processing (NLP):** Utilizes OpenAI's GPT-3.5-turbo model to understand and generate human-like responses based on user queries.
- **Database Integration:** Uses Firebase Firestore to store and retrieve document embeddings, enabling scalable and efficient data management.
- **Text Splitting:** Automatically processes large text files by splitting them into smaller, manageable chunks to facilitate easier analysis and querying.
- **WhatsApp Integration:** Communicates with users via WhatsApp, using the Twilio API to handle sending and receiving messages.
- **Customizable Prompt Templates:** Allows for the creation of dynamic response templates tailored to specific user interactions and contexts.
- **Chat History Management:** Maintains context-aware responses by keeping track of user interactions and conversation history.

## Step-by-Step Setup Guide

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

### 3. Initialize Firebase Firestore

- **Firebase Setup:** Set up a Firebase project through the [Firebase Console](https://console.firebase.google.com/). Download the service account key JSON file and place it in your project directory.
- **Python Code Initialization:**

    ```python
    import firebase_admin
    from firebase_admin import credentials, firestore

    def _initialize_firestore():
        cred = credentials.Certificate('path_to_your_service_account_key.json')
        firebase_admin.initialize_app(cred)
        return firestore.client()
    ```

- **Purpose:** Initializes the Firebase Firestore client, allowing the chatbot to store and retrieve document embeddings.

### 4. Initialize OpenAI Embeddings

- **API Key Setup:** Use the API key from OpenAI to set up the embeddings model.
- **Python Code Initialization:**

    ```python
    import openai

    def _initialize_embeddings():
        openai.api_key = os.getenv("OPENAI_API_KEY")
        # Example usage for embeddings
        return openai.Embedding.create(model="text-embedding-ada-002", input="sample text")
    ```

- **Purpose:** Converts text into vector representations for efficient similarity searches.

### 5. Set Up Vector Store

- **Firestore Vector Store Setup:** Configure Firestore to store and retrieve document embeddings.
- **Python Code Initialization:**

    ```python
    def _initialize_vectorstore():
        db = _initialize_firestore()
        # Set up vector store (example)
        return db.collection('vectorstore')
    ```

- **Purpose:** Facilitates quick and efficient searches by storing and retrieving document embeddings.

### 6. Split Large Text Files

- **Text Splitting Configuration:** Implement text splitting to manage large text files.
- **Python Code Initialization:**

    ```python
    from langchain.text_splitter import CharacterTextSplitter

    def _initialize_text_splitter():
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        return text_splitter
    ```

- **Purpose:** Handles large text files by splitting them into manageable chunks for processing.

### 7. Configure the Flask App

- **Flask App Setup:** Create a Flask application to handle incoming messages from Twilio.
- **Python Code Example:**

    ```python
    from flask import Flask, request, jsonify
    from twilio.rest import Client
    import os

    app = Flask(__name__)

    @app.route('/twilio', methods=['POST'])
    def handle_twilio_message():
        # Process incoming message and respond
        incoming_message = request.form['Body']
        from_number = request.form['From']
        response_message = query(incoming_message)
        client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
        client.messages.create(
            body=response_message,
            from_=os.getenv('TWILIO_WHATSAPP_NUMBER'),
            to=from_number
        )
        return jsonify({'status': 'success'})

    def query(message):
        # Example query processing
        return "Your response here"
    ```

- **Purpose:** Defines an endpoint to handle incoming messages from Twilio, processes them with the chatbot, and sends responses.

### 8. Running the Flask App

- **Start Flask Server:** Use the following command to run the Flask application:

    ```bash
    python app.py
    ```

- **Purpose:** Starts the Flask application on the specified port to handle incoming webhook requests from Twilio.

### 9. Querying the Chatbot

- **Interaction:** Users can send messages to the WhatsApp number associated with your Twilio account.
- **Python Code Example:**

    ```python
    def query(message):
        # Implement message processing and response generation
        # Example: use OpenAI's GPT-3.5-turbo to generate a response
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=message,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    ```

- **Purpose:** Processes user queries, retrieves relevant information from the vector store, and generates a response using the GPT-3.5-turbo model.

## Append WhatsApp Chat Screenshots

To provide visual examples of the chatbot in action, append screenshots of your WhatsApp chats with the chatbot here. Ensure that the screenshots clearly demonstrate the functionality and responses generated by the bot.

---

This README provides a comprehensive guide for setting up and using the LawSikhoAssistant chatbot. Ensure you follow each step carefully to successfully deploy and interact with the chatbot.
