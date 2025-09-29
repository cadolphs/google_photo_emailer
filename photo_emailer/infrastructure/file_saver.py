import os
from photo_emailer.utils.events import OutputListener


class FileSaver:
    """Infrastructure wrapper for saving files to disk."""

    def __init__(self):
        self._listener = OutputListener()

    def track_output(self):
        return self._listener.create_tracker()

    @classmethod
    def create(cls):
        return cls()

    @classmethod
    def create_null(cls):
        return FileSaverStub()

    def save_bytes(self, data, path):
        """
        Save bytes to a file.

        Args:
            data: Bytes to save
            path: Path where file will be saved

        Returns:
            Number of bytes written
        """
        with open(path, 'wb') as f:
            bytes_written = f.write(data)

        self._listener.track(data={
            "action": "save_bytes",
            "path": path,
            "bytes_written": bytes_written
        })

        return bytes_written

    def get_file_size(self, path):
        """Get the size of a file in bytes."""
        return os.path.getsize(path)


class FileSaverStub(FileSaver):
    """Nullable version for testing."""

    def __init__(self):
        super().__init__()
        self.saved_files = {}

    def save_bytes(self, data, path):
        """Track saves without actual file operations."""
        bytes_written = len(data)
        self.saved_files[path] = data

        self._listener.track(data={
            "action": "save_bytes",
            "path": path,
            "bytes_written": bytes_written
        })

        return bytes_written

    def get_file_size(self, path):
        """Return size of saved data or default."""
        if path in self.saved_files:
            return len(self.saved_files[path])
        return 1000  # Default size for testing