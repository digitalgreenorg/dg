from django.conf import settings # import the settings file

def admin_media(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {
        'WEBSITE_DOMAIN': settings.WEBSITE_DOMAIN,
        'PRIVACY_POLICY': settings.PRIVACY_POLICY,
        'TERMS_SERVICE': settings.TERMS_SERVICE
    }
