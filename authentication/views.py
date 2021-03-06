import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from authentication.forms import UserProfileForm
from django.contrib import auth
from exam.models import UserProfile
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.conf import settings
import imghdr


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
            return HttpResponseRedirect(reverse("authentication_alert", args=["danger", "Неправильный логин или пароль"]))
    else:
        return HttpResponseRedirect(reverse("authentication_alert", args=["danger", "Неправильный логин или пароль"]))


@login_required(login_url='/')
def sign_out(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("index"))


def validate_date(date_text):
    try:
        date_text = datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return date_text
    except ValueError:
        try:
            date_text = datetime.datetime.strptime(date_text, '%d.%m.%Y')
            return date_text
        except ValueError:
            return datetime.datetime.now()


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
        date_of_birth = validate_date(date_of_birth)


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
            country = ""
        if "city" in request.POST:
            city = request.POST.get("city")
        else:
            city = ""
        if "address" in request.POST:
            address = request.POST.get("address")
        else:
            address = ""
        if "institution" in request.POST:
            institution = request.POST.get("institution")
        else:
            institution = ""
        if "position" in request.POST:
            position = request.POST.get("position")
        else:
            position = ""
        if "picture" in request.FILES:
            picture = request.FILES["picture"]
            if not imghdr.what(picture):
                picture = None
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
        try:
            send_mail(
                'Регистрация на www.exam.moscow',
                'Здравствуйте ' + first_name + '! \n \n Поздравляем Вас с успешной регистрацией на www.exam.moscow! \n \n Ваш логин: ' + email + ' \n Ваш пароль: ' + password_1 + ' \n \n С уважением, команда www.exam.moscow',
                getattr(settings, "EMAIL_HOST_USER", None),
                [email],
                fail_silently=False
            )
        except:
            pass
        user_auth = auth.authenticate(email=email, password=password_1)
        if user_auth is not None and user_auth.is_active:
            auth.login(request, user_auth)
            if "next" in request.POST:
                return HttpResponseRedirect(request.POST["next"])
            else:
                return HttpResponseRedirect(reverse("dashboard"))
        else:
            return HttpResponseRedirect(reverse("authentication_alert", args=[
                        "success", "Поздравляем! Вы успешно зарегистрировались. Для продолжения работы войдите в систему под своим логином и паролем."
                    ]))
    else:
        next_page = None
        if "next" in request.GET:
            next_page = request.GET["next"]
        return render(
            request,
            "authentication/create_profile.html",
            {
                "profile_form": UserProfileForm,
                "next": next_page
            }
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
        if picture and imghdr.what(picture):
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
            try:
                send_mail(
                    'Пароль к аккаунту на www.exam.moscow',
                    'Здравствуйте ' + user[0].first_name + '! \n \n Ваш логин: ' + user[0].email + ' \n Ваш пароль: ' + password + ' \n \n С уважением, команда www.exam.moscow',
                    getattr(settings, "EMAIL_HOST_USER", None),
                    [request.POST["email"]],
                    fail_silently=False
                )
                return HttpResponseRedirect(reverse("authentication_alert", args=[
                    "success", "Новый пароль отправлен на электронную почту."
                ]))
            except:
                return HttpResponseRedirect(reverse("authentication_alert", args=[
                    "danger", "Не удалось отправить пароль на электронную почту. Повторите попытку или сообщите нам о проблеме."
                ]))
        else:
            return HttpResponseRedirect(reverse("authentication_alert", args=[
                    "danger", "Пользователь с e-mail адресом "+request.POST["email"]+" не зарегистрирован!"
                ]))
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