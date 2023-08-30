import sys

from photo_emailer.app import PhotoEmailer

if __name__ == "__main__":
    app = PhotoEmailer()
    app.load_credentials()
    app.refresh_if_needed()
    app.store_credentials()
