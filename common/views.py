from django.views.generic import TemplateView, RedirectView, UpdateView
from django.views.generic import FormView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.contrib.auth import forms as auth_forms
from django.db import transaction
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from common.form import UserProfileForm
from common.models import UserProfile

class RegisterView(FormView):
    form_class = auth_forms.UserCreationForm
    template_name = 'register.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))

        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # register new user in the system
        user = form.save()

        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        auth_user = authenticate(username=username, password=raw_password)
        auth_login(self.request, auth_user)

        return HttpResponseRedirect(reverse('home'))

    def form_invalid(self, form):
        return super(RegisterView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        if self.request.POST:
            context.update({
                'username': self.request.POST.get('username'),
                'password1': self.request.POST.get('password1'),
                'password2': self.request.POST.get('password2')
            })

        return context


# def login(request):
#     return render(request, 'login.html')

class LoginView (FormView):
    template_name = 'login.html'
    form_class = auth_forms.AuthenticationForm

    def dispatch(self, request, *args, **kwargs):

        if self.request.user.is_authenticated:
            if (
                    self.request.user.userprofile.USER_TYPES ==
                    self.request.user.userprofile.USER_TYPE_COMPANY
            ):
                return HttpResponseRedirect(
                    reverse('home'))

            return HttpResponseRedirect(reverse('home'))

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        return HttpResponseRedirect(reverse('home'))

    def form_invalid(self, form):
        return super(LoginView, self).form_invalid(form)





def home(request):
    return render(request, 'index.html')
