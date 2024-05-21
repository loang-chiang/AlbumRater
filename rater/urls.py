from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("album/<str:album_id>", views.album, name="album"),
    path("save_album", views.save_album, name="save_album"),
    path("unsave_album", views.unsave_album, name="unsave_album"),
    path("library", views.library, name="library"),
    path("recent", views.recent, name="recent"),
    path("like_rating", views.like_rating, name="like_rating"),
    path("unlike_rating", views.unlike_rating, name="unlike_rating"),
    path('profile/<str:username>/', views.profile, name='profile'),
]