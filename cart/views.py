from django.shortcuts import render, redirect
from django.http import JsonResponse


def update_item(request):
    return JsonResponse('Item was added', safe=False)