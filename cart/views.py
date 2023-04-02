from django.shortcuts import render, redirect
from django.http import JsonResponse
import json

from shelf.models import BookModel

def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = BookModel.objects.get(id=productId)
    
    return JsonResponse('Item was added', safe=False)