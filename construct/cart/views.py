from api.models import Measure, Product, ProductCategory, Profile, UserCart
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from modules.exceptions import *
from modules.serializers import (GetMeasure, GetProductMeasure,
                                 LoadCartSerializer, UpdateCart)

from .cart import Cart
from .forms import CartAddProductForm, CartRemoveProductForm


@require_POST
def cart_add(request, product_id):
    if request.user.is_active:
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(
                product=product, quantity=cd["quantity"], update_quantity=cd["update"]
            )
        return redirect("cart:cart_detail")
    else:
        return render(request, "dashboard/401.html")


@require_POST
def cart_reduce(request, product_id):
    if request.user.is_active:
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartRemoveProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.reduce(
                product=product, quantity=cd["quantity"], update_quantity=cd["update"]
            )
        return redirect("cart:cart_detail")
    else:
        return render(request, "dashboard/401.html")


def cart_remove(request, product_id):
    if request.user.is_active:
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect("cart:cart_detail")
    else:
        return render(request, "dashboard/401.html")


@server_error_decorator
@is_active_decorator
def cart_detail(request):
    cart = Cart(request)
    profile = Profile.objects.get(client_id=request.user)
    cart_add_product_form = CartAddProductForm()
    cart_remove_product_form = CartRemoveProductForm()
    categories = ProductCategory.objects.all()
    title = "Корзина"
    product_list = UserCart.objects.get(client_id=request.user)
    serializer = LoadCartSerializer(product_list, many=False)
    saved_cart = []
    keys = serializer.data["product_list"].keys()

    for key in keys:
        product = Product.objects.get(id=key)
        measure_serializer = GetProductMeasure(product, many=False)
        measure = Measure.objects.get(id=measure_serializer.data["measure"])
        measure = GetMeasure(measure, many=False)
        saved_cart.append(
            str(serializer.data["product_list"].get(key))
            + str(measure.data["measure"])
            + " --- "
            + str(Product.objects.get(id=key))
        )
    context = {
        "profile": profile,
        "categories": categories,
        "cart": cart,
        "cart_add_product_form": cart_add_product_form,
        "cart_remove_product_form": cart_remove_product_form,
        "title": title,
        "saved_cart": saved_cart,
    }
    return render(request, "cart/detail.html", context)


def update_cart(request):
    if request.user.is_active:
        cart = Cart(request)
        product_list = cart.get_all_products()
        user_cart = UserCart.objects.get(client_id=request.user)
        serializer = UpdateCart(user_cart, data={"product_list": product_list})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return redirect("cart:cart_detail")


def load_cart(request):
    if request.user.is_active:
        cart = Cart(request)
        cart.clear()
        cart = Cart(request)

        product_list = UserCart.objects.get(client_id=request.user)
        serializer = LoadCartSerializer(product_list, many=False)
        keys = serializer.data["product_list"].keys()
        for item in keys:
            cart.add(
                product=Product.objects.get(id=int(item)),
                quantity=int(serializer.data["product_list"].get(item)),
            )

        return redirect("cart:cart_detail")
    else:
        return render(request, "dashboard/401.html")


def clear_cart(request):
    if request.user.is_active:
        cart = Cart(request)
        cart.clear()
        return redirect("cart:cart_detail")
    else:
        return render(request, "dashboard/401.html")
