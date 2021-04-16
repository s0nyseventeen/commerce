from django.http import HttpResponse
from django.shortcuts import redirect
from typing import Callable


def unauthenticated_user(view_func: Callable) -> Callable:

    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper


def allowed_users(allowed_roles: list = []) -> Callable:

    def decorator(view_func: Callable):  # for instance: we pass home() here

        def wrapper(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not allowed to view this page')

        return wrapper

    return decorator


def admin_only(view_func: Callable) -> Callable:

    def wrapper(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'customers':
            return redirect('accounts:user_page')
        if group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper

