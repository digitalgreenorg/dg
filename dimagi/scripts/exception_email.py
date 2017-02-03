from django.core.mail import EmailMultiAlternatives
import dg.settings


def sendmail(subject, body):
    from_email = dg.settings.EMAIL_HOST_USER
    to_email = ["jahnavi@digitalgreen.org","lokesh@digitalgreen.org","abhisheklodha@digitalgreen.org","abhishekchandran@digitalgreen.org"]
    msg = EmailMultiAlternatives(subject, body, from_email, to_email)
    msg.send()
