from django.urls import path
from . import views


app_name = "user_account"

urlpatterns = [
    # path("signup", views.SignUpView.as_view(), name="signup"),
    path("login", views.NormalLoginView.as_view(), name="login")

]

