import typer
from photo_emailer.app import PhotoEmailer
from photo_emailer.logic.file_organizer import organize_files_into_folders

app = typer.Typer()

@app.command()
def send_photos(
    email: str = typer.Argument(..., help="The email address to send the photos to"),
    image_directory: str = typer.Argument(..., help="Directory containing images to send")
):
    """Send photos from the specified directory to email addresses in the provided file."""
    photo_emailer = PhotoEmailer(image_directory=image_directory)
    photo_emailer.load_credentials()
    photo_emailer.refresh_if_needed()
    photo_emailer.store_credentials()
    photo_emailer.send_emails(email)
    # photo_emailer.send_test_email(email)

@app.command()
def chunk_files(
    source_directory: str = typer.Argument(..., help="Directory containing files to organize"),
    output_directory: str = typer.Argument(..., help="Directory where organized sub-folders will be created"),
    max_size_mb: int = typer.Option(25, "--max-size", "-s", help="Maximum size per sub-folder in MB")
):
    """Organize files from source directory into sub-folders with a maximum total size per folder."""
    organize_files_into_folders(source_directory, output_directory, max_size_mb)

if __name__ == "__main__":
    app()
