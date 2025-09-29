from photo_emailer.infrastructure.file_operations import FileOperations
from photo_emailer.infrastructure.globber import Globber
from photo_emailer.infrastructure.image_processor import ImageProcessor
from photo_emailer.logic.image_dimension_calculator import calculate_new_dimensions, needs_resizing
import os


def chunk_files_by_size(file_paths, size_limit, file_operations):
    """
    Group file paths into chunks where each chunk's total size is under the limit.
    Returns a list of lists, where each inner list contains file paths.
    """
    if not file_paths:
        return []

    chunks = [[]]
    current_size = 0
    
    for file_path in file_paths:
        file_size = file_operations.get_file_size(file_path)
        
        if file_size > size_limit:
            raise ValueError(
                f"File {file_path} of size {file_size} is bigger than limit of {size_limit}"
            )
        
        if current_size + file_size > size_limit and chunks[-1]:
            chunks.append([])
            current_size = 0
        
        chunks[-1].append(file_path)
        current_size += file_size
    
    return chunks


def organize_files_into_folders(source_directory, output_directory, max_folder_size_mb=25,
                               resize_max_dimension=None, resize_quality=85):
    """
    Organize files from source directory into sub-folders in output directory,
    ensuring each sub-folder's total file size doesn't exceed max_folder_size_mb.

    Args:
        source_directory: Directory containing source images
        output_directory: Directory where organized folders will be created
        max_folder_size_mb: Maximum size per folder in MB
        resize_max_dimension: Optional max dimension for resizing images (None = no resize)
        resize_quality: JPEG quality for resized images (1-100)
    """
    file_operations = FileOperations.create()
    globber = Globber.create()
    image_processor = ImageProcessor.create() if resize_max_dimension else None

    # Convert MB to bytes
    size_limit = max_folder_size_mb * 1024 * 1024

    # Get all image files from source directory
    image_files = globber.glob(source_directory)

    if not image_files:
        print(f"No image files found in {source_directory}")
        return

    # Chunk files by size
    file_chunks = chunk_files_by_size(image_files, size_limit, file_operations)

    # Create output directory
    file_operations.create_directory(output_directory)

    # Copy files to organized sub-folders
    for i, chunk in enumerate(file_chunks, 1):
        folder_name = f"batch_{i:03d}"
        folder_path = os.path.join(output_directory, folder_name)
        file_operations.create_directory(folder_path)

        total_size = 0
        for file_path in chunk:
            filename = os.path.basename(file_path)
            destination = os.path.join(folder_path, filename)

            if resize_max_dimension and image_processor:
                # Check if resizing is needed
                try:
                    width, height = image_processor.get_image_dimensions_from_file(file_path)
                    if needs_resizing(width, height, max_dimension=resize_max_dimension):
                        # Calculate new dimensions
                        new_width, new_height = calculate_new_dimensions(
                            width, height, max_dimension=resize_max_dimension
                        )
                        # Resize and save
                        file_size = image_processor.resize_and_save(
                            file_path, destination, new_width, new_height, resize_quality
                        )
                        print(f"  Resized {filename}: {width}x{height} -> {new_width}x{new_height}")
                    else:
                        # Just copy without resizing
                        file_size = image_processor.copy_without_resize(file_path, destination)
                except Exception as e:
                    print(f"  Warning: Could not process {filename}: {e}")
                    # Fall back to regular copy
                    file_operations.copy_file(file_path, destination)
                    file_size = file_operations.get_file_size(destination)
            else:
                # No resizing requested, just copy
                file_operations.copy_file(file_path, destination)
                file_size = file_operations.get_file_size(destination)

            total_size += file_size

        print(f"Created {folder_name} with {len(chunk)} files ({total_size / (1024*1024):.1f} MB)")

    print(f"Organized {len(image_files)} files into {len(file_chunks)} folders in {output_directory}")