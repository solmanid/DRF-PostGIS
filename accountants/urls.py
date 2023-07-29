from django.urls import path

from . import views

urlpatterns = [
    path('profile/<int:id>', views.AccountantProfileView.as_view(), name='accountant_profile')

]
