from photo_emailer.infrastructure.image_processor import ImageProcessor
from photo_emailer.infrastructure.image_loader import ImageLoader
from photo_emailer.infrastructure.file_saver import FileSaver
from PIL import Image
import io


def create_test_image(width=100, height=100):
    """Helper to create test image bytes."""
    img = Image.new('RGB', (width, height), color='red')
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    return buffer.getvalue()


def test_get_image_dimensions_from_bytes():
    processor = ImageProcessor.create_null()
    test_bytes = create_test_image(200, 150)

    width, height = processor.get_image_dimensions_from_bytes(test_bytes)

    assert width == 200
    assert height == 150


def test_get_image_dimensions_from_file():
    test_bytes = create_test_image(300, 200)
    loader = ImageLoader.create_null(response=test_bytes)
    processor = ImageProcessor(image_loader=loader, file_saver=FileSaver.create_null())

    width, height = processor.get_image_dimensions_from_file("test.jpg")

    assert width == 300
    assert height == 200


def test_resize_image_bytes():
    processor = ImageProcessor.create_null()
    test_bytes = create_test_image(400, 300)

    resized_bytes = processor.resize_image_bytes(test_bytes, 200, 150, quality=85)

    # Check that we got bytes back
    assert isinstance(resized_bytes, bytes)
    assert len(resized_bytes) > 0

    # Verify the dimensions of the resized image
    with Image.open(io.BytesIO(resized_bytes)) as img:
        assert img.size == (200, 150)


def test_resize_and_save():
    test_bytes = create_test_image(400, 300)
    loader = ImageLoader.create_null(response=test_bytes)
    saver = FileSaver.create_null()
    processor = ImageProcessor(image_loader=loader, file_saver=saver)

    bytes_written = processor.resize_and_save(
        "source.jpg", "dest.jpg", 200, 150, quality=90
    )

    # Check that bytes were "written"
    assert bytes_written > 0

    # Check that the file was "saved" in the stub
    assert "dest.jpg" in saver.saved_files

    # Verify the saved image dimensions
    saved_bytes = saver.saved_files["dest.jpg"]
    with Image.open(io.BytesIO(saved_bytes)) as img:
        assert img.size == (200, 150)


def test_copy_without_resize():
    test_bytes = create_test_image(400, 300)
    loader = ImageLoader.create_null(response=test_bytes)
    saver = FileSaver.create_null()
    processor = ImageProcessor(image_loader=loader, file_saver=saver)

    bytes_written = processor.copy_without_resize("source.jpg", "dest.jpg")

    # Check that the exact bytes were copied
    assert bytes_written == len(test_bytes)
    assert "dest.jpg" in saver.saved_files
    assert saver.saved_files["dest.jpg"] == test_bytes


def test_resize_and_save_with_tracking():
    test_bytes = create_test_image(800, 600)
    loader = ImageLoader.create_null(response=test_bytes)
    saver = FileSaver.create_null()
    processor = ImageProcessor(image_loader=loader, file_saver=saver)

    tracker = processor.track_output()
    processor.resize_and_save("input.jpg", "output.jpg", 400, 300, quality=85)

    # Check that the action was tracked
    events = tracker.data
    assert len(events) == 1
    event = events[0]
    assert event["action"] == "resize_and_save"
    assert event["source"] == "input.jpg"
    assert event["destination"] == "output.jpg"
    assert event["original_size"] == (800, 600)
    assert event["new_size"] == (400, 300)
    assert event["quality"] == 85


def test_image_mode_conversion():
    # Create an RGBA image
    img = Image.new('RGBA', (100, 100), color=(255, 0, 0, 128))
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    rgba_bytes = buffer.getvalue()

    processor = ImageProcessor.create_null()

    # Resize should handle RGBA -> RGB conversion
    resized_bytes = processor.resize_image_bytes(rgba_bytes, 50, 50)

    # Check that the result is a valid JPEG (RGB)
    with Image.open(io.BytesIO(resized_bytes)) as img:
        assert img.mode == 'RGB'
        assert img.size == (50, 50)