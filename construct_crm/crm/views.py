from datetime import datetime

from django.contrib.auth import login
from django.contrib.auth.views import LogoutView, LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse


def index(request):
    return render(request, 'crm/index.html')

