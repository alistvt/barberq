from rest_framework import serializers
from .models import Barbery


class BarberySerializer(serializers.ModelSerializer):
    class Meta:
        model = Barbery
        fields = ('name', 'address',)
