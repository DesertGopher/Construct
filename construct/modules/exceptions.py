from .custom_loguru import *
from .orders_logs import *
from django.shortcuts import render


def server_error_decorator(func):
    def wrapped(*args, **kwargs):
        try:
            log_request_created(server_logger, *args, **kwargs)
            result = func(*args, **kwargs)
            log_request_completed(server_logger, result, *args, **kwargs)
            return result
        except Exception as message:
            log_request_error(server_logger, message)
            return func(*args, **kwargs)
            # return render(request, 'dashboard/500.html', {'message': message})

    return wrapped


def orders_decorator(func):
    def wrapped(request, *args, **kwargs):
        try:
            log_request_created(orders_logger, *args, **kwargs)
            result = str(
                "Пользователь "
                + str(request.user.username)
                + " сделал заказ в приложении"
            )
            log_request_completed(orders_logger, result, *args, **kwargs)
            return func(request, *args, **kwargs)
        except Exception as message:
            log_request_error(orders_logger, message)
            return func(request, *args, **kwargs)
            # return render(request, 'dashboard/500.html', {'message': message})

    return wrapped


def is_active_decorator(func):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_active:
            message = "Пользователь не авторизован"
            log_request_error(server_logger, message)
            return render(request, "dashboard/401.html")
        return func(request, *args, **kwargs)

    return wrapped


def is_staff_decorator(func):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_staff:
            message = str("Пользователь " + str(request.user.username) + " не менеджер")
            log_request_error(server_logger, message)
            return render(request, "dashboard/403.html")
        return func(request, *args, **kwargs)

    return wrapped


def is_superuser_decorator(func):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_superuser:
            message = str(
                "Пользователь " + str(request.user.username) + " не администратор"
            )
            log_request_error(server_logger, message)
            return render(request, "dashboard/403.html")
        return func(request, *args, **kwargs)

    return wrapped
