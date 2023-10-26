from django.shortcuts import render, get_object_or_404
from django.views import generic
# from django.utils.decorators import method_decorator
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from account.mixins import LoginRequiredMixin
from .models import Environment


def environment(request, ipaddress):
    target = get_object_or_404(Environment, ipaddress=request.POST['ipaddress'])
    return render(request, "env/environment.html", {"target": target})


class RequireLoginView(LoginRequiredMixin):
    login_url = "/account/login"


class EnvironmentsView(RequireLoginView, generic.ListView):
    template_name = "env/env.html"
    context_object_name = "ipaddress_list"

    def get_queryset(self) -> list:
        ip_list = []
        respons = Environment.objects.all()
        for index in respons:
            ip_list.append(index.ipaddress)
        return ip_list


# @method_decorator(login_required, name="dispatch")
class EnvironmentView(RequireLoginView, generic.FormView):
    model = Environment
    template_name = "env/environment.html"
    context_object_name = "target"

    redirect_field_name = "env"

    def get_queryset(self):
        return Environment.objects.get(ipaddress=self.request.POST["ipaddress"])

    def post(self, request, **kwargs):
        return render(request, self.template_name, {self.context_object_name: self.get_queryset()})


# Create your views here.
