# DRF
from django.http import HttpRequest
from rest_framework import serializers

from marks.models import AcceptedPlace
# Django local
from .models import Accountant, PaymentMark


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


class AcceptedListSerializer(serializers.ModelSerializer):
    supervisor = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = AcceptedPlace
        fields = '__all__'

        extra_kwargs = {
            # 'supervisor': {'read_only': True},
            'is_paid': {'read_only': True},
        }


class AddPaymentSerializers(serializers.ModelSerializer):
    class Meta:
        model = PaymentMark
        fields = '__all__'
        extra_kwargs = {
            'accountant': {'read_only': True}
        }

    def create(self, validated_data):
        request: HttpRequest = self.context.get('request')
        if request is not None:
            user = Accountant.objects.filter(id=request.user.id).first()
            payment = PaymentMark.objects.create(
                accountant=user,
                accept_mark=validated_data.get('accept_mark'),
                price=validated_data['price']
            )
            return payment
