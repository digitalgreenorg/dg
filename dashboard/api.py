from tastypie.resources import ModelResource
from dashboard.models import Country,State,District,Block,Village,FieldOfficer,Partners
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from django.conf.urls.defaults import patterns, include, url
from tastypie.utils import trailing_slash
from haystack.query import SearchQuerySet
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from forms import  CountryForm,StateForm,DistrictForm,BlockForm,VillageForm,FieldOfficerForm,PartnerForm
from tastypie import fields
from tastypie.validation import FormValidation
from django.forms.models import ModelChoiceField



class ModelFormValidation(FormValidation):
    """
        Override tastypie's standard ``FormValidation`` since this does not care
        about URI to PK conversion for ``ToOneField`` or ``ToManyField``.
        """
    
    def uri_to_pk(self, uri):
        """
            Returns the integer PK part of a URI.
            
            Assumes ``/api/v1/resource/123/`` format. If conversion fails, this just
            returns the URI unmodified.
            
            Also handles lists of URIs
            """
        
        if uri is None:
            return None
        
        # convert everything to lists
        multiple = not isinstance(uri, basestring)
        uris = uri if multiple else [uri]
        
        # handle all passed URIs
        converted = []
        for one_uri in uris:
            try:
                # hopefully /api/v1/<resource_name>/<pk>/
                converted.append(int(one_uri.split('/')[-2]))
            except (IndexError, ValueError):
                raise ValueError(
                                 "URI %s could not be converted to PK integer." % one_uri)
        
        # convert back to original format
        return converted if multiple else converted[0]
    
    def is_valid(self, bundle, request=None):
        data = bundle.data
        # Ensure we get a bound Form, regardless of the state of the bundle.
        if data is None:
            data = {}
        # copy data, so we don't modify the bundle
        data = data.copy()
        
        # convert URIs to PK integers for all relation fields
        relation_fields = [name for name, field in
                           self.form_class.base_fields.items()
                           if issubclass(field.__class__, ModelChoiceField)]
        
        for field in relation_fields:
            if field in data:
                data[field] = self.uri_to_pk(data[field])
        
        # validate and return messages on error
        form = self.form_class(data)
        if form.is_valid():
            return {}
        return form.errors

class CountryResource(ModelResource):
    class Meta:
        queryset = Country.objects.all()
        resource_name = 'country'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        ordering = ["start_date","country_name"]
        filtering = {
        'country_name': ALL,
        'start_date':ALL,
        }
        always_return_data = True
        validation = FormValidation(form_class=CountryForm)
    
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
            ]
    
    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        
        # Do the query.
        sqs = SearchQuerySet().models(Country).load_all().auto_query(request.GET.get('q', ''))
        paginator = Paginator(sqs, 20)
        
        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")
        
        objects = []
        
        for result in page.object_list:
            bundle = self.build_bundle(obj=result.object, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)
        
        object_list = {
            'objects': objects,
        }
        
        self.log_throttled_access(request)
        return self.create_response(request, object_list)

class StateResource(ModelResource):
    country = fields.ForeignKey(CountryResource, 'country')
    class Meta:
        queryset = State.objects.all()
        resource_name = 'state'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        ordering = ["start_date","state_name","region","country"]
        filtering = {
        'state_name': ALL,
        'start_date': ALL,
        'region':ALL,
        'country':ALL_WITH_RELATIONS,
        }
        always_return_data = True
        validation = ModelFormValidation(form_class=StateForm)
    
    def override_urls(self):
        return [
        url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
        ]
    
    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        
        # Do the query.
        sqs = SearchQuerySet().models(State).load_all().auto_query(request.GET.get('q', ''))
        paginator = Paginator(sqs, 20)
        
        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")
        
        objects = []
        
        for result in page.object_list:
            bundle = self.build_bundle(obj=result.object, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)
        
        object_list = {
            'objects': objects,
        }
        
        self.log_throttled_access(request)
        return self.create_response(request, object_list)


class DistrictResource(ModelResource):
    state = fields.ForeignKey(StateResource, 'state')
    class Meta:
        queryset = District.objects.all()
        resource_name = 'district'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        #fields=["start_date","state","district_name","id"]
        ordering = ["start_date","state","district_name"]
        filtering = {
        'district_name': ALL,
        'state':ALL_WITH_RELATIONS,
        'start_date': ALL,
        }
        always_return_data = True
        validation = ModelFormValidation(form_class=DistrictForm)
    def override_urls(self):
        return [
                url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
                ]
    
    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        
        # Do the query.
        sqs = SearchQuerySet().models(District).load_all().auto_query(request.GET.get('q', ''))
        paginator = Paginator(sqs, 20)
        
        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")
        
        objects = []
        
        for result in page.object_list:
            bundle = self.build_bundle(obj=result.object, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)
        
        object_list = {
            'objects': objects,
        }
        
        self.log_throttled_access(request)
        return self.create_response(request, object_list)

class BlockResource(ModelResource):
    district = fields.ForeignKey(DistrictResource, 'district')
    class Meta:
        queryset = Block.objects.all()
        resource_name = 'block'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        ordering = ["start_date","block_name","district"]
        filtering = {
        'block_name': ALL,
        'district':ALL_WITH_RELATIONS,
        'start_date': ALL,
        }
        always_return_data = True
        validation = ModelFormValidation(form_class=BlockForm)
    
    def override_urls(self):
        return [
                url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
                ]
    
    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        
        # Do the query.
        sqs = SearchQuerySet().models(Block).load_all().auto_query(request.GET.get('q', ''))
        paginator = Paginator(sqs, 20)
        
        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")
        
        objects = []
        
        for result in page.object_list:
            bundle = self.build_bundle(obj=result.object, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)
        
        object_list = {
            'objects': objects,
        }
        
        self.log_throttled_access(request)
        return self.create_response(request, object_list)

class VillageResource(ModelResource):
    block = fields.ForeignKey(BlockResource, 'block')
    class Meta:
        queryset = Village.objects.all()
        resource_name = 'village'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        excludes = ["no_of_households","road_connectivity"]
        ordering = ["start_date","village_name","block","population"]
        filtering = {
        'village_name': ALL,
        'block':ALL_WITH_RELATIONS,
        'start_date': ALL,
        }
        always_return_data = True
        validation = ModelFormValidation(form_class=VillageForm)
    
    def override_urls(self):
        return [
                url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
                ]
    
    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        
        # Do the query.
        sqs = SearchQuerySet().models(Village).load_all().auto_query(request.GET.get('q', ''))
        paginator = Paginator(sqs, 20)
        
        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")
        
        objects = []
        
        for result in page.object_list:
            bundle = self.build_bundle(obj=result.object, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)
        
        object_list = {
            'objects': objects,
        }
        
        self.log_throttled_access(request)
        return self.create_response(request, object_list)

class FieldOfficerResource(ModelResource):
    class Meta:
        queryset = FieldOfficer.objects.all()
        resource_name = 'field_officer'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True
        validation = ModelFormValidation(form_class=FieldOfficerForm)

class PartnersResource(ModelResource):
    class Meta:
        queryset = Partners.objects.all()
        resource_name = 'partner'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True
        validation = ModelFormValidation(form_class=PartnerForm)



