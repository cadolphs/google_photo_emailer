from photo_emailer.app import PhotoEmailer
from photo_emailer.infrastructure.credentials_loader import CredentialsLoader
from photo_emailer.logic.credentials import Credentials
from googleapiclient.discovery import build


# Simplest App seed
def test_app_loads_credentials_from_file():
    loader = CredentialsLoader.create_null(result={"token": "TESTTOKEN"})
    my_app = PhotoEmailer(credentials_loader=loader)

    credentials = my_app.run()

    expected_credentials = Credentials.from_dict({"token": "TESTTOKEN"})

    assert expected_credentials == credentials


def test_authentication_spike():
    loader = CredentialsLoader.create(filename="token.json")
    creds = loader.load_credentials()

    credentials = Credentials.from_dict(creds)

    # this doesn't work, because our credentials class is a pure logic class
    # service = build("gmail", "v1", credentials=credentials)
