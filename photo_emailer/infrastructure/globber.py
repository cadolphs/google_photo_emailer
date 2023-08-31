from glob import glob


class Globber:
    @classmethod
    def create(cls):
        return cls()

    @classmethod
    def create_null(cls, files=None, extensions=None):
        globber = cls()

        def null_glob(path):
            return [f"{path}/{file}" for file in files]

        globber.glob = null_glob
        return globber

    def glob(self, path):
        return glob(f"{path}/*.jpg")
