from google_auth_oauthlib.flow import InstalledAppFlow
from photo_emailer.logic.credentials import Credentials


class BrowserAuthClient:
    def __init__(self, service):
        self.service = service

    def run_browser_authentication(self):
        return self.service.run_browser_authentication()

    @classmethod
    def create(cls):
        return cls(GoogleBrowserAuthService())

    @classmethod
    def create_null(cls, response=None):
        return cls(NullBrowserAuthService(response))


class GoogleBrowserAuthService:
    def run_browser_authentication(self):
        SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        g_creds = flow.run_local_server(port=0)
        return Credentials(
            token=g_creds.token,
            refresh_token=g_creds.refresh_token,
            token_uri=g_creds.token_uri,
            client_id=g_creds.client_id,
            client_secret=g_creds.client_secret,
            scopes=g_creds.scopes,
            expiry=g_creds.expiry.isoformat() + "Z",
        )


class NullBrowserAuthService:
    def __init__(self, response=None):
        if response is None:
            response = Credentials.get_test_instance()
        self.response = response

    def run_browser_authentication(self):
        return self.response


def run_browser_authentication(self):
    SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    return flow.run_local_server(port=0)
