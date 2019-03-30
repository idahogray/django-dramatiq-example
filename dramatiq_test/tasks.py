from django.core.mail import EmailMultiAlternatives
from dramatiq import actor

from .models import AModel


def _should_retry(num_retries, exception):
    # dramatiq retries after any exception. This will limit the
    # retry attempts to SMTP and socket timeouts only.
    return (
        isinstance(exception, SMTPException)
        or isinstance(exception, socket.timeout)
    )


@actor(retry_when=_should_retry)
def send_email_1(subject):
    print("Task Sending Email 1...")
    email = EmailMultiAlternatives(
        subject=subject,
        body='This is a test body',
        from_email='idahogray@gmail.com',
        to=('idahogray@gmail.com',)
    )
    email.send()
    print("...Email 1 Sent (Task)")


@actor(retry_when=_should_retry)
def send_email_2(subject):
    print("Task Sending Email 2...")
    email = EmailMultiAlternatives(
        subject=subject,
        body='This is a test body',
        from_email='idahogray@gmail.com',
        to=('idahogray@gmail.com',)
    )
    email.send()
    print("...Email 2 Sent (Task)")


@actor(retry_when=_should_retry)
def send_email_3(subject):
    print("Task Sending Email 3...")
    email = EmailMultiAlternatives(
        subject=subject,
        body='This is a test body',
        from_email='idahogray@gmail.com',
        to=('idahogray@gmail.com',)
    )
    email.send()
    print("...Email 3 Sent (Task)")


@actor(retry_when=_should_retry)
def send_email_4(subject):
    print("Task Sending Email 4...")
    email = EmailMultiAlternatives(
        subject=subject,
        body='This is a test body',
        from_email='idahogray@gmail.com',
        to=('idahogray@gmail.com',)
    )
    email.send()
    print("...Email 4 Sent (Task)")


@actor(retry_when=_should_retry)
def send_email_5(subject):
    print("Task Sending Email 5...")
    a_model = AModel.objects.first()
    print(a_model.a_field)
    email = EmailMultiAlternatives(
        subject=subject,
        body='This is a test body',
        from_email='idahogray@gmail.com',
        to=('idahogray@gmail.com',)
    )
    email.send()
    print("...Email 5 Sent (Task)")