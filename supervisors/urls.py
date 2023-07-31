from django.urls import path

from . import views

urlpatterns = [
    path('profile/<int:id>', views.SupervisorProfileView.as_view(), name='supervisor_profile'),
    path('reports/', views.ShowReportsView.as_view(), name='mark_for_supervisor'),
    path('accept/', views.AcceptPlace.as_view(), name='accept_mark'),
    path('accep/', views.Accept.as_view(), name='accept_mark'),
]
