<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LawSikhoAssistant - README</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f4;
            color: #333;
        }
        h1, h2, h3 {
            color: #444;
        }
        code {
            background-color: #eee;
            padding: 2px 4px;
            font-size: 1.1em;
        }
        pre {
            background-color: #eee;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }
        .section {
            margin-bottom: 40px;
        }
        .step {
            margin-bottom: 20px;
        }
    </style>
</head>
<body>

<h1>LawSikhoAssistant - Detailed README</h1>

<div class="section">
    <h2>Description</h2>
    <p><strong>LawSikhoAssistant</strong> is an advanced chatbot designed to interact with users over WhatsApp. It provides information about and promotes legal courses offered by LawSikho. The chatbot integrates with Twilio for WhatsApp communication, Firebase Firestore for storing and retrieving embeddings, and OpenAI's GPT-3.5-turbo for natural language processing. The bot is built with Python, using the Flask web framework for handling webhooks, and various libraries to manage its functionality.</p>
</div>

<div class="section">
    <h2>Features</h2>
    <ul>
        <li><strong>Natural Language Processing (NLP):</strong> Utilizes OpenAI's GPT-3.5-turbo to understand and respond to user queries.</li>
        <li><strong>Database Integration:</strong> Stores and retrieves embeddings from Firebase Firestore for efficient and scalable data management.</li>
        <li><strong>Text Splitting:</strong> Automatically splits large text files into smaller chunks for processing.</li>
        <li><strong>WhatsApp Integration:</strong> Communicates with users through WhatsApp, leveraging the Twilio API.</li>
        <li><strong>Customizable Prompt Templates:</strong> Templates for generating responses tailored to the context of user queries.</li>
        <li><strong>Chat History Management:</strong> Keeps track of user interactions to provide context-aware responses.</li>
    </ul>
</div>

<div class="section">
    <h2>Step-by-Step Setup Guide</h2>

    <div class="step">
        <h3>1. Install Required Libraries</h3>
        <p>Ensure that you have Python installed, and then install the necessary libraries using pip:</p>
        <pre><code>pip install firebase-admin openai langchain flask twilio python-dotenv</code></pre>
        <p>These libraries are used as follows:</p>
        <ul>
            <li><strong>firebase-admin:</strong> To interact with Firebase Firestore.</li>
            <li><strong>openai:</strong> To access OpenAI's GPT-3.5-turbo for natural language processing.</li>
            <li><strong>langchain:</strong> For managing text splitting, embeddings, and other AI-related functions.</li>
            <li><strong>flask:</strong> To create a web server that handles incoming webhook requests from Twilio.</li>
            <li><strong>twilio:</strong> For sending and receiving messages via WhatsApp.</li>
            <li><strong>python-dotenv:</strong> To load environment variables from a .env file.</li>
        </ul>
    </div>

    <div class="step">
        <h3>2. Create a .env File</h3>
        <p>Create a file named <code>.env</code> in the root directory of your project. This file should contain the following environment variables:</p>
        <pre><code>OPENAI_API_KEY=your_openai_api_key
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=your_twilio_whatsapp_number</code></pre>
        <p>Replace the placeholders with your actual API keys and credentials.</p>
    </div>

    <div class="step">
        <h3>3. Initialize Firebase Firestore</h3>
        <p>Ensure that you have a Firebase project set up. Download the service account key JSON file and place it in your project directory.</p>
        <p>In your Python code, initialize Firebase Firestore as follows:</p>
        <ul>
            <li><strong>Function:</strong> <code>_initialize_firestore()</code></li>
            <li><strong>Purpose:</strong> Initializes the Firebase Firestore client using credentials stored in the <code>package.json</code> file. This allows the bot to store and retrieve embeddings.</li>
        </ul>
    </div>

    <div class="step">
        <h3>4. Initialize OpenAI Embeddings</h3>
        <p>Set up the OpenAI embeddings model using the API key:</p>
        <ul>
            <li><strong>Function:</strong> <code>_initialize_embeddings()</code></li>
            <li><strong>Purpose:</strong> This model is used to convert text into vector representations for similarity searches.</li>
        </ul>
    </div>

    <div class="step">
        <h3>5. Set Up Vector Store</h3>
        <p>Initialize the Firestore Vector Store where document embeddings are stored and retrieved for query processing:</p>
        <ul>
            <li><strong>Function:</strong> <code>_initialize_vectorstore()</code></li>
            <li><strong>Purpose:</strong> Stores and retrieves embeddings to facilitate quick and efficient searches.</li>
        </ul>
    </div>

    <div class="step">
        <h3>6. Split Large Text Files</h3>
        <p>To handle large text files, configure the text splitter to divide them into smaller chunks:</p>
        <ul>
            <li><strong>Function:</strong> <code>_initialize_text_splitter()</code></li>
            <li><strong>Purpose:</strong> Automatically splits large text files into manageable chunks for processing.</li>
        </ul>
    </div>

    <div class="step">
        <h3>7. Configure the Flask App</h3>
        <p>Set up the Flask app to handle incoming messages from Twilio:</p>
        <ul>
            <li><strong>Function:</strong> <code>app.route('/twilio', methods=['POST'])</code></li>
            <li><strong>Purpose:</strong> Defines a webhook endpoint that receives incoming messages, processes them with the chatbot, and sends back a response via Twilio.</li>
        </ul>
    </div>

    <div class="step">
        <h3>8. Running the Flask App</h3>
        <p>To start the Flask server, run the following command in your terminal:</p>
        <pre><code>python app.py</code></pre>
        <p>This will start the Flask application on the specified port, allowing it to handle incoming requests from Twilio.</p>
    </div>

    <div class="step">
        <h3>9. Querying the Chatbot</h3>
        <p>Interact with the chatbot via WhatsApp by sending messages to the number associated with your Twilio account. The chatbot will process your query and respond accordingly.</p>
        <ul>
            <li><strong>Function:</strong> <code>query()</code></li>
            <li><strong>Purpose:</strong> Processes user queries, retrieves relevant information from the vector store, and generates a response using the GPT-3.5-turbo model.</li>
        </ul>
    </div>
</div>

<div class="section">
    <h2>Append WhatsApp Chat Screenshots</h2>
    <p>To provide visual examples of the chatbot in action, append screenshots of your WhatsApp chats with the chatbot here. Ensure that the screenshots clearly demonstrate the functionality and responses generated by the bot.</p>
</div>

</body>
</html>
