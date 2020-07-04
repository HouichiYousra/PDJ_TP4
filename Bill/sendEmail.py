
from django.core.mail import EmailMessage
from Bill.settings import EMAIL_HOST_USER
# Create your views here.


def send(_message, _subject, _receivers):
    message = _message
    subject = _subject
    email = EmailMessage(subject, message, EMAIL_HOST_USER, _receivers)
    email.send()
