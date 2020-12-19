from rest_framework import serializers

from django.contrib.auth import get_user_model


class SignupSerializer(serializers.ModelSerializer):
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
