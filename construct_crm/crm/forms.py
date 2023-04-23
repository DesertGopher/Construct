from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *


class AuthUserForm(AuthenticationForm, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AuthUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['password'].label = ''
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'})
        self.fields['password'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})

    class Meta:
        model = User
        fields = ['username', 'password']


class UserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        # self.fields['username'].help_text = ''
        self.fields['username'].label = ''
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': 'Имя пользователя'})
        # self.fields['password1'].help_text = ''
        self.fields['password1'].label = ''
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control',
                                                                     'placeholder': 'Пароль'})
        # self.fields['password2'].help_text = ''
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
                                               'class': 'form-control',
                                               })
        self.fields['bio'].help_text = ''
        self.fields['bio'].label = ''
        self.fields['bio'].widget = forms.Textarea(attrs={'placeholder': 'Расскажите о себе',
                                               'cols': 8,
                                               'rows': 5,
                                               'class': 'form-control',
                                               })
        self.fields['website'].help_text = ''
        self.fields['website'].label = ''
        self.fields['website'].widget = forms.Textarea(attrs={'placeholder':
                                               'Оставьте ссылку на Ваш контакт (социальная сеть или вебсайт)',
                                               'cols': 8,
                                               'rows': 1,
                                               'class': 'form-control',
                                               })


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
                                                                 'class': 'form-control',
                                                                 })

        self.fields['last_name'].help_text = ''
        self.fields['last_name'].label = ''
        self.fields['last_name'].widget = forms.Textarea(attrs={'placeholder':
                                                                'Фамилия',
                                                                'cols': 8,
                                                                'rows': 1,
                                                                'class': 'form-control',
                                                                })

        self.fields['email'].help_text = ''
        self.fields['email'].label = ''
        self.fields['email'].widget = forms.Textarea(attrs={'placeholder':
                                                            'Адрес электронной почты',
                                                            'cols': 8,
                                                            'rows': 1,
                                                            'class': 'form-control',
                                                            })


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['text', ]

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['text'].help_text = ''
        self.fields['text'].label = ''
        self.fields['text'].widget = forms.Textarea(attrs={'placeholder': 'Опишите ваши впечатления о товаре',
                                                           'cols': 8,
                                                           'rows': 3,
                                                           'class': 'form-control',
                                                           })


class OrderCreate(ModelForm):

    payment_type = forms.ModelChoiceField(
        queryset=OrderPayment.objects.all(),
        # empty_label='Тип оплаты',
        label='Выберите тип оплаты',
    )

    address_id = forms.ModelChoiceField(
        queryset=Address.objects.filter(is_active=True),
        # empty_label='Адрес доставки',
        label='Выберите адрес доставки',
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['address_id'].queryset = Address.objects.filter(
                is_active=True, client_id=user
            )

    class Meta:
        model = Order
        fields = ['payment_type', 'address_id']


class OrderEdit(ModelForm):
    payment_type = forms.ModelChoiceField(
        queryset=OrderPayment.objects.all(),
        label='Выберите тип оплаты',
    )

    status = forms.ModelChoiceField(
        queryset=OrderStatus.objects.all(),
        label='Статус заказа',
    )

    class Meta:
        model = Order
        fields = ['payment_type', 'status']


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
