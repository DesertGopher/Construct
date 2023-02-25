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


class ProductEdit(ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'price', 'about', 'measure', 'category_class', 'vendor', 'is_stock', 'discount', 'prod_pic']

    price = forms.IntegerField(required=True)
    is_stock = forms.IntegerField(required=True)
    discount = forms.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        super(ProductEdit, self).__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['price'].required = False
        self.fields['about'].required = False
        self.fields['measure'].required = False
        self.fields['category_class'].required = False
        self.fields['vendor'].required = False
        self.fields['is_stock'].required = False
        self.fields['discount'].required = False

        self.fields['name'].label = 'Наименование'
        self.fields['price'].label = 'Цена'
        self.fields['about'].label = 'Описание'
        self.fields['measure'].label = 'Измерение'
        self.fields['category_class'].label = 'Категория'
        self.fields['vendor'].label = 'Производитель'
        self.fields['is_stock'].label = 'В наличии'
        self.fields['discount'].label = 'Скидка (%)'

        self.fields['name'].widget = forms.Textarea(attrs={'placeholder':
                                                           'Наименование товара',
                                                           'cols': 8,
                                                           'rows': 1,
                                                           'class': 'form-control',
                                                           'required': 'True'})

        self.fields['about'].widget = forms.Textarea(attrs={'placeholder': 'Описание продукта',
                                                            'cols': 8,
                                                            'rows': 5,
                                                            'class': 'form-control',
                                                            'required': 'True'})

        self.fields['vendor'].widget = forms.Textarea(attrs={'placeholder': 'Производитель',
                                                             'cols': 8,
                                                             'rows': 1,
                                                             'class': 'form-control',
                                                             'required': 'True'})


class NewsEdit(ModelForm):

    class Meta:
        model = News
        fields = ['title', 'news', 'picture']

    def __init__(self, *args, **kwargs):
        super(NewsEdit, self).__init__(*args, **kwargs)
        self.fields['title'].help_text = ''
        self.fields['title'].label = ''
        self.fields['title'].widget = forms.Textarea(attrs={'placeholder':
                                                            'Заголовок',
                                                            'cols': 8,
                                                            'rows': 1,
                                                            'class': 'form-control', })
        self.fields['news'].help_text = ''
        self.fields['news'].label = ''
        self.fields['news'].widget = forms.Textarea(attrs={'placeholder': 'Содержание',
                                                           'cols': 8,
                                                           'rows': 5,
                                                           'class': 'form-control', })
