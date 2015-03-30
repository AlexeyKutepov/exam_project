from django.shortcuts import render


def index(request):
    return render(request, "exam/index.html")


def dashboard(request):
    return render(request, "exam/dashboard.html")