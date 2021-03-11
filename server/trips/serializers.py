from django.contrib.auth import get_user_model
from django.db.models import fields

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Trip


class UserSerializer(serializers.ModelSerializer):
    """Serializer for signup"""
    password1 = serializers.CharField(write_only=True, min_length=5,
                                      style={'input_type': 'password'},
                                      trim_whitespace=False
                                      )
    password2 = serializers.CharField(write_only=True, min_length=5,
                                      style={'input_type': 'password'},
                                      trim_whitespace=False
                                      )

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'email', 'username',
            'password1', 'password2',
        )
        read_only_fields = ('id',)

    def validate(self, attrs):
        """Validate user input"""
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError('Passwords must match')
        return attrs

    def create(self, validated_data):
        """Create serializer user"""
        validated_data.pop('password1')
        validated_data['password'] = validated_data.pop('password2')

        return get_user_model().objects.create_user(**validated_data)


class LogInSerializer(TokenObtainPairSerializer):
    """Serializer for generation token"""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = UserSerializer(user).data

        for key, value in user_data.items():
            if key != 'id':
                token[key] = value

        return token


class TripSerializer(serializers.ModelSerializer):
    """Serializer for trip objects"""

    class Meta:
        model = Trip
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated')


class NestedTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'
        depth = 1
