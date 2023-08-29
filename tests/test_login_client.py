from photo_emailer.infrastructure.login_client import (
    GoogleCredentialsStub,
    GoogleCredentials,
    GoogleCredentialBuilder,
    LoginClient,
    get_tomorrows_date_string,
)
from photo_emailer.logic.credentials import Credentials


def test_google_credentials_stub_refreshes_token():
    expired_credentials = Credentials.get_test_instance()
    expired_credentials.expiry = "2022-08-23T21:04:01.984063Z"

    assert expired_credentials.is_expired() is True

    stub_credentials = GoogleCredentialBuilder.create_null().make_google_credentials(
        credentials=expired_credentials
    )

    stub_credentials.refresh(None)

    new_credentials = GoogleCredentialBuilder.create_null().make_logic_credentials(
        credentials=stub_credentials
    )

    assert new_credentials.is_expired() is False


def test_login_client_refreshes_if_needed():
    expired_credentials = Credentials.get_test_instance()
    expired_credentials.expiry = "2022-08-23T21:04:01.984063Z"

    assert expired_credentials.is_expired() is True

    login_client = LoginClient.create_null(
        credentials=expired_credentials,
    )

    login_client.refresh_if_needed()

    assert login_client.credentials.is_expired() is False


def test_login_client_leaves_alone_if_not_expired():
    nonexpired_credentials = Credentials.get_test_instance()
    nonexpired_credentials.expiry = get_tomorrows_date_string()

    assert nonexpired_credentials.is_expired() is False

    login_client = LoginClient.create_null(
        credentials=nonexpired_credentials,
    )

    login_client.refresh_if_needed()

    assert login_client.credentials == nonexpired_credentials


def test_google_credential_builder():
    # Simple translation class so tests should be simple
    builder = GoogleCredentialBuilder.create()
    credentials = Credentials.get_test_instance()

    google_credentials = builder.make_google_credentials(credentials)

    assert isinstance(google_credentials, GoogleCredentials)
    assert google_credentials.token == credentials.token
    assert google_credentials.refresh_token == credentials.refresh_token
    assert google_credentials.token_uri == credentials.token_uri
    assert google_credentials.client_id == credentials.client_id
    assert google_credentials.client_secret == credentials.client_secret
    assert google_credentials.scopes == credentials.scopes
    assert google_credentials.expiry == credentials.expiry


def test_login_service_provides_builder_with_valid_credentials():
    expired_credentials = Credentials.get_test_instance()
    expired_credentials.expiry = "2022-08-23T21:04:01.984063Z"

    login_client = LoginClient.create_null(
        credentials=expired_credentials, builder_response="HELLO"
    )

    output_tracker = login_client.track_output()
    assert login_client.login() == "HELLO"

    data = output_tracker.data
    assert data[0]["action"] == "login"
    assert data[0]["credentials"].is_expired() is False
