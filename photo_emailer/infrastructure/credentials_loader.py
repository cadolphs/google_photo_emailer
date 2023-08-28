import json


class CredentialsLoader:
    def __init__(self, filename):
        self.filename = filename

    @classmethod
    def create(cls, filename):
        return cls(filename)

    @staticmethod
    def create_null(result):
        return CredentialsLoaderStub(result)

    def load_credentials(self):
        with open(self.filename, "r") as f:
            return json.load(f)


class CredentialsLoaderStub:
    def __init__(self, result):
        self.result = result

    def load_credentials(self):
        return self.result
