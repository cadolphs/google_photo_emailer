import pytest
from photo_emailer.infrastructure.file_operations import FileOperations
from photo_emailer.logic.file_organizer import chunk_files_by_size


def test_chunk_files_by_size_smaller_than_limit():
    file_operations = FileOperations.create_null()
    file_operations.set_file_size("file1.jpg", 1000)
    file_operations.set_file_size("file2.jpg", 1000)
    file_operations.set_file_size("file3.jpg", 1000)
    
    file_paths = ["file1.jpg", "file2.jpg", "file3.jpg"]
    chunks = chunk_files_by_size(file_paths, 3000, file_operations)
    
    assert len(chunks) == 1
    assert chunks[0] == file_paths


def test_chunk_files_by_size_bigger_than_limit():
    file_operations = FileOperations.create_null()
    file_operations.set_file_size("file1.jpg", 1000)
    file_operations.set_file_size("file2.jpg", 1001)
    file_operations.set_file_size("file3.jpg", 1002)
    
    file_paths = ["file1.jpg", "file2.jpg", "file3.jpg"]
    chunks = chunk_files_by_size(file_paths, 3000, file_operations)
    
    assert len(chunks) == 2
    assert chunks[0] == ["file1.jpg", "file2.jpg"]
    assert chunks[1] == ["file3.jpg"]


def test_chunk_files_by_size_raises_error_if_single_file_bigger_than_limit():
    file_operations = FileOperations.create_null()
    file_operations.set_file_size("huge_file.jpg", 3001)
    
    file_paths = ["huge_file.jpg"]
    
    with pytest.raises(ValueError):
        chunk_files_by_size(file_paths, 3000, file_operations)


def test_chunk_files_by_size_empty_list():
    file_operations = FileOperations.create_null()
    chunks = chunk_files_by_size([], 1000, file_operations)
    assert chunks == []