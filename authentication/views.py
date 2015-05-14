from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from authentication.forms import UserProfileForm
from django.contrib import auth
from exam.models import UserProfile
from django.core.urlresolvers import reverse
from django.core.mail import send_mail


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
        try:
            user_profile_in_db = UserProfile.objects.get(email=email)
            if user_profile_in_db:
                return HttpResponseRedirect(reverse("authentication_alert", args=["danger", "Пользователь с e-mail адресом "+email+" уже существует!"]))
        except:
            # Exception does not matter
            pass
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
        send_mail(
            'Регистрация на exam.ru',
            'Здравствуйте ' + first_name + '! \n \n Поздравляем Вас с успешной регистрацией на exam.ru! \n \n Ваш логин: ' + email + ' \n Ваш пароль: ' + password_1 + ' \n \n С уважением, команда exam.ru',
            'test.kutepov@yandex.ru',
            [email],
            fail_silently=False
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
    if "save" in request.POST:
        if "picture" in request.FILES:
            picture = request.FILES["picture"]
        else:
            picture = None
        user = UserProfile.objects.get(id=request.user.id)
        email = request.POST["email"]
        user.email = email
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        password = None
        if password1 and password2 and password1 != "" and password2 != "" and password1 == password2:
            password = request.POST["password1"]
            user.set_password(password)
        user.first_name = request.POST["firstName"]
        user.middle_name = request.POST["middleName"]
        user.last_name = request.POST["lastName"]
        user.date_of_birth = request.POST["dateOfBirth"]
        user.gender = request.POST["gender"]
        user.country = request.POST["country"]
        user.city = request.POST["city"]
        user.address = request.POST["address"]
        user.institution = request.POST["institution"]
        user.position = request.POST["position"]
        if picture:
            user.picture = picture
        user.save()
        if password:
            user = auth.authenticate(email=email, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
        return HttpResponseRedirect(reverse("dashboard"))
    else:
        return render(
                request,
                "authentication/settings.html",
                {}
            )


def generate_password(length=8):
    """
    Generates new password
    :param length: length of password
    :return:
    """
    if not isinstance(length, int) or length < 8:
        raise ValueError("temp password must have positive length")

    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    import random
    return ''.join(map(lambda x: random.choice(chars), range(length)))


def recovery_password(request):
    """
    Recoveries the password
    :param request:
    :return:
    """
    if "email" in request.POST:
        user = UserProfile.objects.filter(email=request.POST["email"])
        password = generate_password()
        if user and len(user) == 1:
            user[0].set_password(password)
            user[0].save()
            send_mail(
                'Пароль к аккаунту на exam.ru',
                'Здравствуйте ' + user[0].first_name + '! \n \n Ваш логин: ' + user[0].email + ' \n Ваш пароль: ' + password + ' \n \n С уважением, команда exam.ru',
                'test.kutepov@yandex.ru',
                [request.POST["email"]],
                fail_silently=False
            )
        else:
            pass
    return HttpResponseRedirect(reverse("index"))


def alert(request, status, message):
    """
    Shows page with message
    :param request:
    :param status: status (success, danger ... for bootstrap)
    :param message: message
    :return:
    """
    return render(
        request,
        "exam/alert.html",
        {
            "status": status,
            "message": message
        }
    )