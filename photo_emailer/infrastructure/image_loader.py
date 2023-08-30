class ImageLoader:
    @classmethod
    def create(cls):
        return cls()

    @classmethod
    def create_null(cls, response=None):
        loader = cls()

        def null_load_image(filename):
            return response

        loader.load_image = null_load_image
        return loader

    def load_image(self, filename):
        with open(filename, "rb") as f:
            return f.read()
