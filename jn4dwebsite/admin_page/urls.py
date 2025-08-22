from django.urls import path
from . import views

urlpatterns = [
    path('', views.adminhome, name="adminpage"),
    path('manage-header/', views.manage_header, name="manage-header")
]
