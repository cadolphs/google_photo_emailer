import json

import sys

from photo_emailer.email_client import EmailClient, AuthClient

auth_client = AuthClient.create()
creds = auth_client.get_credentials()

client = EmailClient.create(credentials=creds)
client.send_email(to="clemens.adolphs+test@gmail.com", subject="test", body="Hello!")

sys.exit(0)
