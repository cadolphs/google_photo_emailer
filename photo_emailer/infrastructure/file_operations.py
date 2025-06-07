import os
import shutil
from pathlib import Path
from photo_emailer.utils.events import OutputListener


class FileOperations:
    def __init__(self):
        self._listener = OutputListener()

    def track_output(self):
        return self._listener.create_tracker()

    @classmethod
    def create(cls):
        return cls()

    @classmethod
    def create_null(cls):
        return FileOperationsStub()

    def create_directory(self, path):
        """Create a directory if it doesn't exist."""
        Path(path).mkdir(parents=True, exist_ok=True)
        self._listener.track(data={"action": "create_directory", "path": path})

    def copy_file(self, source, destination):
        """Copy a file from source to destination."""
        shutil.copy2(source, destination)
        self._listener.track(data={"action": "copy_file", "source": source, "destination": destination})

    def get_file_size(self, file_path):
        """Get the size of a file in bytes."""
        return os.path.getsize(file_path)


class FileOperationsStub(FileOperations):
    def __init__(self):
        super().__init__()
        self.file_sizes = {}

    def create_directory(self, path):
        self._listener.track(data={"action": "create_directory", "path": path})

    def copy_file(self, source, destination):
        self._listener.track(data={"action": "copy_file", "source": source, "destination": destination})

    def get_file_size(self, file_path):
        # Return predefined size or default to 1000 bytes
        return self.file_sizes.get(file_path, 1000)

    def set_file_size(self, file_path, size):
        """Helper method for testing to set expected file sizes."""
        self.file_sizes[file_path] = size