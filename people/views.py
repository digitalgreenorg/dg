from rest_framework import routers, serializers, generics
from rest_framework.response import Response
from rest_framework import status, viewsets
# from rest_framework.decorators import action

from people.models import Person
from geographies.models import Country, State, District, Block, Village
from people.serializers import FarmerSerializer #, VillageSerializer

from geographies.serializers import DistrictSerializer, BlockSerializer, VillageSerializer

from django.http import HttpResponse


class FarmerViewSet(viewsets.ModelViewSet):

    queryset = Person.objects.all()[:1000]
    serializer_class = FarmerSerializer

    # @action(methods=['post'], detail=True)
    # def set_password(self, request, pk=None):
    #     return Response("HI, It worked!")

class VillagesViewSet(viewsets.ModelViewSet):
    
    queryset = Village.objects.all()[:10]
    serializer_class = VillageSerializer

class BlockViewSet(viewsets.ModelViewSet):
    
    queryset = Block.objects.all()[:10]
    serializer_class = BlockSerializer




class FarmerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET farmer/:id/
    """
    queryset = Person.objects.all()
    serializer_class = FarmerSerializer

    def get(self, request, *args, **kwargs):
        try:
            a_farmer = self.queryset.get(pk=kwargs["pk"])
            # farmers_all = self.queryset.filter(id__gte=10, id__lte=20)
            return Response(FarmerSerializer(a_farmer, many=True).data)
        except Person.DoesNotExist:
            return Response(
                data={
                    "message": "Farmer with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )