from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, Textarea, DateTimeField
from api.models import Review, Order, Address, OrderPayment, Product, OrderStatus
from django import forms


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
