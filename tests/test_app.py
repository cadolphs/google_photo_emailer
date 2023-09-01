from photo_emailer.app import PhotoEmailer
from photo_emailer.logic.credentials import Credentials
from photo_emailer.infrastructure.credentials_io import CredentialsIO
from photo_emailer.infrastructure.credentials_refresher import CredentialsRefresher
from photo_emailer.infrastructure.browser_authentication import BrowserAuthClient
from photo_emailer.infrastructure.email_sender import EmailSender
from photo_emailer.infrastructure.globber import Globber
from photo_emailer.infrastructure.image_loader import ImageLoader


def test_app_loads_token_from_file():
    creds = Credentials.get_test_instance()
    loader = CredentialsIO.create_null(result=creds.to_dict())

    app = PhotoEmailer(credentials_loader=loader)
    app.load_credentials()

    assert app.credentials == creds


def test_app_can_refresh_credentials_if_expired():
    creds = Credentials.get_test_instance()
    creds.expiry = "2022-08-23T21:04:01.984063Z"

    loader = CredentialsIO.create_null(result=creds.to_dict())
    refresher = CredentialsRefresher.create_null()

    app = PhotoEmailer(credentials_loader=loader, credentials_refresher=refresher)

    app.load_credentials()
    app.refresh_if_needed()

    assert app.credentials.is_expired() is False


def test_app_invokes_browser_flow_if_refresh_fails():
    creds = Credentials.get_test_instance()
    creds.expiry = "2022-08-23T21:04:01.984063Z"

    loader = CredentialsIO.create_null(result=creds.to_dict())
    loader_output = loader.track_output()

    refresher = CredentialsRefresher.create_test_instance_that_errors()
    browser_auth_client = BrowserAuthClient.create_null()

    app = PhotoEmailer(
        credentials_loader=loader,
        credentials_refresher=refresher,
        browser_auth_client=browser_auth_client,
    )

    app.load_credentials()
    app.refresh_if_needed()
    app.store_credentials()
    assert app.credentials.is_expired() is False


def test_app_can_send_email():
    creds = Credentials.get_test_instance()

    loader = CredentialsIO.create_null(result=creds.to_dict())
    loader_output = loader.track_output()

    refresher = CredentialsRefresher.create_null()
    browser_auth_client = BrowserAuthClient.create_null()

    sender = EmailSender.create_null()
    sender_output = sender.track_output()

    app = PhotoEmailer(
        credentials_loader=loader,
        credentials_refresher=refresher,
        browser_auth_client=browser_auth_client,
        sender=sender,
    )

    app.load_credentials()
    app.refresh_if_needed()
    app.store_credentials()

    app.send_email(to="test@test.com")

    data = sender_output.data[0]
    assert data["action"] == "send_email"
    msg = data["msg"]
    assert msg["Subject"] == ""
    assert msg["To"] == "test@test.com"

    expected = app.prepare_email("test@test.com")

    content = None
    expected_content = None
    attachment = None
    expected_attachment = None

    for part, expected_part in zip(msg.walk(), expected.walk(), strict=True):
        if part.get_content_type() == "text/plain":
            content = part.get_content()
            expected_content = expected_part.get_content()
        elif part.get_content_type() == "image/png":
            attachment = part.get_content()
            expected_attachment = expected_part.get_content()


def test_email_preparation_loads_directory():
    globber = Globber.create_null(files=["test1.jpg", "test2.jpg"])
    image_loader = ImageLoader.create_null(response=b"test")

    app = PhotoEmailer(globber=globber, image_loader=image_loader)

    email = app.prepare_email("foo@bar.com")

    num_attachments = 0
    for part in email.walk():
        if part.get_content_maintype() == "image":
            num_attachments += 1
    assert num_attachments == 2


def test_app_sends_multiple_emails_when_chunking():
    creds = Credentials.get_test_instance()

    loader = CredentialsIO.create_null(result=creds.to_dict())

    refresher = CredentialsRefresher.create_null()
    browser_auth_client = BrowserAuthClient.create_null()

    sender = EmailSender.create_null()
    sender_output = sender.track_output()

    globber = Globber.create_null(files=["test1.jpg", "test2.jpg", "test3.jpg"])
    image_loader = ImageLoader.create_null(response=bytes(1000))

    app = PhotoEmailer(
        credentials_loader=loader,
        credentials_refresher=refresher,
        browser_auth_client=browser_auth_client,
        sender=sender,
        globber=globber,
        image_loader=image_loader,
        max_email_size=2000,
    )

    app.load_credentials()
    app.refresh_if_needed()
    app.store_credentials()

    app.send_emails(to="test@test.com")

    # expecting two emails in the output
    assert len(sender_output.data) == 2

    # First mail should have two attachments, second should have one
    msg_1 = sender_output.data[0]["msg"]
    msg_2 = sender_output.data[1]["msg"]

    num_attachments_1 = len(
        [part for part in msg_1.walk() if part.get_content_maintype() == "image"]
    )
    num_attachments_2 = len(
        [part for part in msg_2.walk() if part.get_content_maintype() == "image"]
    )

    assert num_attachments_1 == 2
    assert num_attachments_2 == 1
