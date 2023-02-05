from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from api.models import Profile, Address, District, Product
from api.models import News


class SearchForm(forms.Form):

    query = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['query'].label = ''
        self.fields['query'].widget = forms.TextInput(attrs={'placeholder': 'Поиск по базе...'})
