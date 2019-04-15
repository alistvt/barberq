from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from mainapp.models import Barbery, UserProfile
from mainapp.serializers import (BarberyListSerializer, BarberyTimeSlotListSerializer,
                                 UserProfileSerializer, UserSignUpSerializer, ReservationSerializer)
from mainapp.permissions import IsOwner


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
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated, IsOwner, )


class UserReservationsView(generics.ListAPIView):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        user = self.request.user
        user_profile = UserProfile.objects.get(pk=user.pk)
        return user_profile.reservations
