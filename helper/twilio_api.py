from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve Twilio credentials from environment variables
account_sid = os.getenv('TWILIO_SID')
auth_token = os.getenv('TWILIO_TOKEN')
from_number = os.getenv('FROM')

# Initialize the Twilio client
client = Client(account_sid, auth_token)

def send_text_message(to: str, message: str) -> None:
    try:
        message = client.messages.create(
            from_=from_number,
            body=message,
            to=to
        )
        print(f"Message sent successfully! {message.sid}")
    except Exception as e:
        print(f"Error sending message: {str(e)}")

# Example usage
to_number = 'whatsapp:+916232158146'
text_message = 'Hello, this is a test message from Twilio!'

send_text_message(to_number, text_message)


print("cexecuted successfully!")