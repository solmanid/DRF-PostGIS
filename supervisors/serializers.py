# DRF
from rest_framework import serializers

from marks.models import AcceptedPlace
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


class AcceptPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcceptedPlace
        fields = '__all__'

        extra_kwargs = {
            'supervisor': {'read_only': True},
            'is_paid': {'read_only': True},
        }

        # def show_own_accept(self):
        #     request = self.context.get('request')
        #     own_mark = self.model.objects.filter(supervisor=request.user.id)
        #     return own_mark

    def create(self, validated_data):
        request = self.context.get('request')

        user = Supervisor.objects.filter(username=request.user.username).first()
        print(user)

        accepted_place = AcceptedPlace.objects.create(
            supervisor=user,
            description=validated_data['description'],
            mark=validated_data['mark'],
            mark_id=validated_data['mark'].id,
        )

        return accepted_place
