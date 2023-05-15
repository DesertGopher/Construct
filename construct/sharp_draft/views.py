from django.http.response import FileResponse
from django.shortcuts import render

from api.models import Profile
from modules.exceptions import *

from .encrypt import create_xml
from .forms import EncodeForm


@server_error_decorator
@is_staff_decorator
def index(request):
    profile = Profile.objects.get(client_id=request.user)
    return render(request, "sharp_draft/index.html", {"profile": profile})


@server_error_decorator
@is_staff_decorator
def create_plate(request):
    profile = Profile.objects.get(client_id=request.user)
    return render(request, "sharp_draft/create_plate.html", {"profile": profile})


@server_error_decorator
@is_staff_decorator
def xml_encode(request):
    profile = Profile.objects.get(client_id=request.user)
    if request.method == "POST":
        form = EncodeForm(request.POST)
        if form.is_valid():
            p_profile = form["profile"].value()
            p_length = form["length"].value()
            p_material = form["material"].value()
            p_proj_name = form["project_name"].value()
            p_elem_name = form["element_name"].value()
            obj = create_xml(
                length=p_length,
                profile=p_profile,
                material=p_material,
                project_name=p_proj_name,
                element_name=p_elem_name,
                user=request.user,
            )
            print(obj["name"])
            return FileResponse(
                open(obj["path"], "rb"), as_attachment=True, filename=obj["name"]
            )
    else:
        form = EncodeForm()
    return render(
        request, "sharp_draft/xml_encode.html", {"profile": profile, "form": form}
    )
