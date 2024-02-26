from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.


@login_required(login_url="/login/")
def home(request):
    return render(request, "home.html")


@login_required(login_url="/login/")
def consulting(request):
    return render(request, "committee/consulting.html")
