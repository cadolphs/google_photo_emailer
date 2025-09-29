import pytest
from photo_emailer.logic.image_dimension_calculator import (
    calculate_new_dimensions,
    needs_resizing
)


def test_calculate_dimensions_with_max_dimension_landscape():
    # Landscape image: 4000x3000
    width, height = 4000, 3000
    new_width, new_height = calculate_new_dimensions(width, height, max_dimension=2000)

    assert new_width == 2000
    assert new_height == 1500  # Maintains 4:3 aspect ratio


def test_calculate_dimensions_with_max_dimension_portrait():
    # Portrait image: 3000x4000
    width, height = 3000, 4000
    new_width, new_height = calculate_new_dimensions(width, height, max_dimension=2000)

    assert new_width == 1500  # Maintains 3:4 aspect ratio
    assert new_height == 2000


def test_calculate_dimensions_with_max_dimension_square():
    # Square image: 3000x3000
    width, height = 3000, 3000
    new_width, new_height = calculate_new_dimensions(width, height, max_dimension=1500)

    assert new_width == 1500
    assert new_height == 1500


def test_calculate_dimensions_no_resize_needed():
    # Image already smaller than max_dimension
    width, height = 1000, 800
    new_width, new_height = calculate_new_dimensions(width, height, max_dimension=2000)

    assert new_width == 1000  # No change
    assert new_height == 800   # No change


def test_calculate_dimensions_with_max_width():
    width, height = 4000, 3000
    new_width, new_height = calculate_new_dimensions(width, height, max_width=2000)

    assert new_width == 2000
    assert new_height == 1500  # Maintains aspect ratio


def test_calculate_dimensions_with_max_height():
    width, height = 4000, 3000
    new_width, new_height = calculate_new_dimensions(width, height, max_height=1500)

    assert new_width == 2000  # Maintains aspect ratio
    assert new_height == 1500


def test_calculate_dimensions_with_both_max_width_and_height():
    # Should fit within both constraints
    width, height = 4000, 3000
    new_width, new_height = calculate_new_dimensions(width, height, max_width=1600, max_height=1000)

    # Should be limited by height constraint (more restrictive)
    assert new_width == 1333  # 4000 * (1000/3000)
    assert new_height == 1000


def test_calculate_dimensions_max_dimension_overrides_width_height():
    # max_dimension should take precedence
    width, height = 4000, 3000
    new_width, new_height = calculate_new_dimensions(
        width, height,
        max_dimension=1000,
        max_width=2000,  # These should be ignored
        max_height=2000
    )

    assert new_width == 1000
    assert new_height == 750


def test_calculate_dimensions_invalid_input():
    with pytest.raises(ValueError):
        calculate_new_dimensions(0, 100, max_dimension=1000)

    with pytest.raises(ValueError):
        calculate_new_dimensions(100, -10, max_dimension=1000)


def test_calculate_dimensions_very_small_result():
    # Should never return 0 dimensions
    width, height = 10000, 1
    new_width, new_height = calculate_new_dimensions(width, height, max_dimension=100)

    assert new_width == 100
    assert new_height == 1  # Should be at least 1


def test_needs_resizing_with_max_dimension():
    assert needs_resizing(4000, 3000, max_dimension=2000) is True
    assert needs_resizing(1500, 1000, max_dimension=2000) is False
    assert needs_resizing(2000, 2000, max_dimension=2000) is False
    assert needs_resizing(2001, 1999, max_dimension=2000) is True


def test_needs_resizing_with_max_width():
    assert needs_resizing(4000, 3000, max_width=3000) is True
    assert needs_resizing(2000, 3000, max_width=3000) is False


def test_needs_resizing_with_max_height():
    assert needs_resizing(4000, 3000, max_height=2000) is True
    assert needs_resizing(4000, 1500, max_height=2000) is False


def test_needs_resizing_with_both_constraints():
    assert needs_resizing(4000, 3000, max_width=5000, max_height=2000) is True
    assert needs_resizing(4000, 3000, max_width=5000, max_height=4000) is False