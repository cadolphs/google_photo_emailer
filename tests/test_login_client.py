from photo_emailer.infrastructure.login_client import LoginClient


def test_login_client_loads_and_refreshes_valid_credentials():
    client = LoginClient.create()
    credentials = client.get_credentials()

    assert credentials and not credentials.expired
