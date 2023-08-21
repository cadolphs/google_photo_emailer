import json

import sys

from photo_emailer.email_client import EmailClient

client = EmailClient.create_null()
client.authenticate()
client.send_email(to="clemens.adolphs+test@gmail.com", subject="test", body="Hello!")

sys.exit(0)

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
creds = flow.run_local_server(port=0)
with open("stored_credentials.json", "w") as json_file:
    json.dump(creds, json_file)

store_creds(json, "stored_credentials.json")

# store the auth token for later use

service = build("gmail", "v1", credentials=creds)
message = MIMEText("This is the body of the email")
message["to"] = "clemensadolphs+test@gmail.com"
message["subject"] = "Email Subject"
create_message = {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}

try:
    message = (
        service.users().messages().send(userId="me", body=create_message).execute()
    )
    print(f'sent message to {message} Message Id: {message["id"]}')
except HTTPError as error:
    print(f"An error occurred: {error}")
    message = None
