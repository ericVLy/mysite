from typing import Any
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView
from .forms import LoginForm
from .admin import UserCreationForm


class NormalLoginView(LoginView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.form_class = None
        self.authentication_form = LoginForm
        self.signup_form = UserCreationForm
        self.template_name = "index.html"
        self.signup_prefix = "signup_form"
        self.login_prefix = None
        self.next_page = '/'
        # self.model = NormalUser

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        signup_form = self.signup_form(prefix=self.signup_prefix)
        context[self.signup_prefix] = signup_form
        return context

    def form_valid(self, form):
        if form.prefix == self.signup_prefix:
            form.save()
            return render(self.request, 
                          "auto_refresh.html", 
                          {"title": "signup succeed", "body": "signup succeed", "url": self.request.path})
        else:
            auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.prefix = self.login_prefix
        form = self.get_form()
        self.prefix = self.signup_prefix
        signup_form = self.get_form(self.signup_form)
        if form.is_valid():
            self.prefix = self.login_prefix
            print("form valid")
            return self.form_valid(form)
        elif signup_form.is_valid():
            self.prefix = self.signup_prefix
            print("signup form valid")
            return self.form_valid(signup_form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        print("***********form invalid***********")
        return super().form_invalid(form)

    # def get_form(self, form_class):
    #     return super().get_form(form_class)

    def get_form_class(self):
        return self.authentication_form


# Create your views here.
