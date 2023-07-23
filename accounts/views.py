# Python
import datetime
import random

# Django build-in
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

# DRF
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import BlacklistedToken


# Local django
from .models import OtpCode, User
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    UserRegisterSerializers,
    UserSerializer,
    UserLoginSerializer,
    UserUpdateSerializer,
    OtpCodeSerializer,
)


# Create your views here.


class UserRegister(APIView):
    serializer_class = UserRegisterSerializers

    def post(self, request):
        ser_data = UserRegisterSerializers(data=request.POST)
        if ser_data.is_valid():
            ser_data.create(validated_data=ser_data.validated_data)
            return Response(data=ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


# todo: this is can verifying account with send token to user email
# I have error key must be str, int , ... not __proxy__
# class UserRegisterVerify(APIView):
#     def get(self, request, token):
#         try:
#             user = User.objects.get(token=token)
#             user.is_active = True
#             user.save()
#             return Response({_('detail'): _('Email verified successfully.')}, status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             return Response({_('detail'): _('Invalid verification token.')}, status=status.HTTP_400_BAD_REQUEST)


class GetUser(APIView):
    serializer_class = UserSerializer

    def get(self, request):
        user = request.user
        print(user)
        ser_data = UserSerializer(instance=request.user)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class UserLogin(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request: HttpRequest):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        print(user)

        if user is not None:
            otp = OtpCode.objects.create(email=user.email, code=random.randint(1000, 9999))
            otp_code = otp.code
            otp.send_gmail(email=user.email, code=otp_code)

            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)
            return Response({'token': "Check your email box we send you a code "}, status=status.HTTP_200_OK)
        return Response({_('error'): _('Invalid credentials')}, status=status.HTTP_401_UNAUTHORIZED)


class UserLoginVerify(APIView):
    serializer_class = OtpCodeSerializer

    def post(self, request: HttpRequest):
        ser_data = OtpCodeSerializer(data=request.data)
        if ser_data.is_valid():
            user_code = ser_data.validated_data.get('code')
            try:
                db_code = OtpCode.objects.get(code=user_code)
            except OtpCode.DoesNotExist:
                return Response({_('error'): _('Invalid Code')}, status=status.HTTP_400_BAD_REQUEST)
            else:
                otp_date = db_code.created.minute + 2
                today_now = datetime.datetime.now().minute
                if otp_date < today_now:
                    db_code.delete()
                    return Response({'Time': 'Expired code'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    user = User.objects.filter(email__iexact=db_code.email).first()
                    refresh = RefreshToken.for_user(user)
                    token = str(refresh.access_token)
                    user.token = str(token)
                    user.save()
                    # token = Token.objects.get_or_create(user)

                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    authenticate(username=user.username, password=user.password)
                    db_code.delete()
                    return Response({'token': token}, status=status.HTTP_200_OK)

        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

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


class UserLogout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = request.user.token
        user = User.objects.get(token__exact=token)
        user.token = ''
        user.save()
        token = ''
        logout(request)
        print(request.user.is_authenticated)
        return Response("Successfully", status=status.HTTP_200_OK)
