from dataclasses import dataclass
from datetime import datetime, timezone, timedelta


@dataclass
class Credentials:
    token: str
    refresh_token: str
    token_uri: str
    client_id: str
    client_secret: str
    scopes: list[str]
    expiry: str

    @classmethod
    def get_test_instance(cls):
        return cls(
            "TESTTOKEN",
            "TESTREFRESHTOKEN",
            "TESTURI",
            "TESTCLIENTID",
            "TESTCLIENTSECRET",
            ["TESTSCOPE"],
            (datetime.now() + timedelta(days=1)).isoformat() + "Z",
        )

    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get("token"),
            data.get("refresh_token"),
            data.get("token_uri"),
            data.get("client_id"),
            data.get("client_secret"),
            data.get("scopes"),
            data.get("expiry"),
        )

    def is_expired(self) -> bool:
        # returns true if expiry is in the past
        return datetime.fromisoformat(self.expiry) <= datetime.now(timezone.utc)
