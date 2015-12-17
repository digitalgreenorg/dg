from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from models import Upload

class UploadResource(ModelResource):
	class Meta:
		queryset = Upload.objects.all()
		resource_name = 'upload'
		authentication = Authentication()
		authorization = Authorization()