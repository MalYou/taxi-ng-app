from django.contrib.auth import get_user_model

from rest_framework import generics

from . import serializers


class SignUpView(generics.CreateAPIView):
    """Endpoint to create a new user"""
    queryset = get_user_model().objects.all()
    serializer_class = serializers.SignupSerializer
