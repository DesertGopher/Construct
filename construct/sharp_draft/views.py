from django.shortcuts import render
from api.models import Profile
from modules.exceptions import *
from .forms import EncodeForm
from .encrypt import create_xml


@server_error_decorator
@is_staff_decorator
def index(request):
    profile = Profile.objects.get(client_id=request.user)
    return render(request, 'sharp_draft/index.html', {'profile': profile})


@server_error_decorator
@is_staff_decorator
def create_plate(request):
    profile = Profile.objects.get(client_id=request.user)
    return render(request, 'sharp_draft/create_plate.html', {'profile': profile})


@server_error_decorator
@is_staff_decorator
def xml_encode(request):
    profile = Profile.objects.get(client_id=request.user)
    if request.method == "POST":
        form = EncodeForm(request.POST)
        if form.is_valid():
            p_profile = form['profile'].value()
            p_length = form['length'].value()
            p_material = form['material'].value()
            p_pname = form['project_name'].value()
            p_ename = form['element_name'].value()
            create_xml(length=p_length,
                    profile=p_profile,
                    material=p_material,
                    project_name=p_pname,
                    element_name=p_ename,
                    user=request.user)
    else:
        form = EncodeForm()
    return render(request, 'sharp_draft/xml_encode.html', {'profile': profile,
                                                           'form': form})
