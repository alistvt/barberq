from rest_framework import serializers
from .models import Barbery, TimeSlot, UserProfile


class BarberyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barbery
        fields = ('name', 'address',)


class TimeSlotListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ('barbery', 'start_time', 'duration', 'reserved', )


class BarberyTimeSlotListSerializer(serializers.ModelSerializer):
    time_slots = TimeSlotListSerializer(many=True)

    class Meta:
        model = TimeSlot
        fields = ('time_slots', )


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'first_name', 'last_name', 'password', )
