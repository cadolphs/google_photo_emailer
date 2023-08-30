from photo_emailer.app import PhotoEmailer
from photo_emailer.logic.credentials import Credentials
from photo_emailer.infrastructure.credentials_loader import CredentialsLoader


def test_app_loads_token_from_file():
    creds = Credentials.get_test_instance()
    loader = CredentialsLoader.create_null(result=creds)

    app = PhotoEmailer(credentials_loader=loader)
    loaded_creds = app.load_credentials()

    assert creds == loaded_creds


def test_app_can_refresh_credentials_if_expired():
    creds = Credentials.get_test_instance()
    creds.expiry = "2022-08-23T21:04:01.984063Z"

    loader = CredentialsLoader.create_null(result=creds)

    app = PhotoEmailer(credentials_loader=loader)

    # TODO here we need a credentials refresher
