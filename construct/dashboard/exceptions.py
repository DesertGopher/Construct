from typing import Optional
from django.shortcuts import render
from functools import wraps
from django.core.exceptions import PermissionDenied


def server_error_decorator(func):

    def wrapped(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except Exception as message:
            return render(request, 'dashboard/500.html', {'message': message})

    return wrapped


def is_active_decorator(func):

    def wrapped(request, *args, **kwargs):
        if not request.user.is_active:
            return render(request, 'dashboard/401.html')
        return func(request, *args, **kwargs)

    return wrapped


def is_staff_decorator(func):

    def wrapped(request, *args, **kwargs):
        if not request.user.is_staff:
            return render(request, 'dashboard/403.html')
        return func(request, *args, **kwargs)

    return wrapped


def is_superuser_decorator(func):

    def wrapped(request, *args, **kwargs):
        if not request.user.is_superuser:
            return render(request, 'dashboard/403.html')
        return func(request, *args, **kwargs)

    return wrapped
