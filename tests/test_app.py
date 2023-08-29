from photo_emailer.app import PhotoEmailer
from photo_emailer.infrastructure.credentials_loader import CredentialsLoader
from photo_emailer.infrastructure.login_client import LoginClient
from photo_emailer.logic.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials as GoogleCredentials


def test_app_can_perform_login():
    creds = Credentials.get_test_instance()
    creds.expiry = "2022-08-23T21:04:01.984063Z"

    loader = CredentialsLoader.create_null(
        result={
            "token": creds.token,
            "refresh_token": creds.refresh_token,
            "token_uri": creds.token_uri,
            "client_id": creds.client_id,
            "expiry": creds.expiry,
        }
    )

    my_app = PhotoEmailer(
        credentials_loader=loader, login_client=LoginClient.create_null(None, "service")
    )

    my_app.login()
    client = my_app.login_client

    assert isinstance(client, LoginClient)
    assert client.credentials.token == creds.token
    assert client.credentials.is_expired() is False
    assert my_app.service is not None
