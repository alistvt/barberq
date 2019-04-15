from rest_framework import serializers
from .models import Barbery, TimeSlot, UserProfile, Reservation


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


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'first_name', 'last_name', 'password', )

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
        # user = user_serializer.object


class BarberyTimeSlotReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barbery
        fields = ('name', 'address', 'email', )


class TimeSlotReservationSerializer(serializers.ModelSerializer):
    barbery = BarberyTimeSlotReservationSerializer(read_only=True)

    class Meta:
        model = TimeSlot
        fields = ('barbery', 'start_time', 'duration', )


class ReservationSerializer(serializers.ModelSerializer):
    slot = TimeSlotReservationSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = ('slot', )
