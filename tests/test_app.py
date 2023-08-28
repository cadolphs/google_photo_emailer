from photo_emailer.app import PhotoEmailer
from photo_emailer.infrastructure.credentials_loader import CredentialsLoader


# Simplest App seed
def test_app_loads_credentials_from_file():
    loader = CredentialsLoader.create_null(result={"TOKEN": "TESTTOKEN"})
    my_app = PhotoEmailer(credentials_loader=loader)

    credentials = my_app.run()

    expected_credentials = {"TOKEN": "TESTTOKEN"}

    assert expected_credentials == credentials
