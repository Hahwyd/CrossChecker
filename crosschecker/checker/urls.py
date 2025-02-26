from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import HomeView, CheckWikiView, UserProfileView, signup

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("check/", CheckWikiView.as_view(), name="check_wiki"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", signup, name="signup"),
]
