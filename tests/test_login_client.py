from photo_emailer.infrastructure.login_client import LoginClient, CredentialFileLoader
from google.oauth2.credentials import Credentials


def test_login_client_loads_and_refreshes_valid_credentials():
    client = LoginClient.create()
    credentials = client.get_credentials()

    assert credentials and not credentials.expired


def test_null_client():
    client = LoginClient.create_null(credential_response=Credentials(token="FOOBAR"))
    credentials = client.get_credentials()
    assert credentials.token == "FOOBAR"


def test_file_loader_loads_right_file():
    loader = CredentialFileLoader.create(credentials_file="test_token.json")
    credentials = loader.load_credentials()

    assert credentials.token == "TOKEN"
    assert credentials.refresh_token == "REFRESH_TOKEN"
    assert credentials.expired
