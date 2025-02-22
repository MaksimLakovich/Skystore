from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import CustomLoginView, CustomRegisterView, CustomEditProfileView

app_name = "users"

urlpatterns = [
    path("register/", CustomRegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("edit_profile/", CustomEditProfileView.as_view(), name="edit_profile"),
]
