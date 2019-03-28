from django.core.mail import EmailMultiAlternatives
from dramatiq import actor


@actor
def send_email(subject):
    print("Task Sending Email...")
    email = EmailMultiAlternatives(
        subject=subject,
        body='This is a test body',
        from_email='idahogray@gmail.com',
        to=('idahogray@gmail.com',)
    )
    email.send()
    print("...Email Sent (Task)")