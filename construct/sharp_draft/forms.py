from django import forms

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
