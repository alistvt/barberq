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
        fields = ('username', 'email', 'first_name', 'last_name', )


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


class UserPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=200)
    # password2 = serializers.CharField(max_length=200)

    def validate(self, data):
        # if data['password'] != data['password2']:
        #     raise serializers.ValidationError("passwords doesn't match.")
        # data.pop('password2')
        return data

    def update(self, instance, validated_data):
        # password =
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


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


class UserReserveTimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ()

    def update(self, instance, validated_data):
        if not instance.can_be_reserved():
            raise serializers.ValidationError("This slot is reserved.")
        user = validated_data['user']
        user_profile = UserProfile.objects.get(pk=user.pk)
        return instance.reserve(user_profile)


class UserCancelReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('slot', 'user', )
