from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('view-products/<str:pk>', views.viewProducts, name="view-products"),
    path('view-color-products/<str:pk>', views.viewColorProducts, name="view-color-products"),
    path('view-specifications/<str:pk>', views.viewSpecifications, name="view-specifications"),
    path('sign-up', views.signUp, name="sign-up"),
    path('sign-in', views.signIn, name="sign-in"),
    path('logout/', views.signOut, name="sign-out"),
    path('profile/<str:pk>', views.viewUserProfile, name="view-user-profile"),
    path('edit-profile/<str:pk>', views.editUserProfile, name="edit-user-profile"),
    path('change-password/<str:pk>', views.changePassword, name="change-password"),
]
