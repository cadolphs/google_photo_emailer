from photo_emailer.infrastructure.credentials_io import CredentialsIO

from photo_emailer.logic.credentials import Credentials
from photo_emailer.infrastructure.email_sender import EmailSender
from photo_emailer.infrastructure.credentials_refresher import CredentialsRefresher
from photo_emailer.infrastructure.browser_authentication import BrowserAuthClient
from email.message import EmailMessage
from google.auth.exceptions import RefreshError
from photo_emailer.infrastructure.image_loader import ImageLoader
from photo_emailer.infrastructure.globber import Globber
from photo_emailer.logic.chunker import chunk_files


class PhotoEmailer:
    def __init__(
        self,
        credentials_loader=None,
        credentials_refresher=None,
        browser_auth_client=None,
        sender=None,
        image_loader=None,
        globber=None,
        image_directory="./",
        max_email_size=8 * 1024 * 1024,
    ):
        self.credentials_loader = (
            credentials_loader
            if credentials_loader is not None
            else CredentialsIO.create("token.json")
        )

        self.credentials_refresher = (
            credentials_refresher
            if credentials_refresher is not None
            else CredentialsRefresher.create()
        )

        self.browser_auth_client = (
            browser_auth_client
            if browser_auth_client is not None
            else BrowserAuthClient.create()
        )

        self.sender = sender if sender is not None else EmailSender.create()

        self.image_loader = (
            image_loader if image_loader is not None else ImageLoader.create()
        )

        self.globber = globber if globber is not None else Globber.create()

        self.image_directory = image_directory

        self.max_email_size = max_email_size

        self.credentials = None

    def load_credentials(self):
        self.credentials = Credentials.from_dict(
            self.credentials_loader.load_credentials()
        )

    def refresh_if_needed(self):
        try:
            if self.credentials.is_expired():
                self.credentials = self.credentials_refresher.refresh(self.credentials)
        except RefreshError:
            self.credentials = self.browser_auth_client.run_browser_authentication()

    def store_credentials(self):
        self.credentials_loader.store_credentials(self.credentials.to_dict())

    def send_email(self, to):
        msg = self.prepare_email(to)
        self.sender.send_email(msg, self.credentials)

    def send_emails(self, to):
        for msg in self.prepare_emails(to):
            self.sender.send_email(msg, self.credentials)

    def send_test_email(self, to):
        msg = EmailMessage()
        msg.set_content("Hi mom!")
        msg["Subject"] = "Test"
        msg["To"] = to
        self.sender.send_email(msg, self.credentials)

    def prepare_emails(self, to):
        image_files = self.globber.glob(self.image_directory)
        image_contents = [
            self.image_loader.load_image(image_file) for image_file in image_files
        ]
        chunks = chunk_files(image_contents, self.max_email_size)

        msgs = []
        for chunk in chunks:
            msg = EmailMessage()
            msg["Subject"] = "Photos"
            msg["To"] = to
            msg["From"] = "clemens.adolphs@gmail.com"
            for idx, image in enumerate(chunk):
                msg.add_attachment(image, maintype="image", subtype="jpeg", filename=f"photo_{idx+1}.jpg")
            msgs.append(msg)
        return msgs

    def prepare_email(self, to):
        msg = EmailMessage()
        msg["subject"] = ""
        msg["to"] = to
        msg.set_content("Hello World")

        for image_file in self.globber.glob(self.image_directory):
            image = self.image_loader.load_image(image_file)
            msg.add_attachment(image, maintype="image", subtype="jpg")

        return msg
