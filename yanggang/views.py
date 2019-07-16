from django.shortcuts import render

def home(request):
    return render(request, 'yanggang/home.html')


def success(request):
    return render(request, 'yanggang/success.html')


def canceled(request):
    return render(request, 'yanggang/canceled.html')