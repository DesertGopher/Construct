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
    kir = ('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    if request.method == "POST":
        form = EncodeForm(request.POST)
        if form.is_valid():
            find_kir = [x for x in kir if x in form["project_name"].value().lower()]
            if int(form["length"].value()) < 150 or find_kir:
                if int(form["length"].value()) < 150:
                    message = 'Длина профиля должна быть больше 150 мм'
                    return render(
                        request, "sharp_draft/xml_encode.html", {"profile": profile,
                                                                 "form": form,
                                                                 "message": message}
                    )
                if find_kir:
                    message = 'Имя проекта должно содержать только латинские символы и цифры'
                    return render(
                        request, "sharp_draft/xml_encode.html", {"profile": profile,
                                                                 "form": form,
                                                                 "message": message}
                    )
            else:
                obj = create_xml(
                    length=form["length"].value(),
                    profile=form["profile"].value(),
                    material=form["material"].value(),
                    project_name=form["project_name"].value(),
                    element_name=form["element_name"].value(),
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
