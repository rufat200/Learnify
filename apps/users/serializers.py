from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'full_name']


class UserCreateSerializer(BaseUserCreateSerializer):
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ['email', 'password', 'role', 'full_name']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            full_name=validated_data['full_name']
        )
        return user
