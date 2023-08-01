# Django build-in
from django.http import HttpRequest
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# DRF
from rest_framework.views import APIView

from accounts.permissions import IsOwnerOrReadOnly
from marks.models import AcceptedPlace
from marks.models import PlacePoints
from marks.serializers import MarksListSerializers
# Local django
from supervisors.models import Supervisor
from .permissions import IsSupervisorUser
from .serializers import SupervisorProfileSerializer, AcceptPlaceSerializer


# Third party


class SupervisorProfileView(APIView):
    """
    This view only show accountant user information
    """
    serializer_class = SupervisorProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request: HttpRequest, id):
        user = Supervisor.objects.filter(id=id).first()
        if user:
            ser_data = SupervisorProfileSerializer(instance=user)
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response({'Error': 'User does not exists'}, status=status.HTTP_400_BAD_REQUEST)


class ShowReportsView(generics.ListAPIView):
    permission_classes = [IsSupervisorUser]
    serializer_class = MarksListSerializers
    queryset = PlacePoints.objects.filter(status=True).order_by('created')


class Accept(APIView):
    serializer_class = AcceptPlaceSerializer
    permission_classes = [
        IsSupervisorUser
    ]

    def get(self, request: HttpRequest):
        query = AcceptedPlace.objects.filter(supervisor=request.user.id)
        ser_data = AcceptPlaceSerializer(instance=query, many=True)
        return Response(data=ser_data.data)

    def post(self, request):
        # Assuming you have already authenticated the user
        serializer = AcceptPlaceSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            mark: PlacePoints = serializer.validated_data['mark']
            place = PlacePoints.objects.get(id=mark.id)
            if place.is_accepted is False and mark is not None:
                place.is_accepted = True
                place.save()
                serializer.create(serializer.validated_data)
                accepted_place = serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'Error': 'Mark does not exists or some one accepted '})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
