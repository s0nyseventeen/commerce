from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter


def register_page(request):
	if request.user.is_authenticated:
		return redirect('accounts:home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, f'Account was created for {user}')
				return redirect('accounts:login')
		return render(request, 'accounts/register.html', {'form': form})


def login_page(request):
	if request.user.is_authenticated:
		return redirect('accounts:home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password')
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('accounts:home')
			else:
				messages.info(request, 'Username or password is incorrect')
		return render(request, 'accounts/login.html')


def logout_user(request):
	logout(request)
	return redirect('accounts:login')


@login_required(login_url='accounts:login')
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


@login_required(login_url='accounts:login')
def products(request):
	products = Product.objects.all()
	return render(request, 'accounts/products.html', {'products': products})


@login_required(login_url='accounts:login')
def customer(request, pk):
	customer = Customer.objects.get(id=pk)
	customer_orders = customer.order_set.all()  # Customer model get its orders
	total_orders = customer_orders.count()
	my_filter = OrderFilter(request.GET, queryset=customer_orders)
	customer_orders = my_filter.qs
	context = {
		'customer': customer,
		'customer_orders': customer_orders,
		'total_orders': total_orders,
		'my_filter': my_filter
	}
	return render(request, 'accounts/customer.html', context)


@login_required(login_url='accounts:login')
def create_order(request, pk):
	order_form_set = inlineformset_factory(
		Customer, 
		Order, 
		fields=('product', 'status'),
		extra=5  # how many fields we want insta to be on the page
	)
	customer = Customer.objects.get(id=pk)

	# queryset.none() - to hide already ordered items
	formset = order_form_set(
		queryset=Order.objects.none(),
		instance=customer
	)
	# form = OrderForm(initial={'customer': customer})
	if request.method == 'POST':
		# print('Printing POST:', request.POST)
		# form = OrderForm(request.POST)
		formset = order_form_set(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('accounts:home')
	return render(request, 'accounts/order_form.html', {'formset': formset})


@login_required(login_url='accounts:login')
def update_order(request, pk):
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)
	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('accounts:home')
	return render(request, 'accounts/order_form.html', {'form': form})


@login_required(login_url='accounts:login')
def delete_order(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == 'POST':
		order.delete()
		return redirect('accounts:home')
	return render(request, 'accounts/delete_order.html', {'order': order})
