from photo_emailer.logic.credentials import Credentials


def test_credentials_from_dict():
    credentials = Credentials.from_dict({"TOKEN": "FOO"})

    assert credentials.token == "FOO"
