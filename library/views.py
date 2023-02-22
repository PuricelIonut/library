from django.shortcuts import render


def not_found_view(request, exception):
    return render(request, 'templates/404.html')