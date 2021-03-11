from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import generics, viewsets, permissions

from rest_framework_simplejwt.views import TokenObtainPairView

from . import serializers
from . import models


class SignUpView(generics.CreateAPIView):
    """Endpoint to create a new user"""
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer


class LogInView(TokenObtainPairView):
    """Endpoint for getting a valid token"""
    serializer_class = serializers.LogInSerializer


class TripView(viewsets.ReadOnlyModelViewSet):
    """Endpoint for getting Trips or a specific trip"""
    lookup_field = 'id'
    lookup_url_kwarg = 'trip_id'
    serializer_class = serializers.NestedTripSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user

        if user.group == 'driver':
            return models.Trip.objects.filter(
                Q(status=models.Trip.REQUESTED | Q(driver=user))
            )

        if user.group == 'rider':
            return models.Trip.filter(rider=user)

        return models.Trip.objects.none()

