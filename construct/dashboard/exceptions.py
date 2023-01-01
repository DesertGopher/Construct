from typing import Optional
from django.shortcuts import render


def server_error_decorator(func):
    def wrapped(request, *args, **kwargs):
        # try:
            return func(request, *args, **kwargs)
        # except Exception as message:
        #     return render(request, 'dashboard/500.html', {'message': message})

    return wrapped
