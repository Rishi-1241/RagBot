<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
            background-color: #f4f4f4;
            color: #333;
        }
        h1, h2, h3 {
            color: #007BFF;
            margin-bottom: 20px;
        }
        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        h2 {
            font-size: 2em;
            margin-bottom: 15px;
        }
        p {
            margin-bottom: 15px;
        }
        .code-block {
            background-color: #333;
            color: #fff;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }
        .highlight {
            background-color: #FFD700;
            padding: 2px 5px;
            border-radius: 3px;
            color: #000;
        }
        .section {
            margin-bottom: 30px;
        }
        .link {
            color: #007BFF;
            text-decoration: none;
            font-weight: bold;
        }
        .link:hover {
            text-decoration: underline;
        }
        .contact-info {
            background-color: #f8f9fa;
            padding: 15px;
            border-left: 5px solid #007BFF;
            border-radius: 5px;
        }
        footer {
            margin-top: 30px;
            padding: 10px;
            background-color: #007BFF;
            color: white;
            text-align: center;
            border-radius: 5px;
        }
    </style>
    <title>LawSikhoAssistant Project Documentation</title>
</head>
<body>

    <h1>LawSikhoAssistant Chatbot Project</h1>

    <div class="section">
        <h2>Project Overview</h2>
        <p>
            The <span class="highlight">LawSikhoAssistant</span> is an AI-powered chatbot developed to assist users in exploring and enrolling in legal courses offered by LawSikho. This chatbot integrates with <span class="highlight">Twilio for WhatsApp</span>, allowing seamless communication with users through the WhatsApp platform.
        </p>
        <p>
            The chatbot uses OpenAI's GPT-3.5 model to provide accurate and engaging responses to user queries. It also has a robust mechanism to handle conversation history, retrieve relevant information from a Firestore database, and split lengthy text content into manageable chunks.
        </p>
    </div>

    <div class="section">
        <h2>Key Features</h2>
        <ul>
            <li>AI-powered responses using OpenAI GPT-3.5</li>
            <li>Integration with Twilio API for WhatsApp messaging</li>
            <li>Firestore-based vector store for document retrieval</li>
            <li>Text splitting and chunking for efficient processing</li>
            <li>Customizable prompt templates for tailored user interaction</li>
        </ul>
    </div>

    <div class="section">
        <h2>Project Structure</h2>
        <p>The project is organized into the following key components:</p>
        <ul>
            <li><strong>main.py:</strong> Core logic for the chatbot, including text processing, interaction with Firestore, and OpenAI API calls.</li>
            <li><strong>app.py:</strong> Flask application that handles incoming messages from Twilio, processes them through the chatbot, and sends responses back to WhatsApp.</li>
            <li><strong>utils.py:</strong> Utility functions for text splitting, token counting, and chunk management.</li>
        </ul>
        <p>To keep the code secure and modular, sensitive information such as API keys and credentials are stored in a <span class="highlight">.env</span> file.</p>
    </div>

    <div class="section">
        <h2>Installation and Setup</h2>
        <p>Follow these steps to set up and run the project:</p>
        <ol>
            <li>Clone the repository to your local machine:</li>
            <div class="code-block">git clone https://github.com/yourusername/lawsikhoassistant.git</div>
            <li>Navigate to the project directory:</li>
            <div class="code-block">cd lawsikhoassistant</div>
            <li>Install the required Python packages:</li>
            <div class="code-block">pip install -r requirements.txt</div>
            <li>Create a <span class="highlight">.env</span> file and add your API keys and credentials:</li>
            <div class="code-block">
                OPENAI_API_KEY=your-openai-api-key<br>
                TWILIO_ACCOUNT_SID=your-twilio-account-sid<br>
                TWILIO_AUTH_TOKEN=your-twilio-auth-token<br>
                TWILIO_WHATSAPP_NUMBER=your-twilio-whatsapp-number
            </div>
            <li>Run the Flask application:</li>
            <div class="code-block">python app.py</div>
        </ol>
    </div>

    <div class="section">
        <h2>Usage</h2>
        <p>Once the Flask app is running, the chatbot will be able to respond to WhatsApp messages sent to your Twilio number. Simply send a message, and the chatbot will reply with relevant information or guidance about LawSikho's legal courses.</p>
    </div>

    <div class="section">
        <h2>Web Scraping Source</h2>
        <p>
            The content for this chatbot was sourced from the LawSikho course page: 
            <a href="https://awsikho.com/course/diploma-in-us-corporate-law-and-paralegal-studies" class="link">Diploma in US Corporate Law and Paralegal Studies</a>.
            The data was processed and stored in a Firestore database to facilitate quick and accurate retrieval during chatbot interactions.
        </p>
    </div>

    <div class="section">
        <h2>Contact Information</h2>
        <div class="contact-info">
            <p>For more information or immediate assistance, contact:</p>
            <p><strong>Email:</strong> support@lawsikho.com</p>
            <p><strong>Phone:</strong> +91 98186 78383</p>
        </div>
    </div>

    <footer>
        <p>&copy; 2024 LawSikho. All rights reserved.</p>
    </footer>

</body>
</html>
