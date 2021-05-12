from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path('register/', register_page, name='register'),
    path('login/', login_page, name='login'),
    path('logout/', logout_user, name='logout'),

    path('', home, name='home'),
    path('user/', user_page, name='user_page'),
    path('account/', account_settings, name='account'),
    path('products/', products, name='products'),
    path('customer/<int:pk>/', customer, name='customer_detail'),
    path('create_order/<int:pk>/', create_order, name='create_order'),
    path('update_order/<int:pk>/', update_order, name='update_order'),
    path('delete_order/<int:pk>/', delete_order, name='delete_order'),

    path('reset_password/', auth_views.PasswordResetView.as_view(),
         name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
