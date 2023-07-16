# Django Build-in
from django.utils.crypto import get_random_string
from django.utils.encoding import force_str
# DRF
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

# Local Django
from utils.email_service import send_email
from .models import User, OtpCode


class UserRegisterSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
            # 'email_active_code',
        ]

        extra_kwargs = {
            'email': {'required': True},
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Password must be match")
        return data

    def create(self, validated_data):
        del validated_data['password2']

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            email_active_code=get_random_string(72),

        )
        user.set_password(validated_data['password'])
        user.save()
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        user.token = str(token)
        user.refresh_token = str(refresh)
        # user.is_active = False
        user.save()
        send_email(
            subject='Account Verify',
            to=validated_data['email'],
            context={'token': str(token)},
            template_name='emails/reset_pass.html')
        return {
            'user': user,
            'token': token,
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'avatar',
            'first_name',
            'last_name',
            'is_staff',
            'is_active',
        ]


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',

        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'avatar'
        ]


class OtpCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtpCode
        fields = [
            'code'
        ]
