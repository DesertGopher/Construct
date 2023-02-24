from functools import wraps
from typing import List

from loguru import logger
from .custom_loguru import *
from django.shortcuts import render
from django.db import IntegrityError, DataError
from django.core.exceptions import EmptyResultSet, ObjectDoesNotExist, MultipleObjectsReturned

from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, ParseError


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


def is_active_decorator(func):

    def wrapped(request, *args, **kwargs):
        if not request.user.is_active:
            # ex_logger.info(str('Пользователь не авторизован'))
            return render(request, 'dashboard/401.html')
        return func(request, *args, **kwargs)

    return wrapped


def is_staff_decorator(func):

    def wrapped(request, *args, **kwargs):
        if not request.user.is_staff:
            # ex_logger.info(str('Пользователь ' + str(request.user.username) + ' не менеджер'))
            return render(request, 'dashboard/403.html')
        return func(request, *args, **kwargs)

    return wrapped


def is_superuser_decorator(func):

    def wrapped(request, *args, **kwargs):
        if not request.user.is_superuser:
            # ex_logger.info(str('Пользователь ' + str(request.user.username) + ' не администратор'))
            return render(request, 'dashboard/403.html')
        return func(request, *args, **kwargs)

    return wrapped
