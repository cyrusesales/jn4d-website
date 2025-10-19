from django.urls import path
from . import views

urlpatterns = [
    path('', views.adminHome, name="adminpage"),
    path('manage-header/', views.manageHeader, name="manage-header"),
    path('edit-header/<str:pk>', views.editHeader, name="edit-header"),
    path('delete-header/<str:pk>', views.deleteHeader, name="delete-header"),
    path('manage-carousel/', views.manageCarousel, name="manage-carousel"),
    path('edit-carousel/<str:pk>', views.editCarousel, name='edit-carousel'),
    path('add-carousel/', views.addCarousel, name="add-carousel"),
    path('delete-carousel/<str:pk>', views.deleteCarousel, name="delete-carousel"),
    path('manage-categories/', views.manageCategories, name='manage-categories'),
    path('edit-categories/<str:pk>', views.editCategories, name='edit-categories'),
    path('add-categories/', views.addCategories, name='add-categories'),
    path('delete-categories/<str:pk>', views.deleteCategories, name="delete-categories"),
    path('add-products/<str:pk>', views.addProducts, name='add-products'),
    path('manage-products/<str:pk>', views.manageProducts, name='manage-products'),
    path('edit-products/<str:pk>', views.editProducts, name="edit-products"),
    path('delete-products/<str:pk>', views.deleteProducts, name="delete-products"),
]
