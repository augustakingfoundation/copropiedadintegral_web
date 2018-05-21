from django.conf import settings
from django.core.mail import EmailMessage

from huey.contrib.djhuey import task


@task(retries=0, retry_delay=60 * 10)
def send_email(subject, body, mail_to, reply_to=None):
    email_message = EmailMessage(
        subject=settings.EMAIL_SUBJECT.format(subject),
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=mail_to,
        reply_to=reply_to,
    )
    email_message.content_subtype = 'html'
    email_message.send()
