from email.message import EmailMessage
from photo_emailer.infrastructure.email_sender import EmailSender


def test_email_sender_sends_email():
    msg = EmailMessage()
    msg["To"] = "clemens.adolphs+test@gmail.com"
    msg["Subject"] = "Test"
    msg.set_content("A test email.")

    sender = EmailSender.create_null()
    output_tracker = sender.track_output()

    sender.send_email(msg)

    assert output_tracker.data[0]["action"] == "send_email"
