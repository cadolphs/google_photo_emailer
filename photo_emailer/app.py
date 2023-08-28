from photo_emailer.infrastructure.credentials_loader import CredentialsLoader


class PhotoEmailer:
    def __init__(self, credentials_loader=None):
        if credentials_loader is None:
            self.credentials_loader = CredentialsLoader.create(filename="token.json")
        else:
            self.credentials_loader = credentials_loader

    def run(self):
        return self.credentials_loader.load_credentials()
