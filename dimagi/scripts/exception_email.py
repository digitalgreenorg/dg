from django.core.mail import EmailMultiAlternatives
import dg.settings


def sendmail(subject, body):
    from_email = dg.settings.EMAIL_HOST_USER
    to_email = ["sreenivas@digitalgreen.org", "aadish@digitalgreen.org", "nandini@digitalgreen.org", "jahnavi@digitalgreen.org"]
    msg = EmailMultiAlternatives(subject, body, from_email, to_email)
    msg.send()
