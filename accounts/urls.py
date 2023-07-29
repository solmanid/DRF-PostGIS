from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from . import views

# from .views import UserViewSet

# router = routers.DefaultRouter()
# router.register(r'', UserViewSet)

urlpatterns = [
    # path('token/', TokenObtainSlidingView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('ver/', TokenVerifyView.as_view(), name='ver'),
    path('register/', views.UserRegister.as_view(), name='user_register'),
    path('login/', views.UserLogin.as_view(), name='user_login'),
    path('login/verify/', views.UserLoginVerify.as_view(), name='user_login_verify'),
    path('update/<int:id>', views.UserUpdate.as_view(), name='update_user'),
    path('update/s/<int:id>', views.EmployeeUpdate.as_view(), name='update_supervisor'),
    path('pass-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # path('', include(router.urls), name='user'),
    # re_path('auth/', include('rest_auth.urls'), name='auth'),
]
