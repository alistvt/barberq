from rest_framework import serializers
from .models import Barbery, TimeSlot, UserProfile, Reservation
from django.utils.translation import ugettext_lazy as _


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
    confirm_password = serializers.CharField(max_length=200, required=True, label=_('confirm password'),
                                             help_text=_('confirm password'), write_only=True)

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'confirm_password', )
        extra_kwargs = {
            'email': {
                'required': True,
            },
            'password': {
                'write_only': True,
            }
        }

    def validate(self, attrs):
        confirm_password = attrs.pop('confirm_password', None)
        password = attrs.get('password')
        if confirm_password != password:
            raise serializers.ValidationError(_('passwords doesn\'t match.'))
        return attrs

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
        fields = ('reserved', 'start_time', 'duration', )
        extra_kwargs = {
            'reserved': {
                'read_only': True,
            },
            'start_time': {
                'read_only': True,
            },
            'duration': {
                'read_only': True,
            },
        }

    def update(self, instance, validated_data):
        if not instance.can_be_reserved():
            raise serializers.ValidationError("This slot is reserved.")
        user = validated_data['user']
        user_profile = UserProfile.objects.get(pk=user.pk)
        return instance.reserve(user_profile)
