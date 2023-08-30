from email.message import EmailMessage
from photo_emailer.infrastructure.email_sender import EmailSender
from photo_emailer.logic.credentials import Credentials


def test_email_sender_sends_email():
    msg = EmailMessage()
    msg["Subject"] = "Test Subject"
    msg["To"] = "test_to@test.com"
    msg.set_content("Test Content")

    sender = EmailSender.create_null()
    output = sender.track_output()

    creds = Credentials.get_test_instance()

    sender.send_email(msg, creds)

    assert output.data == [{"action": "send_email", "msg": msg, "creds": creds}]
