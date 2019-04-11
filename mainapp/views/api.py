from rest_framework import generics
from mainapp.models import Barbery
from mainapp.serializers import BarberySerializer


class BarberyListView(generics.ListAPIView):
    queryset = Barbery.objects.all()
    serializer_class = BarberySerializer
    permission_classes = []
