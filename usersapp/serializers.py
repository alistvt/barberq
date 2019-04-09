from rest_framework import serializers
from mainapp.models import Barbery, UserProfile, TimeSlot, Reservation


class BarberySerializer(serializers.ModelSerializer):
    class Meta:
        model = Barbery
        fields = ('name', 'address', )


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', )


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ('barbery', 'start_time', 'duration', )


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ()
