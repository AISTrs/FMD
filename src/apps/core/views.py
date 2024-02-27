from django.shortcuts import render


# Create your views here.


def home(request):
    return render(request, "home.html")


def consulting(request):
    return render(request, "committee/consulting.html")
