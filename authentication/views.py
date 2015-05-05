from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from authentication.forms import UserProfileForm
from django.contrib import auth
from exam.models import UserProfile
from django.core.urlresolvers import reverse


@csrf_protect
def sign_in(request):
    if "email" in request.POST and "password" in request.POST:
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = auth.authenticate(email=email, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse("dashboard"))
        else:
            return render(request, "exam/index.html", {"login_error": "has-error"})
    else:
        return render(request, "exam/index.html", {"login_error": "has-error"})


@login_required(login_url='/')
def sign_out(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("index"))


def create_profile(request):
    """
    Creates new user profile
    :param request:
    :return:
    """
    if "email" and "password1" and "password2" and "dateOfBirth" in request.POST:
        email = request.POST.get("email")
        password_1 = request.POST.get("password1")
        password_2 = request.POST.get("password2")
        date_of_birth = request.POST.get("dateOfBirth")

        if "lastName" in request.POST:
            last_name = request.POST.get("lastName")
        else:
            last_name = None
        if "firstName" in request.POST:
            first_name = request.POST.get("firstName")
        else:
            first_name = None
        if "middleName" in request.POST:
            middle_name = request.POST.get("middleName")
        else:
            middle_name = None
        if "gender" in request.POST:
            gender = request.POST.get("gender")
        else:
            gender = UserProfile.MALE
        if "country" in request.POST:
            country = request.POST.get("country")
        else:
            country = None
        if "city" in request.POST:
            city = request.POST.get("city")
        else:
            city = None
        if "address" in request.POST:
            address = request.POST.get("address")
        else:
            address = None
        if "institution" in request.POST:
            institution = request.POST.get("institution")
        else:
            institution = None
        if "position" in request.POST:
            position = request.POST.get("position")
        else:
            position = None
        if "picture" in request.FILES:
            picture = request.FILES["picture"]
        else:
            picture = None
        user = auth.get_user_model().objects.create_user(
            email=email,
            password=password_1,
            date_of_birth=date_of_birth,
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            gender=gender,
            country=country,
            city=city,
            address=address,
            institution=institution,
            position=position,
            picture=picture
        )
        return render(
            request,
            "exam/index.html",
        )
    else:
        return render(
            request,
            "authentication/create_profile.html",
            {"profile_form": UserProfileForm}
        )


@login_required(login_url='/')
def settings(request):
    return render(
            request,
            "authentication/settings.html",
            {}
        )