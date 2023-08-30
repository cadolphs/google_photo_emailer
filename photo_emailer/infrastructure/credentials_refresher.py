from photo_emailer.utils.datestuff import get_tomorrows_date_string
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials as GoogleCredentials
from google.auth.transport.requests import Request
from photo_emailer.logic.credentials import Credentials


class CredentialsRefresher:
    @classmethod
    def create(cls):
        return cls()

    @classmethod
    def create_null(cls):
        refresher = cls()

        def nulled_refresh(creds):
            creds.expiry = get_tomorrows_date_string()
            return creds

        refresher.refresh = nulled_refresh
        return refresher

    @classmethod
    def create_test_instance_that_errors(cls):
        refresher = cls()

        def nulled_refresh(credentials):
            raise RefreshError("Could not refresh credentials")

        refresher.refresh = nulled_refresh
        return refresher

    def refresh(self, creds):
        g_creds = GoogleCredentials(
            token=creds.token,
            refresh_token=creds.refresh_token,
            token_uri=creds.token_uri,
            client_id=creds.client_id,
            client_secret=creds.client_secret,
            scopes=creds.scopes,
            expiry=creds.expiry,
        )
        g_creds.refresh(Request())
        return Credentials(
            token=g_creds.token,
            refresh_token=g_creds.refresh_token,
            token_uri=g_creds.token_uri,
            client_id=g_creds.client_id,
            client_secret=g_creds.client_secret,
            scopes=g_creds.scopes,
            expiry=g_creds.expiry.isoformat() + "Z",
        )
