from tastypie.authentication import ApiKeyAuthentication
from tastypie.models import ApiKey
from django.http import HttpResponse




class AnonymousGETAuthentication(ApiKeyAuthentication):
    """ Check user api key with request user. Applicable for both web and mobile """

    def is_authenticated(self, request, **kwargs):
        """ Check user API key """

        if request.method == "GET":
            meta_auth_container = request.META.get('HTTP_AUTHORIZATION')
            if meta_auth_container and len(meta_auth_container):
                apikey = meta_auth_container.split('ApiKey')[-1].split(':')[-1]
                try:
                    apikey_object = ApiKey.objects.get(key=apikey)
                    if apikey_object:
                        return True
                except Exception:
                    return HttpResponse("-1", status=401)
        else:
            return HttpResponse("-1", status=401)
