# Django build-in
from django.http import HttpRequest, HttpResponse
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
# DRF
from rest_framework.views import APIView

# Local django
from accountants.models import Accountant, PaymentMark
from marks.models import AcceptedPlace
from .permissions import IsAccountantUser
from .serializers import AccountantProfileSerializer, AcceptedListSerializer, AddPaymentSerializers


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


class AcceptedList(generics.ListAPIView):
    serializer_class = AcceptedListSerializer
    queryset: AcceptedPlace = AcceptedPlace.objects.all().order_by('created')
    permission_classes = [IsAccountantUser, ]

    def get_queryset(self):
        user = self.request.query_params.get('user', None)
        from_date = self.request.query_params.get('from', None)
        to_date = self.request.query_params.get('to', None)
        if user is not None:
            queryset = self.queryset.filter(
                supervisor__username__icontains=user,
                action=AcceptedPlace.Status.accepted
            )
        if from_date is not None:
            queryset = self.queryset.filter(
                created__month__gte=from_date,
                action=AcceptedPlace.Status.accepted
            )
        if to_date is not None:
            queryset = self.queryset.filter(
                created__month__lte=to_date,
                action=AcceptedPlace.Status.accepted
            )
        if from_date and to_date is not None:
            queryset = self.queryset.filter(
                created__month__gte=from_date,
                created__month__lte=to_date,
                action=AcceptedPlace.Status.accepted)
        if from_date and user is not None:
            queryset = self.queryset.filter(
                supervisor__username__icontains=user,
                created__month__gte=from_date,
                action=AcceptedPlace.Status.accepted)
        if to_date and user is not None:
            queryset = self.queryset.filter(
                supervisor__username__icontains=user,
                created__month__lte=to_date,
                action=AcceptedPlace.Status.accepted)
        if from_date and to_date and user is not None:
            queryset = self.queryset.filter(
                supervisor__username__icontains=user,
                created__month__gte=from_date,
                created__month__lte=to_date,
                action=AcceptedPlace.Status.accepted)

        if user is None and from_date is None and to_date is None:
            queryset = self.queryset.filter(action=AcceptedPlace.Status.accepted)
        return queryset


class AddPayment(APIView):
    def get(self, request: HttpRequest):
        query = AcceptedPlace.objects.filter(is_paid=False, action=AcceptedPlace.Status.accepted)
        ser_data = AcceptedListSerializer(instance=query, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        ser_data = AddPaymentSerializers(data=request.data, context={'request': request})
        if ser_data.is_valid():
            accept_mark = ser_data.validated_data['accept_mark']
            mark = PaymentMark.objects.filter(accept_mark=accept_mark).exists()
            paying: AcceptedPlace = AcceptedPlace.objects.filter(id=accept_mark.id).first()

            if mark is False:
                if paying.is_paid is False:
                    paying.is_paid = True
                    paying.save()
                    ser_data.save()
                    return Response(data=ser_data.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({'Notification': 'This mark is paid'})
            else:
                return Response({'Notification': 'This mark is paid'})
        else:
            return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)



