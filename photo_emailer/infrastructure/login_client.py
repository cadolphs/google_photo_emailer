from google.oauth2.credentials import Credentials


class LoginClient:
    def __init__(self, credential_loader=None):
        self.credential_loader = credential_loader

    @classmethod
    def create(cls):
        return cls(CredentialFileLoader.create())

    @classmethod
    def create_null(cls, credential_response=None):
        client = cls(CredentialFileLoader.create_null(credential_response))
        return client

    def get_credentials(self):
        stored_creds = self.credential_loader.load_credentials()
        if stored_creds and stored_creds.expired and stored_creds.refresh_token:
            print("Refreshing expired credentials...")
            stored_creds.refresh(Request())
            self.store_credentials(stored_creds)
            return stored_creds
        elif not stored_creds.expired:
            print("Reusing stored credentials...")
            return stored_creds
        else:
            raise NotImplementedError(
                "Cannot handle absent or invalid credentiaks right now"
            )


class CredentialFileLoader:
    def __init__(self, credentials_file):
        self.credentials_file = credentials_file

    def load_credentials(self):
        return Credentials.from_authorized_user_file(self.credentials_file)

    @classmethod
    def create(cls, credentials_file="token.json"):
        return cls(credentials_file)

    @classmethod
    def create_null(cls, credential_response=None):
        loader = cls("")
        loader.load_credentials = lambda: credential_response
        return loader
