from google.oauth2.credentials import Credentials


class LoginClient:
    @classmethod
    def create(cls):
        return cls()

    def get_credentials(self):
        stored_creds = self._load_credentials("token.json")
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

    def _load_credentials(self, json):
        return Credentials.from_authorized_user_file(json)
