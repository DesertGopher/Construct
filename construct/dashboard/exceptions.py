from functools import wraps
from loguru import logger

from django.shortcuts import render
from django.conf import settings

logger.add(settings.PATH_LOG / "server_logs.txt", diagnose=False, backtrace=False,
           format="{time} {level} {message}", level="DEBUG", rotation="1 MB",
           retention='7 days', compression="zip",
           filter=lambda record: "view" in record["extra"])
ex_logger = logger.bind(view=True)


def exception_resolver():
    pass


def server_error_decorator(func):

    def wrapped(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except Exception as message:
            ex_logger.exception(message)
            return render(request, 'dashboard/500.html', {'message': message})

    return wrapped


def is_active_decorator(func):

    def wrapped(request, *args, **kwargs):
        if not request.user.is_active:
            ex_logger.info(str('Пользователь не авторизован'))
            return render(request, 'dashboard/401.html')
        return func(request, *args, **kwargs)

    return wrapped


def is_staff_decorator(func):

    def wrapped(request, *args, **kwargs):
        if not request.user.is_staff:
            ex_logger.info(str('Пользователь ' + str(request.user.username) + ' не менеджер'))
            return render(request, 'dashboard/403.html')
        return func(request, *args, **kwargs)

    return wrapped


def is_superuser_decorator(func):

    def wrapped(request, *args, **kwargs):
        if not request.user.is_superuser:
            ex_logger.info(str('Пользователь ' + str(request.user.username) + ' не администратор'))
            return render(request, 'dashboard/403.html')
        return func(request, *args, **kwargs)

    return wrapped
