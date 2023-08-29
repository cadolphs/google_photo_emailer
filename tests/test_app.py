from photo_emailer.app import PhotoEmailer
from photo_emailer.infrastructure.credentials_loader import CredentialsLoader
from photo_emailer.infrastructure.email_sender import EmailSender
from photo_emailer.infrastructure.login_client import LoginClient
from photo_emailer.logic.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials as GoogleCredentials


def test_app_steps():
    creds = Credentials.get_test_instance()

    loader = CredentialsLoader.create_null(
        result={
            "token": creds.token,
            "refresh_token": creds.refresh_token,
            "token_uri": creds.token_uri,
            "client_id": creds.client_id,
            "expiry": creds.expiry,
        }
    )

    sender = EmailSender.create_null()
    output_tracker = sender.track_output()

    my_app = PhotoEmailer(
        credentials_loader=loader,
        login_client=LoginClient.create_null(None),
        email_sender=sender,
    )

    my_app.login()
    my_app.send_email(subject="foo", message="bar")

    data = output_tracker.data[0]

    assert data["action"] == "send_email"
