from django.urls import path

from . import views

urlpatterns = [
    path('profile/<int:id>', views.AccountantProfileView.as_view(), name='accountant_profile'),
    path('accepted/', views.AcceptedList.as_view(), name='accountant_mark'),
    path('payment/', views.AddPayment.as_view(), name='payment'),
    path('payment-factor/', views.export_factor, name='factor'),
]
