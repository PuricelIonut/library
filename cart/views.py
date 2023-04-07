from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.utils.safestring import mark_safe
import json

from shelf.models import BookModel
from cart.models import Order, OrderItem
from .helpers import cookie_guest_cart, get_total_quantity


def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        cookie_data = cookie_guest_cart(request)
        items = cookie_data['items']
        order = cookie_data['order']

    return render(request, 'cart.html', {'items':items, 'order':order, "cart_items": get_total_quantity(request),
})


def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user
    product = BookModel.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
        messages.success(request, mark_safe('Item <b>added</b> to shopping cart succesfully!'))
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        messages.success(request, mark_safe('Item <b>removed</b> from the shopping cart succesfully!'))


    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)