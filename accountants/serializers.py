# DRF
from rest_framework import serializers

# Django local
from .models import Accountant


class AccountantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accountant
        fields = [
            'username',
            'email',
            'avatar',
            'user_type',
            'last_login',
        ]