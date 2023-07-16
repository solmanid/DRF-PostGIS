from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.UserRegister.as_view(), name='user_register'),
    path('reg/verify/<str:token>', views.UserRegisterVerify.as_view(), name='user_verify'),
    path('login/', views.UserLogin.as_view(), name='user_login'),
    path('profile/', views.GetUser.as_view(), name='profile'),
    path('update/<int:pk>', views.UserUpdate.as_view(), name='update_user'),
]