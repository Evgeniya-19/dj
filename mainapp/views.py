import random

from django.shortcuts import render, get_object_or_404

from mainapp.models import Product, ProductCategory
from basketapp.models import Basket

def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return[]

def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products


def get_hot_product():
    products = Product.objects.all()

    return random.sample(list(products), 1)[0]


def products(request, pk=None):
    title = 'продукты'

    links_menu = ProductCategory.objects.all()
    basket = get_basket(request.user)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)


    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        context = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'related_products': same_products,
            'products': products,
            'basket': basket,
            'hot_product': hot_product,
        }
        return render(request, 'mainapp/products.html', context)


    products = Product.objects.all().order_by('price')

    context = {
        'title': title,
        'links_menu': links_menu,
        'related_products': same_products,
        'hot_product': hot_product,
        'products': products,
        'basket': basket,
    }
    return render(request, 'mainapp/products.html', context)

def product(request, pk):
    title = 'продукты'
    links_menu = ProductCategory.objects.all()
    basket = get_basket(request.user)

    product = get_object_or_404(Product, pk=pk)

    same_products = get_same_products(product)

    context = {
        'title': title,
        'links_menu': links_menu,
        'related_products': same_products,
        'products': products,
        'basket': basket,
    }
    return render(request, 'mainapp/product.html', context)
