from django.http.response import FileResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from api.models import Profile, Templates
from modules.exceptions import *

from .encrypt import create_xml
from .forms import EncodeForm, CreateTemplate


@server_error_decorator
@is_active_decorator
def index(request):
    profile = Profile.objects.get(client_id=request.user)
    return render(request, "sharp_draft/home_page.html", {"profile": profile})


@server_error_decorator
@is_active_decorator
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


@server_error_decorator
@is_active_decorator
def create_plate(request):
    profile = Profile.objects.get(client_id=request.user)
    return render(request, "sharp_draft/create_plate.html", {"profile": profile})


@server_error_decorator
@is_active_decorator
def create_template(request):
    profile = Profile.objects.get(client_id=request.user)
    form = CreateTemplate(request.POST)
    if request.method == "POST":
        if form.is_valid():
            temp_f = form.save(commit=False)
            temp_f.client_id = request.user
            temp_f.save()
            return redirect('sharp_draft:templates')
        else:
            form = CreateTemplate()

    return render(request, "sharp_draft/create_template.html", {'form': form, "profile": profile})


@server_error_decorator
@is_active_decorator
def edit_template(request, temp_id):
    profile = Profile.objects.get(client_id=request.user)
    try:
        temp_item = Templates.objects.get(pk=temp_id, client_id=request.user)
    except Templates.DoesNotExist:
        message = 'Такого штампа нет.'
        return render(request, 'dashboard/404.html', {'message': message})

    if request.method == "POST":
        form = CreateTemplate(request.POST, instance=temp_item)
        if form.is_valid():
            temp_f = form.save(commit=False)
            temp_f.client_id = request.user
            temp_f.save()
            return redirect('sharp_draft:templates')
    else:
        form = CreateTemplate(instance=temp_item)

    return render(request, "sharp_draft/edit_template.html", {"form": form,
                                                              "profile": profile,
                                                              "temp_item": temp_item
                                                              })


@server_error_decorator
@is_active_decorator
def templates(request):
    tid = str(request.GET.get('tid'))
    profile = Profile.objects.get(client_id=request.user)
    context = {
        "profile": profile,
    }
    if tid and tid.isnumeric():
        template = Templates.objects.get(id=int(tid))
        context["template"] = template

    temp_list = Templates.objects.filter(client_id=request.user)
    context["temp_list"] = temp_list
    return render(request, "sharp_draft/templates.html", context)
