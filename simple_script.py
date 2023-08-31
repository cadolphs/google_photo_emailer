import sys

from photo_emailer.app import PhotoEmailer

if __name__ == "__main__":
    app = PhotoEmailer(image_directory=sys.argv[2])
    app.load_credentials()
    app.refresh_if_needed()
    app.store_credentials()

    app.send_email(sys.argv[1])
