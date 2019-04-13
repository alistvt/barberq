from rest_framework import generics
from mainapp.models import Barbery
from mainapp.serializers import BarberyListSerializer, BarberyTimeSlotListSerializer


class BarberyListView(generics.ListAPIView):
    queryset = Barbery.objects.all()
    serializer_class = BarberyListSerializer
    permission_classes = []


class BarberyProfileView(generics.RetrieveAPIView):
    queryset = Barbery.objects.all()
    serializer_class = BarberyListSerializer
    permission_classes = []


# TODO is this true or not?!
class BarberyTimeSlotsListView(generics.RetrieveAPIView):
    queryset = Barbery.objects.all()
    serializer_class = BarberyTimeSlotListSerializer
    permission_classes = []
