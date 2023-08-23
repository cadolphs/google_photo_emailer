from photo_emailer.app import PhotoEmailer


# Simplest App seed
def test_app_retrieves_credentials():
    my_app = PhotoEmailer()
    credentials = my_app.run()

    expected_credentials = {"token": "TOKEN"}

    assert expected_credentials == credentials
