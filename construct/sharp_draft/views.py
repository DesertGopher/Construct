from django.http.response import FileResponse
from django.shortcuts import render, redirect

from api.models import Profile, Templates
from api.views import UserProfile
from modules.exceptions import *

from .encrypt import create_xml
from .forms import EncodeForm, CreateTemplate, PlatePDF, SettingPlateForm
from .forms import Angle, TrianglePlate, TrapezoidPlate, SquarePlate
from .plate_scheme import generate_pdf


@server_error_decorator
@is_active_decorator
def index(request):
    """Возвращение главной страницы модуля Sharp Draft"""
    profile = UserProfile().get(request=request, client=request.user)
    return render(request, "sharp_draft/home_page.html", {"profile": profile})


@server_error_decorator
@is_active_decorator
def xml_encode(request):
    """Метод создание XML-файла"""
    profile = UserProfile().get(request=request, client=request.user)
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
def create_template(request):
    """Метод создания пользовательского штампа"""
    profile = UserProfile().get(request=request, client=request.user)
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
def edit_template(request, temp_id: int):
    """Метод редактирования пользовательского штампа"""
    profile = UserProfile().get(request=request, client=request.user)
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
def delete_template(request, temp_id):
    """Метод удаления пользовательского штампа"""
    try:
        Templates.objects.get(pk=temp_id, client_id=request.user).delete()
    except Templates.DoesNotExist:
        message = 'Такого штампа нет.'
        return render(request, 'dashboard/404.html', {'message': message})
    return redirect('sharp_draft:templates')


@server_error_decorator
@is_active_decorator
def templates(request):
    """Страница со списком пользовательских штампов"""
    tid = str(request.GET.get('tid'))
    profile = UserProfile().get(request=request, client=request.user)
    temp_list = Templates.objects.filter(client_id=request.user)
    context = {
        "profile": profile,
        "temp_list": temp_list
    }
    if tid and tid.isnumeric():
        template = Templates.objects.get(id=int(tid))
        context["template"] = template

    return render(request, "sharp_draft/templates.html", context)


@server_error_decorator
@is_active_decorator
def create_plate(request):
    """Метод создания чертежа типовой ЛСТК пластины"""
    profile = UserProfile().get(request=request, client=request.user)
    # profile = Profile.objects.get(client_id=request.user)
    plate = str(request.GET.get('plate'))
    user_template = str(request.GET.get('user_template'))
    setform = SettingPlateForm()
    temp_form = PlatePDF()
    plate_form = SquarePlate()

    context = {
        "profile": profile,
        "setform": setform,
        "temp_form": temp_form,
    }

    if plate == "square":
        plate_form = SquarePlate()
    elif plate == "triangle":
        plate_form = TrianglePlate()
    elif plate == "slicedtriangle":
        plate_form = TrapezoidPlate()
    elif plate == "rect":
        plate_form = TrianglePlate()
    elif plate == "angle":
        plate_form = Angle()
    context["plate_form"] = plate_form
    context["plate"] = plate

    if user_template != "None":
        template = Templates.objects.get(id=user_template)
        context["template"] = template

    if request.method == "POST":
        temp_form = PlatePDF(request.POST)
        data = request.POST
        if temp_form.is_valid():
            obj = generate_pdf(
                template=context["template"],
                plate=plate,
                temp_form=temp_form,
                data=data
            )
            return FileResponse(
                open(obj["path"], "rb"), as_attachment=True, filename=obj["name"]
            )
        else:
            context["message"] = 'ОШИБКА'

    return render(request, "sharp_draft/create_plate.html", context)
