from photo_emailer.logic.credentials import Credentials
from google.oauth2.credentials import Credentials as GoogleCredentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from datetime import datetime, timedelta, timezone
from photo_emailer.utils.events import OutputListener, OutputTracker
from photo_emailer.infrastructure.email_sender import NullEmailService


class LoginClient:
    def __init__(
        self,
        credentials: Credentials,
        credential_builder=None,
        service_builder=None,
    ):
        self.credentials = credentials
        self.credential_builder = credential_builder
        self.service_builder = service_builder
        self._listener = OutputListener()

    @classmethod
    def create(cls, credentials):
        credential_builder = GoogleCredentialBuilder.create()
        return cls(credentials, credential_builder)

    @classmethod
    def create_null(cls, credentials, builder_response=None):
        if builder_response is None:
            builder_response = NullEmailService()

        credential_builder = GoogleCredentialBuilder.create_null()
        service_builder = ServiceBuilder.create_null(builder_response)
        return cls(credentials, credential_builder, service_builder)

    def login(self):
        self.refresh_if_needed()
        creds = self.credential_builder.make_google_credentials(self.credentials)

        service = self.service_builder.build("gmail", "v1", credentials=creds)
        self._listener.track(data={"action": "login", "credentials": creds})
        return service

    def refresh_if_needed(self):
        if self.credentials.is_expired():
            creds = self.credential_builder.make_google_credentials(self.credentials)
            creds.refresh(Request())
            self.credentials = self.credential_builder.make_logic_credentials(creds)

    def track_output(self):
        return self._listener.create_tracker()


class GoogleCredentialBuilder:
    def __init__(self, google_credentials_factory=GoogleCredentials):
        self.google_credentials_factory = google_credentials_factory

    @classmethod
    def create(cls):
        return cls(GoogleCredentials)

    @classmethod
    def create_null(cls):
        return cls(GoogleCredentialsStub)

    def make_google_credentials(self, credentials: Credentials):
        return self.google_credentials_factory(
            token=credentials.token,
            refresh_token=credentials.refresh_token,
            token_uri=credentials.token_uri,
            client_id=credentials.client_id,
            client_secret=credentials.client_secret,
            scopes=credentials.scopes,
            expiry=credentials.expiry,
        )

    def make_logic_credentials(self, credentials):
        return Credentials(
            token=credentials.token,
            refresh_token=credentials.refresh_token,
            token_uri=credentials.token_uri,
            client_id=credentials.client_id,
            client_secret=credentials.client_secret,
            scopes=credentials.scopes,
            expiry=credentials.expiry,
        )


class GoogleCredentialsStub:
    def __init__(
        self,
        token,
        refresh_token,
        token_uri,
        client_id,
        client_secret,
        scopes,
        expiry,
    ):
        self.token = token
        self.refresh_token = refresh_token
        self.token_uri = token_uri
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes
        self.expiry = expiry

    def refresh(self, request):
        self.expiry = get_tomorrows_date_string()

    def is_expired(self):
        return datetime.fromisoformat(self.expiry) <= datetime.now(timezone.utc)


def get_tomorrows_date_string() -> str:
    return (datetime.now() + timedelta(days=1)).isoformat() + "Z"


class ServiceBuilder:
    def __init__(self, service_builder):
        self.service_builder = service_builder

    @classmethod
    def create(cls):
        return cls(build)

    @classmethod
    def create_null(cls, response=None):
        return cls(ServiceBuildStub(response))

    def build(self, service_name, version, credentials):
        return self.service_builder(service_name, version, credentials=credentials)


class ServiceBuildStub:
    def __init__(self, response):
        self.response = response
        self.last_args = None

    def __call__(self, service_name, version, credentials):
        self.last_args = {
            "service_name": service_name,
            "version": version,
            "credentials": credentials,
        }
        return self.response
