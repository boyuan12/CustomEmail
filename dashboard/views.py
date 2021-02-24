from dashboard.models import Email
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from helpers import current_milli_time, send_mail
from django.contrib.auth.decorators import login_required


# Create your views here.
def register(request):
    if request.method == "POST":
        User.objects.create_user(username=request.POST["username"], password=request.POST["password"]).save()
        user = User.objects.get(username=request.POST["username"])
        login(request, user)
        return HttpResponseRedirect("/")
    else:
        return render(request, "dashboard/register.html")


def login_view(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST["password"])
        if user is not None:
            login(request, user)
            if request.GET.get("next") is not None:
                return HttpResponseRedirect(request.GET.get("next"))
            return HttpResponseRedirect("/")
        return HttpResponse("invalid credential")
    else:
        return render(request, "dashboard/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


@login_required(login_url='/login/')
def index(request):
    emails = Email.objects.filter(to_email=f"{request.user.username}@kinetic-kowalski.online")
    return render(request, "dashboard/index.html", {
        "emails": emails
    })


@login_required(login_url='/login/')
def send(request):
    if request.method == "POST":
        send_mail(f"{request.user.username}@kinetic-kowalski.online", request.POST["receiver"], request.POST["subject"], request.POST["body"])

        Email(timestamp=str(current_milli_time()), subject=request.POST["subject"], body=request.POST["body"], from_email=f"{request.user.username}@kinetic-kowalski.online", to_email=request.POST["receiver"]).save()

        return HttpResponse("Sent successfully!")

    else:
        return render(request, "dashboard/send.html")
