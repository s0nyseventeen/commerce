from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
	path('register/', register_page, name='register'),
	path('login/', login_page, name='login'),
	path('logout/', logout_user, name='logout'),

	path('', home, name='home'),
	path('products/', products, name='products'),
	path('customer/<int:pk>/', customer, name='customer_detail'),
	path('create_order/<int:pk>/', create_order, name='create_order'),
	path('update_order/<int:pk>/', update_order, name='update_order'),
	path('delete_order/<int:pk>/', delete_order, name='delete_order'),
]
