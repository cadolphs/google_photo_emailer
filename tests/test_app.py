from photo_emailer.app import PhotoEmailer
from photo_emailer.infrastructure.credentials_loader import CredentialsLoader
from photo_emailer.logic.credentials import Credentials


# Simplest App seed
def test_app_loads_credentials_from_file():
    loader = CredentialsLoader.create_null(result={"TOKEN": "TESTTOKEN"})
    my_app = PhotoEmailer(credentials_loader=loader)

    credentials = my_app.run()

    expected_credentials = Credentials.from_dict({"TOKEN": "TESTTOKEN"})

    assert expected_credentials == credentials
