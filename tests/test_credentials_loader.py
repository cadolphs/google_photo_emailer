from photo_emailer.infrastructure.credentials_io import CredentialsIO
from pathlib import Path


# focused integration test for the loader
def test_credentials_loder_loads_json_from_file():
    expected = {
        "token": "TOKEN",
        "refresh_token": "REFRESH_TOKEN",
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": "CLIENT_ID",
        "client_secret": "CLIENT_SECRET",
        "scopes": ["https://www.googleapis.com/auth/gmail.send"],
        "expiry": "2022-08-23T21:04:01.984063Z",
    }

    loader = CredentialsIO.create("test_token.json")

    result = loader.load_credentials()

    assert result == expected


def test_credentials_loader_can_store_json_to_file(tmp_path):
    creds = {
        "token": "TESTTOKEN",
        "refresh_token": "REFRESH_TOKEN",
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": "CLIENT_ID",
        "client_secret": "CLIENT_SECRET",
        "scopes": ["https://www.googleapis.com/auth/gmail.send"],
        "expiry": "2022-08-23T21:04:01.984063Z",
    }

    loader = CredentialsIO.create(str(tmp_path / "test_token.json"))
    loader.store_credentials(creds)

    assert Path.exists(tmp_path / "test_token.json")

    loaded_creds = loader.load_credentials()

    assert creds == loaded_creds


def test_credentials_stub_writing():
    loader = CredentialsIO.create_null(None)
    output = loader.track_output()

    loader.store_credentials({"token": "FOO"})

    assert output.data[0] == {
        "action": "store_credentials",
        "credentials": {"token": "FOO"},
    }
