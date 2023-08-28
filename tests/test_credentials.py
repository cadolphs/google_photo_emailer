from photo_emailer.logic.credentials import Credentials
from datetime import datetime, timedelta


def test_credentials_from_dict():
    credentials = Credentials.from_dict({"token": "FOO"})

    assert credentials.token == "FOO"


def test_credentials_know_when_they_are_expired():
    expired_credentials = {
        "token": "TOKEN",
        "refresh_token": "REFRESH_TOKEN",
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": "CLIENT_ID",
        "client_secret": "CLIENT_SECRET",
        "scopes": ["https://www.googleapis.com/auth/gmail.send"],
        "expiry": "2022-08-23T21:04:01.984063Z",
    }

    creds = Credentials.from_dict(expired_credentials)

    assert creds.is_expired() is True

    nonexpired_credentials = expired_credentials.copy()

    # call date util to get todays date and add 1 day

    nonexpired_credentials["expiry"] = get_tomorrows_date_string()
    creds = Credentials.from_dict(nonexpired_credentials)
    assert creds.is_expired() is False


def get_tomorrows_date_string() -> str:
    return (datetime.now() + timedelta(days=1)).isoformat() + "Z"
