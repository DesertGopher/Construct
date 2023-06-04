from django import forms
from django.forms import ModelForm
from api.models import Templates

_PROFILE_CHOICES = (
    ("SA-152-15-U-OUT", "SA-152-15-U-OUT"),
    ("SA-102-15-U-OUT", "SA-102-15-U-OUT"),
    ("SA-203-15-U-OUT", "SA-203-15-U-OUT"),
    ("SA-254-15-U-OUT", "SA-254-15-U-OUT"),
    ("SA-305-15-U-OUT", "SA-305-15-U-OUT"),

    ("SA-152-15-C-IN", "SA-152-15-C-IN"),
    ("SA-102-15-C-IN", "SA-102-15-C-IN"),
    ("SA-203-15-C-IN", "SA-203-15-C-IN"),
    ("SA-254-15-C-IN", "SA-254-15-C-IN"),
    ("SA-305-15-C-IN", "SA-305-15-C-IN"),
)

_STEEL_CHOICES = (
    ("C375", "C375"),
    ("C240", "C240"),
)


_PLATES_CHOICES = (
    ("square", "Квадрат"),
    ("triangle", "Треугольник"),
    ("slicedtriangle", "Треугольник с вырезом"),
    ("rect", "Прямоугольник"),
    ("angle", "Уголок"),
)


class EncodeForm(forms.Form):
    length = forms.CharField()
    project_name = forms.CharField()
    element_name = forms.CharField()
    profile = forms.ChoiceField(choices=_PROFILE_CHOICES)
    material = forms.ChoiceField(choices=_STEEL_CHOICES)

    def __init__(self, *args, **kwargs):
        super(EncodeForm, self).__init__(*args, **kwargs)
        self.fields['length'].label = ''
        self.fields['length'].widget = forms.TextInput(attrs={'placeholder': 'Длина профиля'})
        self.fields['project_name'].label = ''
        self.fields['project_name'].widget = forms.TextInput(attrs={'placeholder': 'Проект'})
        self.fields['element_name'].label = ''
        self.fields['element_name'].widget = forms.TextInput(attrs={'placeholder': 'Имя элемента'})


class CreateTemplate(ModelForm):
    class Meta:
        model = Templates
        fields = ['name', 'author', 'checker', 'company', 'code', 'object', 'project']

    def __init__(self, *args, **kwargs):
        super(CreateTemplate, self).__init__(*args, **kwargs)
        self.fields['name'].help_text = ''
        self.fields['name'].label = ''
        self.fields['name'].widget = forms.Textarea(attrs={'placeholder': 'Название штампа',
                                                           'cols': 8,
                                                           'rows': 1,
                                                           'class': 'form-control',
                                                           'resize': None})
        self.fields['author'].help_text = ''
        self.fields['author'].label = ''
        self.fields['author'].widget = forms.Textarea(attrs={'placeholder': 'Исполнитель',
                                                             'cols': 8,
                                                             'rows': 1,
                                                             'class': 'form-control', })
        self.fields['checker'].help_text = ''
        self.fields['checker'].label = ''
        self.fields['checker'].widget = forms.Textarea(attrs={'placeholder': 'Проверил',
                                                              'cols': 8,
                                                              'rows': 1,
                                                              'class': 'form-control', })
        self.fields['company'].help_text = ''
        self.fields['company'].label = ''
        self.fields['company'].widget = forms.Textarea(attrs={'placeholder': 'Организация',
                                                              'cols': 8,
                                                              'rows': 5,
                                                              'class': 'form-control', })
        self.fields['code'].help_text = ''
        self.fields['code'].label = ''
        self.fields['code'].widget = forms.Textarea(attrs={'placeholder': 'Код проекта',
                                                           'cols': 8,
                                                           'rows': 1,
                                                           'class': 'form-control', })
        self.fields['object'].help_text = ''
        self.fields['object'].label = ''
        self.fields['object'].widget = forms.Textarea(attrs={'placeholder': 'Объект',
                                                             'cols': 8,
                                                             'rows': 5,
                                                             'class': 'form-control', })
        self.fields['project'].help_text = ''
        self.fields['project'].label = ''
        self.fields['project'].widget = forms.Textarea(attrs={'placeholder': 'Проект',
                                                              'cols': 8,
                                                              'rows': 2,
                                                              'class': 'form-control', })


class PlatePDF(forms.Form):
    page = forms.IntegerField()
    pages = forms.IntegerField()
    schema = forms.CharField()
    position = forms.CharField()
    name = forms.CharField()
    amount = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(PlatePDF, self).__init__(*args, **kwargs)
        self.fields['page'].label = ''
        self.fields['page'].widget = forms.TextInput(attrs={'placeholder': 'Лист'})
        self.fields['pages'].label = ''
        self.fields['pages'].widget = forms.TextInput(attrs={'placeholder': 'Листов'})
        self.fields['schema'].label = ''
        self.fields['schema'].widget = forms.TextInput(attrs={'placeholder': 'Имя элемента'})
        self.fields['position'].label = ''
        self.fields['position'].widget = forms.TextInput(attrs={'placeholder': 'Позиция детали'})
        self.fields['name'].label = ''
        self.fields['name'].widget = forms.TextInput(attrs={'placeholder': 'Обозначение'})
        self.fields['amount'].label = ''
        self.fields['amount'].widget = forms.TextInput(attrs={'placeholder': 'Количество'})


class SettingPlateForm(forms.Form):
    plate = forms.ChoiceField(
        choices=_PLATES_CHOICES,
        label='Выберите форму пластины'
    )

    user_template = forms.ModelChoiceField(
        queryset=Templates.objects.all(),
        label='Выберите штамп для чертежа',
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['user_template'].queryset = Templates.objects.filter(
                client_id=user
            )

    class Meta:
        fields = ['payment_type', 'address_id']


class SquarePlate(forms.Form):
    side = forms.IntegerField()
    width = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(SquarePlate, self).__init__(*args, **kwargs)
        self.fields['side'].label = ''
        self.fields['side'].widget = forms.TextInput(attrs={'placeholder': 'Длина стороны A, мм'})
        self.fields['width'].label = ''
        self.fields['width'].widget = forms.TextInput(attrs={'placeholder': 'Толщина металла, мм'})


class TrapezoidPlate(forms.Form):
    side1 = forms.IntegerField()
    side2 = forms.IntegerField()
    slice = forms.IntegerField()
    width = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(TrapezoidPlate, self).__init__(*args, **kwargs)
        self.fields['side1'].label = ''
        self.fields['side1'].widget = forms.TextInput(attrs={'placeholder': 'Длина стороны A, мм'})
        self.fields['side2'].label = ''
        self.fields['side2'].widget = forms.TextInput(attrs={'placeholder': 'Длина стороны B, мм'})
        self.fields['slice'].label = ''
        self.fields['slice'].widget = forms.TextInput(attrs={'placeholder': 'Длина среза C, мм'})
        self.fields['width'].label = ''
        self.fields['width'].widget = forms.TextInput(attrs={'placeholder': 'Толщина металла, мм'})


class TrianglePlate(forms.Form):
    """Fits for rectangle shaped plates too"""
    side1 = forms.IntegerField()
    side2 = forms.IntegerField()
    width = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(TrianglePlate, self).__init__(*args, **kwargs)
        self.fields['side1'].label = ''
        self.fields['side1'].widget = forms.TextInput(attrs={'placeholder': 'Длина стороны A, мм'})
        self.fields['side2'].label = ''
        self.fields['side2'].widget = forms.TextInput(attrs={'placeholder': 'Длина стороны B, мм'})
        self.fields['width'].label = ''
        self.fields['width'].widget = forms.TextInput(attrs={'placeholder': 'Толщина металла, мм'})


class Angle(forms.Form):
    """Fits for rectangle shaped plates too"""
    side1 = forms.IntegerField()
    side2 = forms.IntegerField()
    side3 = forms.IntegerField()
    width = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(Angle, self).__init__(*args, **kwargs)
        self.fields['side1'].label = ''
        self.fields['side1'].widget = forms.TextInput(attrs={'placeholder': 'Длина стороны A, мм'})
        self.fields['side2'].label = ''
        self.fields['side2'].widget = forms.TextInput(attrs={'placeholder': 'Длина стороны B, мм'})
        self.fields['side3'].label = ''
        self.fields['side3'].widget = forms.TextInput(attrs={'placeholder': 'Длина стороны C, мм'})
        self.fields['width'].label = ''
        self.fields['width'].widget = forms.TextInput(attrs={'placeholder': 'Толщина металла, мм'})
