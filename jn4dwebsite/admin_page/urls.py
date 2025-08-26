from django.urls import path
from . import views

urlpatterns = [
    path('', views.adminhome, name="adminpage"),
    path('manage-header/', views.manage_header, name="manage-header"),
    path('edit_header/<str:pk>', views.edit_header, name="edit-header"),
    path('delete_header/<str:pk>', views.delete_header, name="delete-header"),
]
