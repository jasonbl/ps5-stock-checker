import os

from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
toNum = os.getenv('TWILIO_TO_NUM')
fromNum = os.getenv('TWILIO_FROM_NUM')

client = Client(account_sid, auth_token)

def sendInStockText(seller_name, seller_url):
    client.messages.create(
        to=toNum,
        from_=fromNum,
        body="PS5 in stock at " + seller_name + "! Purchase here: " + seller_url,
    )
