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

    def post(self, request: HttpRequest):
        # Assuming you have already authenticated the user
        serializer = AcceptPlaceSerializer(data=request.data, context={'request': request})
        # mark: PlacePoints = serializer.validated_data['mark']
        if serializer.is_valid():
            mark: PlacePoints = serializer.validated_data['mark']
            check_user = AcceptedPlace.objects.filter(supervisor=request.user.id, mark=mark).exists()
            place: PlacePoints = PlacePoints.objects.filter(id=mark.id).first()

            if place.is_accepted is False:
                if check_user is False:
                    action = serializer.validated_data['action']
                    if action == '1':
                        accepted_place = serializer.save()
                        place.is_accepted = True
                        place.save()
                        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                    if action == '2':
                        accepted_place = serializer.save()
                        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
                    return Response({'error': 'some thing is wrong'})
                else:
                    return Response({'Error': 'You already one times created'})
            else:
                return Response({'Notification': 'This point is accepted'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
