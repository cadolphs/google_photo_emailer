from dataclasses import dataclass


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
            "TESTEXPIRY",
        )

    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get("TOKEN"),
            data.get("REFRESH_TOKEN"),
            data.get("TOKEN_URI"),
            data.get("CLIENT_ID"),
            data.get("CLIENT_SECRET"),
            data.get("SCOPES"),
            data.get("EXPIRY"),
        )
