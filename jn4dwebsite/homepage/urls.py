from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.homepage, name="homepage"),

    path('view-products/<str:pk>', views.viewProducts, name="view-products"),
    path('view-items/<str:pk>', views.viewItems, name="view-items"),
    path('view-specifications/<str:pk>', views.viewSpecifications, name="view-specifications"),

    path('add-to-cart/<str:pk>', views.addToCart, name="add-to-cart"),
    path('view-cart/<str:pk>', views.viewCart, name="view-cart"),
    path('update-quantity/<int:pk>', views.updateQuantity, name="update-quantity"),
    path('remove-item/<str:pk>', views.removeItem, name="remove-item"),
    path('checkout/<str:pk>', views.viewCheckout, name="checkout"),
    path('order-status-page/<str:pk>', views.orderStatusPage, name="order-status-page"),
    path('manage-voucher/<str:pk>', views.manageVoucher, name="manage-voucher"),


    path('sign-up', views.signUp, name="sign-up"),
    path('sign-in', views.signIn, name="sign-in"),
    path('logout/', views.signOut, name="sign-out"),
    path('profile/<str:pk>', views.viewUserProfile, name="view-user-profile"),
    path('edit-profile/<str:pk>', views.editUserProfile, name="edit-user-profile"),
    path('change-password/<str:pk>', views.changePassword, name="change-password"),
]
