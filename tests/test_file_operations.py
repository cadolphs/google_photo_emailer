from photo_emailer.infrastructure.file_operations import FileOperations


def test_file_operations_tracks_create_directory():
    file_ops = FileOperations.create_null()
    output = file_ops.track_output()
    
    file_ops.create_directory("/test/path")
    
    assert output.data[0] == {"action": "create_directory", "path": "/test/path"}


def test_file_operations_tracks_copy_file():
    file_ops = FileOperations.create_null()
    output = file_ops.track_output()
    
    file_ops.copy_file("source.jpg", "dest.jpg")
    
    assert output.data[0] == {"action": "copy_file", "source": "source.jpg", "destination": "dest.jpg"}


def test_file_operations_get_file_size():
    file_ops = FileOperations.create_null()
    file_ops.set_file_size("test.jpg", 5000)
    
    size = file_ops.get_file_size("test.jpg")
    
    assert size == 5000


def test_file_operations_default_file_size():
    file_ops = FileOperations.create_null()
    
    size = file_ops.get_file_size("unknown.jpg")
    
    assert size == 1000  # default size