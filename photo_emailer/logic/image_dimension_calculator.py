def calculate_new_dimensions(width, height, max_dimension=None, max_width=None, max_height=None):
    """
    Calculate new dimensions for an image while maintaining aspect ratio.
    This is pure logic with no dependencies on image libraries or file I/O.

    Args:
        width: Current image width in pixels
        height: Current image height in pixels
        max_dimension: Maximum size for the larger dimension (width or height)
        max_width: Maximum width in pixels (ignored if max_dimension is set)
        max_height: Maximum height in pixels (ignored if max_dimension is set)

    Returns:
        Tuple of (new_width, new_height). Returns original dimensions if no
        resizing is needed.
    """
    if width <= 0 or height <= 0:
        raise ValueError(f"Invalid dimensions: {width}x{height}")

    new_width, new_height = width, height

    if max_dimension and max_dimension > 0:
        # Use max_dimension for the larger of the two dimensions
        larger_dimension = max(width, height)

        if larger_dimension > max_dimension:
            # Calculate scale factor based on the larger dimension
            scale_factor = max_dimension / larger_dimension
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)

    elif max_width or max_height:
        # Use specific width/height constraints
        scale_factor = 1.0

        if max_width and width > max_width:
            scale_factor = min(scale_factor, max_width / width)

        if max_height and height > max_height:
            scale_factor = min(scale_factor, max_height / height)

        if scale_factor < 1.0:
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)

    # Ensure we don't return 0 dimensions
    new_width = max(1, new_width)
    new_height = max(1, new_height)

    return new_width, new_height


def needs_resizing(width, height, max_dimension=None, max_width=None, max_height=None):
    """
    Check if an image needs resizing based on the given constraints.

    Args:
        width: Current image width in pixels
        height: Current image height in pixels
        max_dimension: Maximum size for the larger dimension
        max_width: Maximum width in pixels
        max_height: Maximum height in pixels

    Returns:
        Boolean indicating if resizing is needed
    """
    if max_dimension and max_dimension > 0:
        return max(width, height) > max_dimension

    if max_width and width > max_width:
        return True

    if max_height and height > max_height:
        return True

    return False