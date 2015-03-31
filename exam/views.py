from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "exam/index.html")


@login_required(login_url='/')
def dashboard(request):
    return render(request, "exam/dashboard.html")