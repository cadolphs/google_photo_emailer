from photo_emailer.app import PhotoEmailer
from photo_emailer.infrastructure.credentials_loader import CredentialsLoader
from photo_emailer.logic.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials as GoogleCredentials


# Simplest App seed
def test_app_loads_credentials_from_file():
    loader = CredentialsLoader.create_null(result={"token": "TESTTOKEN"})
    my_app = PhotoEmailer(credentials_loader=loader)

    credentials = my_app.run()

    assert credentials.token == "TESTTOKEN"
    assert credentials.refresh_token is None
