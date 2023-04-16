from .models import *
from django.contrib import messages
from django.utils.safestring import mark_safe

import json


def cookie_guest_cart(request):
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}

    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    for i in cart:
        product = BookModel.objects.get(id=i)
        total = (product.price * cart[i]['quantity'])

        order['get_cart_total'] += total
        order['get_cart_items'] += cart[i]['quantity']

        item = {
            'product':{
            'id':product.id,
            'title':product.title,
            'price':product.price,
            'image':product.image
            },
            'quantity':cart[i]['quantity'],
            'get_total':total
        }

        items.append(item)

    return {'order':order, 'items':items}


def get_total_quantity(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        try:
            cartItems = order['get_cart_items']
        except:
            cartItems = created['get_cart_items']
        for i in cart:
            cartItems += cart[i]['quantity']
    
    if cartItems == 0:
        return ''
    else:
        return cartItems
