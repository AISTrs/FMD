from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            user = authenticate(request, username=username,
                                password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("/")
        else:
            messages.error(request, "Invalid login username/passowrd")
            return render(request, "login.html", {"color": "red"})

    return render(request, "login.html")


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists! Please try another username")
            return render(request, "signup.html")

        if password1 != password2:
            messages.error(request, "Passwords did not match!")
            return render(request, "signup.html")

        if User.objects.filter(email=email) and email != "":
            messages.error(request, "Email already registered!")
            return render(request, "login.html", {"color": "green"})

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.first_name = firstname
        user.last_name = lastname
        user.save()

        messages.success(request, "Account created successfully! Please login using your credentials")
        return render(request, "login.html", {"color": "green"})

    return render(request, "signup.html")
