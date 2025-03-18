from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("check/", CheckWikiView.as_view(), name="check_wiki"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("login/",UserLoginView.as_view(),name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("error_page/", ErrorPage.as_view(),name="error_page"),
    path("results/<int:query_id>/", QueryResultsView.as_view(), name="query_results"),
    path("delete_query/<int:query_id>/", DeleteQueryView.as_view(), name="delete_query"),
    path('delete_all_queiries/', DeleteAllQueriesView.as_view(), name='delete_all_queries'),
]
