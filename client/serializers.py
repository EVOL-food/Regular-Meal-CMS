from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import Profile
from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name',
                  'phone_number', 'address', 'gender')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'profile')
        related_fields = ['profile']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        profile_data = validated_data.pop('profile')
        user.profile.first_name = profile_data['first_name']
        user.profile.last_name = profile_data['last_name']
        user.profile.phone_number = profile_data['phone_number']
        user.profile.address = profile_data['address']
        user.profile.gender = profile_data['gender']
        user.save()
        user.profile.save()

        return user
