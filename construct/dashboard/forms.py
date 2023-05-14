from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from api.models import Profile, Address, District, Product
from api.models import News, Support


class AuthUserForm(AuthenticationForm, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AuthUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['password'].label = ''
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': 'Имя пользователя'})
        self.fields['password'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})

    class Meta:
        model = User
        fields = ['username', 'password']


class UserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': 'Имя пользователя'})
        self.fields['password1'].label = ''
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control',
                                                                     'placeholder': 'Пароль'})
        self.fields['password2'].label = ''
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control',
                                                                     'placeholder': 'Подтвердите пароль'})


class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ['profile_status', 'profile_picture', 'bio', 'website']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['profile_status'].help_text = ''
        self.fields['profile_status'].label = ''
        self.fields['profile_status'].widget = forms.Textarea(attrs={'placeholder':
                                               'Опишите себя в двух словах',
                                               'cols': 8,
                                               'rows': 1,
                                               'class': 'form-control'})
        self.fields['bio'].help_text = ''
        self.fields['bio'].label = ''
        self.fields['bio'].widget = forms.Textarea(attrs={'placeholder': 'Расскажите о себе',
                                               'cols': 8,
                                               'rows': 5,
                                               'class': 'form-control'})
        self.fields['website'].help_text = ''
        self.fields['website'].label = ''
        self.fields['website'].widget = forms.Textarea(attrs={'placeholder':
                                               'Оставьте ссылку на Ваш контакт (социальная сеть или вебсайт)',
                                               'cols': 8,
                                               'rows': 1,
                                               'class': 'form-control'})


class AddAddress(ModelForm):

    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        empty_label=None
    )

    class Meta:
        model = Address
        fields = ['fact_address', 'district']

    def __init__(self, *args, **kwargs):
        super(AddAddress, self).__init__(*args, **kwargs)
        self.fields['fact_address'].help_text = ''
        self.fields['fact_address'].label = ''
        self.fields['fact_address'].widget = forms.Textarea(attrs={
                                               'placeholder': 'Впишите новый адрес',
                                               'cols': 8,
                                               'rows': 1,
                                               'class': 'form-control',
                                               })


class UserUpdate(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserUpdate, self).__init__(*args, **kwargs)
        self.fields['first_name'].help_text = ''
        self.fields['first_name'].label = ''
        self.fields['first_name'].widget = forms.Textarea(attrs={'placeholder':
                                                                 'Имя',
                                                                 'cols': 8,
                                                                 'rows': 1,
                                                                 'class': 'form-control'})
        self.fields['last_name'].help_text = ''
        self.fields['last_name'].label = ''
        self.fields['last_name'].widget = forms.Textarea(attrs={'placeholder':
                                                                'Фамилия',
                                                                'cols': 8,
                                                                'rows': 1,
                                                                'class': 'form-control'})
        self.fields['email'].help_text = ''
        self.fields['email'].label = ''
        self.fields['email'].widget = forms.Textarea(attrs={'placeholder':
                                                            'Адрес электронной почты',
                                                            'cols': 8,
                                                            'rows': 1,
                                                            'class': 'form-control'})


class WriteSupport(ModelForm):

    class Meta:
        model = Support
        fields = ['client_mail', 'appeal']

    def __init__(self, *args, **kwargs):
        super(WriteSupport, self).__init__(*args, **kwargs)
        self.fields['client_mail'].help_text = ''
        self.fields['client_mail'].label = ''
        self.fields['client_mail'].widget = forms.Textarea(attrs={
                                               'placeholder': 'Ваш e-mail',
                                               'cols': 8,
                                               'rows': 1,
                                               'class': 'form-control',
                                               })

        self.fields['appeal'].help_text = ''
        self.fields['appeal'].label = ''
        self.fields['appeal'].widget = forms.Textarea(attrs={
                                               'placeholder': 'Опишите вашу проблему или предложение.',
                                               'cols': 12,
                                               'rows': 6,
                                               'class': 'form-control',
                                               })
