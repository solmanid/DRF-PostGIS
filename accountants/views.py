# Django build-in
from django.http import HttpRequest
from rest_framework import status
from rest_framework.response import Response
# DRF
from rest_framework.views import APIView

# Local django
from accountants.models import Accountant
from .serializers import AccountantProfileSerializer


# Third party


class AccountantProfileView(APIView):
    """
    This view only show accountant user information
    """
    serializer_class = AccountantProfileSerializer

    def get(self, request: HttpRequest, id):
        user = Accountant.objects.filter(id=id).first()
        if user:
            ser_data = AccountantProfileSerializer(instance=user)
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response({'Error': 'User does not exists'}, status=status.HTTP_400_BAD_REQUEST)

