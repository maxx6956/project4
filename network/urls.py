
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<str:userpage>", views.userpage, name="userpage"),
    path("following", views.following, name="following"),

    # API
    path("get_post/<int:post_id>", views.get_post, name="get_post"),
    path("like_post/<int:post_id>", views.like_post, name="like_post"),

]
