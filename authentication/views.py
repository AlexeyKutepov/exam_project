from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def sign_in(request):
    if "email" in request.POST and "password" in request.POST:
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = auth.authenticate(email=email, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/dashboard/")
        else:
            return render(request, "exam/index.html", {"login_error": "has-error"})
    else:
        return render(request, "exam/index.html", {"login_error": "has-error"})


@login_required(login_url='/')
def sign_out(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


def create_profile(request):
    return render(request, "authentication/create_profile.html")