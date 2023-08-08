# Python
import datetime
import random

# Django build-in
from django.contrib.auth import authenticate, logout
from django.contrib.auth.hashers import check_password
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
# DRF
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

# Local django
from accountants.models import Accountant
from supervisors.models import Supervisor
from .models import OtpCode, User
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    UserRegisterSerializers,
    UserLoginSerializer,
    UserUpdateSerializer,
    OtpCodeSerializer,
    EmployeeUpdateSerializers,
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

class UserLogin(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request: HttpRequest):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'user': 'dos not exist'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # if user is not None:
            if user.user_type == 'Supervisor':
                if user.last_login is None:
                    return Response({'Notification': 'set a new password', 'User': user.id}, status=status.HTTP_200_OK)
                else:
                    refresh = RefreshToken.for_user(user)
                    token = str(refresh.access_token)
                    user.token = str(token)
                    user.refresh_token = str(refresh)
                    user.save()
                    # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return Response({'Token': token, 'refresh': str(refresh)}, status=status.HTTP_200_OK)
            if user.user_type == 'Accountant':
                if user.last_login is None:
                    return Response({'Notification': 'set a new password', 'User': user.id}, status=status.HTTP_200_OK)
                else:
                    refresh = RefreshToken.for_user(user)
                    token = str(refresh.access_token)
                    user.token = str(token)
                    user.refresh_token = str(refresh)
                    user.save()
                    # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return Response({'Token': token, 'refresh': str(refresh)}, status=status.HTTP_200_OK)
            if user.user_type == 'People':
                otp = OtpCode.objects.create(email=user.email, code=random.randint(1000, 9999))
                otp_code = otp.code
                otp.send_gmail(email=user.email, code=otp_code)

                refresh = RefreshToken.for_user(user)
                token = str(refresh.access_token)
                return Response({'token': "Check your email box we send you a code "}, status=status.HTTP_200_OK)
            else:
                return Response({_('error'): _('Invalid credentials')}, status=status.HTTP_401_UNAUTHORIZED)


class UserLoginVerify(APIView):
    serializer_class = OtpCodeSerializer

    def post(self, request: HttpRequest):
        ser_data = OtpCodeSerializer(data=request.data)
        if ser_data.is_valid():
            user_code = int(ser_data.validated_data.get('code'))
            try:
                db_code = OtpCode.objects.filter(code=user_code).first()
            except OtpCode.DoesNotExist:
                return Response({'error': 'Invalid Code'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if db_code:
                    otp_date = db_code.created.minute + 2
                    today_now = datetime.datetime.now().minute
                else:
                    return Response({"Error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)
                if otp_date < today_now:
                    db_code.delete()
                    return Response({'Time': 'Expired code'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    user = User.objects.filter(email__iexact=db_code.email).first()
                    refresh = RefreshToken.for_user(user)
                    token = str(refresh.access_token)
                    user.token = str(token)
                    user.refresh_token = str(refresh)
                    user.save()
                    # token = Token.objects.get_or_create(user)

                    # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    authenticate(username=user.username, password=user.password)
                    db_code.delete()
                    return Response({'token': token, 'refresh': str(refresh)}, status=status.HTTP_200_OK)

        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = EmployeeUpdateSerializers
    lookup_field = 'id'

    def get_queryset(self):
        return User.objects.none()

    def put(self, request, id):
        super_user = Supervisor.objects.filter(id=id).first()
        accountant_user = Accountant.objects.filter(id=id).first()
        user: User = None
        if super_user is not None:
            user = super_user
        if accountant_user is not None:
            user = accountant_user

        if user is None:
            return Response({'Error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            ser_data = EmployeeUpdateSerializers(instance=user, data=request.data)
            if ser_data.is_valid(raise_exception=True):
                check_pass = user.check_password(ser_data.validated_data['password'])
                if check_pass:
                    refresh = RefreshToken.for_user(user)
                    token = str(refresh.access_token)
                    user.token = str(token)
                    user.refresh_token = str(refresh)
                    user.save()
                    ser_data.save()

                    return Response({'Token': user.token}, status=status.HTTP_200_OK)
                else:
                    return Response({'Error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super().get_serializer(*args, **kwargs)

    def perform_update(self, serializer):

        if 'password' in self.request.data:
            raw_password = self.request.data['password']
            user = serializer.save()
            user.set_password(raw_password)
            user.save()

        else:
            serializer.save()


# class UserLogout(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         token = request.user.token
#         user = User.objects.get(token__exact=token)
#         user.token = ''
#         user.save()
#         token = ''
#         logout(request)
#         print(request.user.is_authenticated)
#         return Response("Successfully", status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Blacklist the token to invalidate it
        try:
            token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
            # Here, you may add more logic to invalidate the token or do other clean-up tasks if needed.
        except KeyError:
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_400_BAD_REQUEST)
        logout(request)
        return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserViewSetSerializers
#
#     def perform_create(self, serializer):
#         self.serializer_class.hash_password(self=self, ser_data=serializer)
#
#     def perform_update(self, serializer):
#         self.serializer_class.hash_password(self=self, ser_data=serializer)
#
#     def get_permissions(self):
#         permission_classes = []
#         if self.action == 'create':
#             permission_classes = [AllowAny]
#         elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
#             permission_classes = [IsLoggedInUserOrAdmin]
#         elif self.action == 'list' or self.action == 'destroy':
#             permission_classes = [IsAdminUser]
#         return [permission() for permission in permission_classes]
