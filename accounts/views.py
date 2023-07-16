import random

from django.contrib.auth import authenticate
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import OtpCode, User
from .serializers import UserRegisterSerializers, UserSerializer, UserLoginSerializer, UserUpdateSerializer


# Create your views here.

class UserRegister(APIView):
    serializer_class = UserRegisterSerializers

    def post(self, request):
        ser_data = UserRegisterSerializers(data=request.POST)
        if ser_data.is_valid():
            ser_data.create(validated_data=ser_data.validated_data)
            # user = ser_data.save()
            # token = RefreshToken.for_user(ser_data.save())
            # print(token)
            return Response(data=ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterVerify(generics.GenericAPIView):
    def get(self, request, token):
        try:
            user = User.objects.get(token=token)
            user.is_active = True
            user.save()
            return Response({_('detail'): _('Email verified successfully.')}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({_('detail'): _('Invalid verification token.')}, status=status.HTTP_400_BAD_REQUEST)


class GetUser(APIView):
    def get(self, request):
        user = request.user
        ser_data = UserSerializer(instance=request.user)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class UserLogin(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request: HttpRequest):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            otp = OtpCode.objects.create(email=user.email, code=random.randint(1000, 9999))
            otp_code = otp.code
            request.session['otp_code'] = otp_code

            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)
            return Response({'token': token}, status=status.HTTP_200_OK)
        return Response({_('error'): _('Invalid credentials')}, status=status.HTTP_401_UNAUTHORIZED)


Token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg5ODM3MzMwLCJpYXQiOjE2ODk0MDUzMzAsImp0aSI6Ijg2NGZiYTY3Y2ZhNjQxMzM5MWVhZGUzOTkxZjQwNTIyIiwidXNlcl9pZCI6Mn0.a5cl5MPdNyniwcFGTPkr3G50CE1ghkhLLEpZaXIOcYA'


class UserUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    lookup_field = 'pk'

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True  # Set partial=True
        return super().get_serializer(*args, **kwargs)

    def perform_update(self, serializer):
        if 'password' in self.request.data:
            raw_password = self.request.data['password']
            user = serializer.save()
            user.set_password(raw_password)
            user.save()

        else:
            serializer.save()
