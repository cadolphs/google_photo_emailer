from PIL import Image
import io
from photo_emailer.utils.events import OutputListener
from photo_emailer.infrastructure.image_loader import ImageLoader
from photo_emailer.infrastructure.file_saver import FileSaver


class ImageProcessor:
    """Infrastructure wrapper for PIL image operations."""

    def __init__(self, image_loader=None, file_saver=None):
        self._listener = OutputListener()
        self._image_loader = image_loader or ImageLoader.create()
        self._file_saver = file_saver or FileSaver.create()

    def track_output(self):
        return self._listener.create_tracker()

    @classmethod
    def create(cls):
        return cls(ImageLoader.create(), FileSaver.create())

    @classmethod
    def create_null(cls, test_image_bytes=None):
        # Use the same ImageProcessor but with nulled dependencies
        if test_image_bytes is None:
            # Create a minimal valid JPEG for testing
            img = Image.new('RGB', (100, 100), color='white')
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG')
            test_image_bytes = buffer.getvalue()

        return cls(
            ImageLoader.create_null(response=test_image_bytes),
            FileSaver.create_null()
        )

    def get_image_dimensions_from_file(self, image_path):
        """
        Get the dimensions of an image file.

        Args:
            image_path: Path to the image file

        Returns:
            Tuple of (width, height) in pixels
        """
        image_bytes = self._image_loader.load_image(image_path)
        return self.get_image_dimensions_from_bytes(image_bytes)

    def get_image_dimensions_from_bytes(self, image_bytes):
        """
        Get the dimensions from image bytes.
        This is pure PIL logic, no I/O.

        Args:
            image_bytes: Raw image data

        Returns:
            Tuple of (width, height) in pixels
        """
        with Image.open(io.BytesIO(image_bytes)) as img:
            return img.size

    def resize_image_bytes(self, image_bytes, new_width, new_height, quality=85):
        """
        Resize image bytes and return the resized bytes.
        This is pure PIL logic, no I/O.

        Args:
            image_bytes: Raw image data
            new_width: Target width in pixels
            new_height: Target height in pixels
            quality: JPEG quality (1-100, default 85)

        Returns:
            Resized image as bytes
        """
        with Image.open(io.BytesIO(image_bytes)) as img:
            # Convert RGBA/P to RGB for JPEG compatibility
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                if img.mode in ('RGBA', 'LA'):
                    background.paste(img, mask=img.split()[-1])
                else:
                    background.paste(img)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            # Resize the image
            resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Convert to bytes
            buffer = io.BytesIO()
            resized.save(buffer, format='JPEG', quality=quality, optimize=True)
            return buffer.getvalue()

    def resize_and_save(self, source_path, destination_path, new_width, new_height, quality=85):
        """
        Load an image, resize it, and save to destination.

        Args:
            source_path: Path to source image file
            destination_path: Path where resized image will be saved
            new_width: Target width in pixels
            new_height: Target height in pixels
            quality: JPEG quality (1-100, default 85)

        Returns:
            Actual size of the saved file in bytes
        """
        # Load image using the image_loader dependency
        image_bytes = self._image_loader.load_image(source_path)

        # Get original dimensions for tracking
        original_size = self.get_image_dimensions_from_bytes(image_bytes)

        # Resize the image (pure logic)
        resized_bytes = self.resize_image_bytes(image_bytes, new_width, new_height, quality)

        # Save using the file_saver dependency
        bytes_written = self._file_saver.save_bytes(resized_bytes, destination_path)

        self._listener.track(data={
            "action": "resize_and_save",
            "source": source_path,
            "destination": destination_path,
            "original_size": original_size,
            "new_size": (new_width, new_height),
            "quality": quality,
            "file_size_bytes": bytes_written
        })

        return bytes_written

    def copy_without_resize(self, source_path, destination_path):
        """
        Copy an image file without resizing.

        Args:
            source_path: Path to source image file
            destination_path: Path where image will be copied

        Returns:
            Size of the copied file in bytes
        """
        # Load using image_loader dependency
        image_bytes = self._image_loader.load_image(source_path)

        # Save using file_saver dependency
        bytes_written = self._file_saver.save_bytes(image_bytes, destination_path)

        self._listener.track(data={
            "action": "copy_without_resize",
            "source": source_path,
            "destination": destination_path,
            "file_size_bytes": bytes_written
        })

        return bytes_written