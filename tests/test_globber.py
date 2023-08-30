from photo_emailer.infrastructure.globber import Globber
import pytest


@pytest.fixture
def directory_with_jpgs(tmp_path):
    jpg1 = tmp_path / "test1.jpg"
    jpg1.write_text("test1")
    jpg2 = tmp_path / "test2.jpg"
    jpg2.write_text("test2")
    return tmp_path


def test_globber(directory_with_jpgs):
    # Focused integration test actually reading from the filesystem
    globber = Globber.create()
    files = globber.glob(directory_with_jpgs)
    assert len(files) == 2
    assert f"{directory_with_jpgs}/test1.jpg" in files
    assert f"{directory_with_jpgs}/test2.jpg" in files


def test_nulled_globber():
    # Unit test that uses a null object to avoid actually reading from the filesystem
    globber = Globber.create_null(files=["test1.jpg", "test2.jpg"])
    files = globber.glob("test")
    assert len(files) == 2
    assert "test1.jpg" in files
    assert "test2.jpg" in files
