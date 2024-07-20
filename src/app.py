from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv
from main import LawSikhoAssistant  # Adjust import as necessary
import logging

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize the LawSikhoAssistant
assistant = LawSikhoAssistant()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/twilio', methods=['POST'])
def webhook():
    try:
        incoming_msg = request.values.get('Body', '').strip()
        from_number = request.values.get('From', '').strip()

        logging.debug(f"Incoming message: {incoming_msg} from {from_number}")

        # Process the incoming message with the chatbot
        response_text = assistant.query(incoming_msg)

        # Create a Twilio response
        resp = MessagingResponse()
        resp.message(response_text)

        logging.debug(f"Response message: {response_text}")

        return str(resp)
    except Exception as e:
        logging.error(f"Error: {e}")
        return str(MessagingResponse().message("Sorry, there was an error processing your request.")), 500

if __name__ == '__main__':
    app.run(port=8000, debug=True)
