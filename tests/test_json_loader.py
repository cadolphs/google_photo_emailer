from photo_emailer.infrastructure.credentials_loader import CredentialsIO


def test_loader_loads_json_file_properly():
    filename = "test_token.json"

    expected_credentials = {
        "token": "TOKEN",
        "refresh_token": "REFRESH_TOKEN",
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": "CLIENT_ID",
        "client_secret": "CLIENT_SECRET",
        "scopes": ["https://www.googleapis.com/auth/gmail.send"],
        "expiry": "2022-08-23T21:04:01.984063Z",
    }

    loader = CredentialsIO.create(filename="test_token.json")
    credentials = loader.load_credentials()

    assert expected_credentials == credentials


def test_null_loader():
    expected_credentials = {
        "token": "TOKEN",
        "refresh_token": "REFRESH_TOKEN",
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": "CLIENT_ID",
        "client_secret": "CLIENT_SECRET",
        "scopes": ["https://www.googleapis.com/auth/gmail.send"],
        "expiry": "2022-08-23T21:04:01.984063Z",
    }
