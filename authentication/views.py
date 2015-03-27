from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def sign_in(request):
    if "email" in request.POST and "password" in request.POST:
        username = request.POST.get("email")
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect("/")
            # return render("main/login.html",
            #                           {"access_denied": "Access denied", "access_denied_class":"access_denied_text"},
            #                           context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/")
        # return render("main/login.html", context_instance=RequestContext(request))

@login_required
def sign_out(request):
    auth.logout(request)
    return HttpResponseRedirect("/")