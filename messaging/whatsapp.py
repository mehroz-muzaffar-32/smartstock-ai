from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

def send_whatsapp_message(phone_number, reorder_suggestions):
    """
    Send reorder suggestions via WhatsApp using Twilio
    """
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    from_number = os.getenv('TWILIO_WHATSAPP_NUMBER')
    
    if not all([account_sid, auth_token, from_number]):
        raise ValueError("Missing Twilio configuration")
    
    client = Client(account_sid, auth_token)
    
    # Format the message
    message_body = "🛒 Reorder Suggestions:\n"
    for suggestion in reorder_suggestions:
        message_body += f"- {suggestion['name']}: {suggestion['current_quantity']} left → Reorder {suggestion['reorder_quantity']}\n"
    
    message = client.messages.create(
        from_=f'whatsapp:{from_number}',
        body=message_body,
        to=f'whatsapp:+{phone_number}'
    )
    
    return message.sid
