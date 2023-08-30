import json
from photo_emailer.utils.events import OutputListener, OutputTracker


class CredentialsIO:
    def __init__(self, filename):
        self.filename = filename
        self._listener = OutputListener()

    def track_output(self):
        return self._listener.create_tracker()

    @classmethod
    def create(cls, filename):
        return cls(filename)

    @staticmethod
    def create_null(result):
        return CredentialsIOStub(result)

    def load_credentials(self):
        with open(self.filename, "r") as f:
            return json.load(f)

    def store_credentials(self, credentials):
        with open(self.filename, "w") as f:
            json.dump(credentials, f)


class CredentialsIOStub(CredentialsIO):
    def __init__(self, result):
        super().__init__(None)
        self.result = result

    def load_credentials(self):
        return self.result

    def store_credentials(self, credentials):
        self._listener.track(
            data={"action": "store_credentials", "credentials": credentials}
        )
