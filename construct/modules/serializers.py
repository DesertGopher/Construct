from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Profile, Order, OrderStatus, UserCart, Measure, Product, ProductCategory, News


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = '__all__'


class OrderProducts(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('product_list', )


class UpdateCart(serializers.ModelSerializer):
    class Meta:
        model = UserCart
        fields = ('product_list', )


class GetMeasure(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields = ('measure', )


class GetProductMeasure(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('measure', )


class LoadCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCart
        fields = ('product_list', )


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCart
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
