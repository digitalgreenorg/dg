from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication, Authentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.authentication import SessionAuthentication
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.exceptions import ImmediateHttpResponse, NotFound
from tastypie.resources import ModelResource
from models import Upload


class UploadResource(ModelResource):
	class Meta:
		queryset = Upload.objects.all()
		resource_name = 'upload'
		authentication = Authentication()
		authorization = Authorization()