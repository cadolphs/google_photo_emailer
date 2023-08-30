from photo_emailer.infrastructure.image_loader import ImageLoader


def test_image_loader():
    loader = ImageLoader.create()
    img = loader.load_image("cat.png")

    with open("cat.png", "rb") as f:
        assert img == f.read()


def test_null_image_loader():
    loader = ImageLoader.create_null(response=b"test")

    assert b"test" == loader.load_image("cat.png")
