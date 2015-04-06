from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from exam.models import Category


def index(request):
    return render(request, "exam/index.html")


@login_required(login_url='/')
def dashboard(request):
    return render(request, "exam/dashboard.html")

@login_required(login_url='/')
def create_new_test(request):
    category_list = Category.objects.all()
    return render(request, "exam/create_new_test.html", {"category_list": category_list})