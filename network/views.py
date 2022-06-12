from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from functools import reduce
from operator import and_, or_

from .models import User, Post, Follow


class PostForm(forms.Form):
    text = forms.CharField(max_length=288, label="",
    widget=forms.Textarea(attrs={'class':'form-control w-100', 'cols': '150', 'rows': '5'}))


def index(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            user = request.user
            print(user)
            form = form.cleaned_data
            post = Post(poster = user, text = form["text"])
            post.save()
    posts = Post.objects.all()
    posts = posts.order_by('-timestamp')

    p = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = p.get_page(page)

    return render(request, "network/index.html", {
        "form": PostForm,
        "posts": posts
    })


def userpage(request, userpage):
    user = User.objects.get(username = userpage)
    follows = Follow.objects.get(account = user)
    posts = user.Posts.all()

    posts = posts.order_by('-timestamp')

    p = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = p.get_page(page)

    print(user.Follows.all())
    if request.method == "POST":
        print(request.POST)
        if request.POST["button"] == "Follow":
           follows.follow.add(request.user)
        elif request.POST["button"] == "Unfollow":
            follows.follow.remove(request.user)
    if request.user in follows.follow.all():
        button = "Unfollow"
    else:
        button = "Follow"
    return render(request, "network/userpage.html", {
        "follows": follows,
        "posts": posts,
        "current": user,
        "button": button,
    })


@login_required
def following(request):
    follows = request.user.Follows.all()
    posts = Post.objects.filter(reduce(or_, [Q(poster=follow.account) for follow in follows]))
    posts = posts.order_by('-timestamp')

    p = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = p.get_page(page)

    return render(request, "network/following.html", {
        "posts": posts,
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            follow = Follow(account=user)
            follow.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
