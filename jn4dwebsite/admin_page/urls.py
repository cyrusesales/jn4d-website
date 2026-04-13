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
    
    path('manage-item/<str:pk>', views.manageItem, name='manage-item'),
    path('add-item/<str:pk>', views.addItem, name="add-item"),
    path('edit-item/<str:pk>', views.editItem, name='edit-item'),
    path('delete-item/<str:pk>', views.deleteItem, name='delete-item'),
    path('change-product-size/<str:pk>', views.changeProductSize, name='change-product-size'),

    path('manage-item-images/<str:pk>', views.manageItemImages, name='manage-item-images'),

    path('edit-placeholder/<str:pk>', views.editPlaceholder, name='edit-placeholder'),
    path('add-placeholder/', views.addPlaceholder, name='add-placeholder'),
    path('delete-placeholder/<str:pk>', views.deletePlaceholder, name='delete-placeholder'),

    path('manage-users/', views.manageUsers, name='manage-users'),
    path('changeUserStatus/<str:pk>', views.changeUserStatus, name='change-user-status'),
    path('change-user-role/<str:pk>', views.changeUserRole, name='change-user-role'),

    path('manage-product-size/', views.manageProductSize, name='manage-product-size'),
    path('edit-product-size/<str:pk>', views.editProductSize, name='edit-product-size'),
    path('add-product-size/', views.addProductSize, name='add-product-size'),
    path('delete-product-size/<str:pk>', views.deleteProductSize, name='delete-product-size'),

    path('manage-size-term/<str:pk>', views.manageSizeTerm, name='manage-size-term'),
    path('add-size-term/<str:pk>', views.addSizeTerm, name='add-size-term'),
    path('edit-size-term/<str:pk>', views.editSizeTerm, name='edit-size-term'),
    path('delete-size-term/<str:pk>', views.deleteSizeTerm, name='delete-size-term'),
    path('get-size-term/', views.getSizeTerm, name='get_size_term'),
]
