# DRF
from rest_framework import serializers

# Django local
from .models import Supervisor


class SupervisorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supervisor
        fields = [
            'username',
            'email',
            'avatar',
            'user_type',
            'last_login',
        ]


