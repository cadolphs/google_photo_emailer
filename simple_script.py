import sys

from photo_emailer.app import PhotoEmailer

if __name__ == "__main__":
    app = PhotoEmailer()
    app.login()
