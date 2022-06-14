import json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from functools import reduce
from operator import and_, or_

from .models import User, Post, Follow


class PostForm(forms.Form):
    text = forms.CharField(max_length=288, label="",
    widget=forms.Textarea(
        attrs={'class':'form-control w-100', 'cols': '150', 'rows': '5'}))


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
    
    # test = Post.objects.get(text = "litty post")
    # if request.user in test.like.all():
    #     print("yes")
    # print(test)
    return render(request, "network/index.html", {
        "form": PostForm,
        "posts": posts,
    })


def userpage(request, userpage):
    user = User.objects.get(username = userpage)
    follows = Follow.objects.get(account = user)
    posts = user.Posts.all()

    posts = posts.order_by('-timestamp')

    p = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = p.get_page(page)

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


@csrf_exempt
@login_required
def get_post(request, post_id):

    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)

    if request.method == "GET":
        return JsonResponse(post.serialize())
    
    # Update likes
    elif request.method =="PUT":
        # data = json.loads(request.body)
        # if data.get("like") is not None:
        #     user = User.objects.get(pk=data["like"])
        if request.user in post.like.all():
            post.like.remove(request.user)
        else:
            post.like.add(request.user)
    return HttpResponse(status=204)




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
