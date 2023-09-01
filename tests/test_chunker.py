from photo_emailer.logic.chunker import chunk_files
import pytest


def test_chunking_files_smaller_than_limit_gives_simple_list():
    file_contents = [bytes(1000), bytes(1000), bytes(1000)]

    chunks = chunk_files(file_contents, 3000)

    assert len(chunks) == 1
    assert chunks[0] == file_contents


def test_chunking_files_bigger_than_limit_gives_correct_result():
    file_contents = [bytes(1000), bytes(1001), bytes(1002)]

    chunks = chunk_files(file_contents, 3000)

    assert len(chunks) == 2
    assert chunks[0] == file_contents[0:2]
    assert chunks[1] == file_contents[2:]


def test_chunking_raises_error_if_single_file_bigger_than_limit():
    file_contents = [bytes(3001)]

    with pytest.raises(ValueError):
        chunk_files(file_contents, 3000)
