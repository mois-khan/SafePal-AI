from twilio.rest import Client
import os
from dotenv import load_dotenv
load_dotenv()

# Load these from your .env securely in a real project
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")

client = Client(account_sid, auth_token)

call = client.calls.create(
    to="+918184881001",          # Indian mobile number (use full format)
    from_=os.getenv("TWILIO_PHONE_NUMBER"),        # Your Twilio US number
    url="https://concavely-inflationary-eddy.ngrok-free.dev//twilio-call"  # This endpoint responds with your TwiML and media stream setup
)

print(call.sid)
