from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views


app_name = "env"
urlpatterns = [
    # path("", views.envs, name="envs"),
    path("", views.EnvironmentsView.as_view(), name="envs"),
    # path("<str:ipaddress>", views.environment, name="env"),
    path("<str:ipaddress>", views.EnvironmentView.as_view(), name="env"),
]
