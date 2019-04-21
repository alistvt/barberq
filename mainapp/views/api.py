from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from mainapp.models import Barbery, UserProfile, TimeSlot
from mainapp.serializers import (BarberyListSerializer, BarberyTimeSlotListSerializer,
                                 UserProfileSerializer, UserSignUpSerializer, ReservationSerializer,
                                 UserPasswordSerializer, UserReserveTimeSlotSerializer,
                                 UserCancelReservationSerializer,)
from mainapp.permissions import IsOwnerOfReservation


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


class UserSignUpView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSignUpSerializer


class UserActionsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        user = self.request.user
        user_profile = UserProfile.objects.get(pk=user.pk)
        return user_profile


class UserReservationsView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        user_profile = UserProfile.objects.get(pk=user.pk)
        return user_profile.reservations


class UserChangePasswordView(generics.UpdateAPIView):
    serializer_class = UserPasswordSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        user = self.request.user
        user_profile = UserProfile.objects.get(pk=user.pk)
        return user_profile


class UserReserveTimeSlotView(generics.CreateAPIView):
    serializer_class = UserReserveTimeSlotSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserCancelReservationView(generics.DestroyAPIView):
    serializer_class = UserCancelReservationSerializer
    permission_classes = (IsAuthenticated, IsOwnerOfReservation, )

    def perform_destroy(self, instance):
        # TODO : Logic on serializers?
        if not instance.can_cancel():
            raise serializers.ValidationError("time has passed and can't be cancelled.")
        instance.cancel()
        return super().perform_destroy(instance)
