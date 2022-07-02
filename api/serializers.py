from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        nickname = validated_data.get('nickname')
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = User(
            nickname=nickname,
            email=email
        )
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class VeganSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vegan
        fields = '__all__'


class CO2CalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CO2Cal
        fields = '__all__'


class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = '__all__'


class GroupPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupPurchase
        fields = '__all__'



