from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

def index(request):
    return render(request, "belt_app/index.html")

def register(request):
    results = User.objects.register(request.POST)

    if results[0]:
        request.session["user_id"] = results[1].id
        request.session["name"] = results[1].name
        request.session["alias"] = results[1].alias
        return redirect("/dashboard")
    else:
        for error in results[1]:
            messages.add_message(request, messages.ERROR, error)
    return redirect("/")

def login(request):

    results = User.objects.login(request.POST)

    if results[0]:
        request.session["user_id"] = results[1].id
        request.session["name"] = results[1].name
        request.session["alias"] = results[1].alias
        return redirect("/dashboard")
    else:
        for error in results[1]:
            messages.add_message(request, messages.ERROR, error)
    return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/")

def dashboard(request):
    if "user_id" not in request.session:
        return(redirect("/"))

    addable = User.objects.exclude(id=request.session["user_id"])
    friended = User.objects.get(id=request.session["user_id"]).friends.all()

    for f in friended:
        addable = addable.exclude(id=f.id)

    allusers = {
        "listallusers": addable,
        "friended": friended
    }
    print(allusers)
    return render(request, "belt_app/dashboard.html", allusers)

def friend(request, user_id):
    this_user = User.objects.get(id=request.session["user_id"])
    this_friend = User.objects.get(id=user_id)
    this_user.friends.add(this_friend)
    return redirect("/dashboard")

def unfriend(request, user_id):
    this_user = User.objects.get(id=request.session["user_id"])
    this_friend = User.objects.get(id=user_id)
    this_user.friends.remove(this_friend)
    return redirect("/dashboard")

def user(request, user_id):
    userpageinfo = {
        "userinfo": User.objects.get(id=user_id)
    }
    return render(request, "belt_app/user.html", userpageinfo)
