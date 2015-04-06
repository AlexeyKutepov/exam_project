from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from exam.models import Category, Test
from django.http import HttpResponseRedirect


def index(request):
    return render(request, "exam/index.html")


@login_required(login_url='/')
def dashboard(request):
    return render(request, "exam/dashboard.html")

@login_required(login_url='/')
def create_new_test(request):
    """
    Creates new test,
    :param request:
    :return:
    """
    if "name" and "description" and "category" in request.POST:
        category = Category.objects.get(name=request.POST["category"])
        if request.POST["isPublic"] == 'public':
            is_public = True
        else:
            is_public = False
        test = Test.objects.get_or_create(
            name=request.POST["name"],
            description=request.POST["description"],
            category=category,
            author=request.user,
            is_public=is_public,
        )
        return HttpResponseRedirect("/create_new_question/")
    else:
        category_list = Category.objects.all()
        return render(request, "exam/create_new_test.html", {"category_list": category_list})


@login_required(login_url='/')
def create_new_question(request):
    return render(request, "exam/create_new_question.html")