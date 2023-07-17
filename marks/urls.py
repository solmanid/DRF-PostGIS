from django.urls import path

from . import views

urlpatterns = [
    path('', views.MarksList.as_view(), name='list_mark'),
    path('add/', views.AddMark.as_view(), name='create_list_mark'),
    path('edit/<int:pk>', views.UpdateMark.as_view(), name='edit_mark'),
    path('del/<int:pk>', views.DeleteMark.as_view(), name='del_mark'),
]