from django.shortcuts import render, redirect

from .models import *
from .forms import OrderForm


def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()
	total_customers = customers.count()
	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	context = {
		'orders': orders,
		'customers': customers,
		'total_customers': total_customers,
		'total_orders': total_orders,
		'delivered': delivered,
		'pending': pending
	}
	return render(request, 'accounts/homepage.html', context)


def products(request):
	products = Product.objects.all()
	context = {
		'products': products
	}
	return render(request, 'accounts/products.html', context)


def customer(request, pk):
	customer = Customer.objects.get(id=pk)
	customer_orders = customer.order_set.all()  # Customer model get its orders
	total_orders = customer_orders.count()
	context = {
		'customer': customer,
		'customer_orders': customer_orders,
		'total_orders': total_orders
	}
	return render(request, 'accounts/customer.html', context)


def create_order(request):
	form = OrderForm
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('accounts:home')
	context = {
		'form': form
	}
	return render(request, 'accounts/order_form.html', context)


def update_order(request, pk):
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)
	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('accounts:home')
	context = {
		'form': form
	}
	return render(request, 'accounts/order_form.html', context)


def delete_order(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == 'POST':
		order.delete()
		return redirect('accounts:home')
	context = {
		'order': order
	}
	return render(request, 'accounts/delete_order.html', context)
