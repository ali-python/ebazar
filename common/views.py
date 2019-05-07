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
from django.contrib.auth.models import User
from django.http import Http404
from merchant.models import MerchantDailyRecord


class RegisterView(FormView):
    form_class = auth_forms.UserCreationForm
    template_name = 'register.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))

        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        with transaction.atomic():
            user = form.save()

            if user.user_profile:
                user.user_profile.phone = self.request.POST.get(
                    'phone')
                user.user_profile.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            auth_user = authenticate(username=username,password=raw_password)
            auth_login(self.request, auth_user)

        return HttpResponseRedirect(reverse('home'))

    def form_invalid(self, form):
        return super(RegisterView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        if self.request.POST:
            context.update({
                'username': self.request.POST.get('username'),
                'phone': self.request.POST.get('phone'),
                'password1': self.request.POST.get('password1'),
                'password2': self.request.POST.get('password2')
            })

        return context


class LoginView (FormView):
    template_name = 'login.html'
    form_class = auth_forms.AuthenticationForm

    def dispatch(self, request, *args, **kwargs):

        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        return HttpResponseRedirect(reverse('login'))

    def form_invalid(self, form):
        return super(LoginView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        merchant_daily_records=MerchantDailyRecord.objects.all()
        context.update({
            'merchant_daily_records': merchant_daily_records
        })
        return context


class HomeView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.user_profile:
                if (
                        self.request.user.user_profile.type ==
                        self.request.user.user_profile.USER_TYPE_MERCHANT
                ):
                    return HttpResponseRedirect(reverse('merchant:dashboard'))
            # if self.request.user.user_profile:
            #     if (
            #             self.request.user.user_profile.type ==
            #             self.request.user.user_profile.USER_TYPE_CLIENT
            #     ):
            #         return HttpResponseRedirect(reverse('home'))

        return super(
            HomeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        merchant_daily_records=MerchantDailyRecord.objects.all()
        context.update({
            'merchant_daily_records': merchant_daily_records
        })

        return context
class UpdateProfile(UpdateView):
    form_class = UserProfileForm
    template_name = 'update_profile.html'
    model = UserProfile
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = User.objects.get(username=self.request.POST.get('username'))
        obj.user.save()
        obj.save()
        return HttpResponseRedirect(reverse('home'))

    def form_invalid(self, form):
        return super(UpdateProfile, self).form_invalid(form)

class UserProfileInfo(TemplateView):
    template_name = 'user_profile_info.html'

    def get_context_data(self, **kwargs):
        context = super(
            UserProfileInfo, self).get_context_data(**kwargs)

        try:
            user_profile = UserProfile.objects.get(id=self.kwargs.get('pk'))
        except UserProfile.DoesNotExist:
            return Http404('User does not exists')
        context.update({
            'user_profile': user_profile
        })

        return context
