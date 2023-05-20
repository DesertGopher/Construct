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
        fields = ['name', 'author', 'checker', 'company', 'code', 'schema', 'stage', 'page', 'object', 'project']

    def __init__(self, *args, **kwargs):
        super(CreateTemplate, self).__init__(*args, **kwargs)
        self.fields['name'].help_text = ''
        self.fields['name'].label = ''
        self.fields['name'].widget = forms.Textarea(attrs={'placeholder': 'Название штампа',
                                                           'cols': 8,
                                                           'rows': 1,
                                                           'class': 'form-control', })
        self.fields['author'].help_text = ''
        self.fields['author'].label = ''
        self.fields['author'].widget = forms.Textarea(attrs={'placeholder': 'Исполнитель',
                                                             'cols': 8,
                                                             'rows': 5,
                                                             'class': 'form-control', })
        self.fields['checker'].help_text = ''
        self.fields['checker'].label = ''
        self.fields['checker'].widget = forms.Textarea(attrs={'placeholder': 'Проверил',
                                                              'cols': 8,
                                                              'rows': 5,
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
                                                           'rows': 5,
                                                           'class': 'form-control', })
        self.fields['schema'].help_text = ''
        self.fields['schema'].label = ''
        self.fields['schema'].widget = forms.Textarea(attrs={'placeholder': 'Имя сборки',
                                                             'cols': 8,
                                                             'rows': 5,
                                                             'class': 'form-control', })
        self.fields['stage'].help_text = ''
        self.fields['stage'].label = ''
        self.fields['stage'].widget = forms.Textarea(attrs={'placeholder': 'Стадия',
                                                            'cols': 8,
                                                            'rows': 5,
                                                            'class': 'form-control', })
        self.fields['page'].help_text = ''
        self.fields['page'].label = ''
        self.fields['page'].widget = forms.Textarea(attrs={'placeholder': 'Лист',
                                                           'cols': 8,
                                                           'rows': 5,
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
                                                              'rows': 5,
                                                              'class': 'form-control', })
