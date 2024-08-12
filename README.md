# LawSikhoAssistant - Detailed README

## Description

**LawSikhoAssistant** is an advanced chatbot designed to interact with users over WhatsApp. It provides information about and promotes legal courses offered by LawSikho. The chatbot integrates with Twilio for WhatsApp communication, Firebase Firestore for storing and retrieving embeddings, and OpenAI's GPT-3.5-turbo for natural language processing. The bot is built with Python, using the Flask web framework for handling webhooks, and various libraries to manage its functionality.

## Features

- **Natural Language Processing (NLP):** Utilizes OpenAI's GPT-3.5-turbo to understand and respond to user queries.
- **Database Integration:** Stores and retrieves embeddings from Firebase Firestore for efficient and scalable data management.
- **Text Splitting:** Automatically splits large text files into smaller chunks for processing.
- **WhatsApp Integration:** Communicates with users through WhatsApp, leveraging the Twilio API.
- **Customizable Prompt Templates:** Templates for generating responses tailored to the context of user queries.
- **Chat History Management:** Keeps track of user interactions to provide context-aware responses.

## Step-by-Step Setup Guide

### 1. Install Required Libraries

Ensure that you have Python installed, and then install the necessary libraries using pip:

```bash
pip install firebase-admin openai langchain flask twilio python-dotenv
