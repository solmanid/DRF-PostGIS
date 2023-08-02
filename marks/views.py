# Django build-in
from django.contrib.gis.geos import Point
from django.http import HttpRequest
# DRF
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response

# Local django
from .models import PlacePoints
from .permissions import IsOwnerOrReadOnly
from .serializers import MarksListSerializers, MarksAddSerializers, UpdateMarkSerializer


class MarksList(ListAPIView):
    queryset = PlacePoints.objects.filter(status=True).order_by('created')
    serializer_class = MarksListSerializers

    def get(self, request, *args, **kwargs):
        if request.user.username:
            if request.user.is_supervisor is True:
                self.queryset = PlacePoints.objects.filter(is_accepted=False).order_by('created')
            if request.user.is_accountant is True:
                self.queryset = PlacePoints.objects.filter(is_accepted=True).order_by('created')
        return self.list(request, *args, **kwargs)


class AddMark(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = MarksAddSerializers

    def post(self, request: HttpRequest):
        ser_data = MarksAddSerializers(data=request.data)
        if ser_data.is_valid():
            lat = float(ser_data.validated_data['lat'])
            lng = float(ser_data.validated_data['lng'])

            points = Point(lng, lat)

            user = request.user
            PlacePoints.objects.create(
                user=user,
                description=ser_data.validated_data['description'],
                location=points,
            )
            return Response(ser_data.data, status=status.HTTP_201_CREATED)

        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateMark(RetrieveUpdateAPIView):
    queryset = PlacePoints.objects.all()
    serializer_class = UpdateMarkSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True  # Set partial=True
        return super().get_serializer(*args, **kwargs)

    def perform_update(self, serializer):
        instance = serializer.instance
        lat = self.request.data.get('lat')
        print(lat)
        lng = self.request.data.get('lng')
        if lat is None:
            serializer.save()
        else:
            lat = float(lat)
            lng = float(lng)
            loc = Point(lng, lat)
            instance.location = loc
            serializer.save()


class DeleteMark(RetrieveDestroyAPIView):
    queryset = PlacePoints.objects.all()
    serializer_class = UpdateMarkSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
