from photo_emailer.app import PhotoEmailer
from photo_emailer.logic.credentials import Credentials
from photo_emailer.infrastructure.credentials_loader import CredentialsLoader
from photo_emailer.infrastructure.credentials_refresher import CredentialsRefresher
from photo_emailer.infrastructure.browser_authentication import BrowserAuthClient


def test_app_loads_token_from_file():
    creds = Credentials.get_test_instance()
    loader = CredentialsLoader.create_null(result=creds.to_dict())

    app = PhotoEmailer(credentials_loader=loader)
    app.load_credentials()

    assert app.credentials == creds


def test_app_can_refresh_credentials_if_expired():
    creds = Credentials.get_test_instance()
    creds.expiry = "2022-08-23T21:04:01.984063Z"

    loader = CredentialsLoader.create_null(result=creds.to_dict())
    refresher = CredentialsRefresher.create_null()

    app = PhotoEmailer(credentials_loader=loader, credentials_refresher=refresher)

    app.load_credentials()
    app.refresh_if_needed()

    assert app.credentials.is_expired() is False


def test_app_invokes_browser_flow_if_refresh_fails():
    creds = Credentials.get_test_instance()
    creds.expiry = "2022-08-23T21:04:01.984063Z"

    loader = CredentialsLoader.create_null(result=creds.to_dict())
    refresher = CredentialsRefresher.create_test_instance_that_errors()
    browser_auth_client = BrowserAuthClient.create_null()

    app = PhotoEmailer(
        credentials_loader=loader,
        credentials_refresher=refresher,
        browser_auth_client=browser_auth_client,
    )

    app.load_credentials()
    app.refresh_if_needed()

    assert app.credentials.is_expired() is False
