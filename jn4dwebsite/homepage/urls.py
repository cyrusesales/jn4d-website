from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('view-products/<str:pk>', views.viewProducts, name="view-products"),
    path('view-color-products/<str:pk>', views.viewColorProducts, name="view-color-products"),
    path('view-specifications/<str:pk>', views.viewSpecifications, name="view-specifications"),
    path('sign-up', views.signUp, name="sign-up"),
]
