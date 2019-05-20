from django.views.generic import TemplateView, RedirectView, UpdateView
from django.views.generic import FormView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.contrib.auth import forms as auth_forms
from django.db import transaction
from django.contrib.auth import authenticate
from django.db.models import Sum

from django.contrib.auth import login as auth_login
from merchant.models import MerchantDailyRecord, MerchantSalesRecords
from common.views import RegisterView, LoginView,HomeView, UpdateProfile
from merchant.views import (DashboardView,DailyRecordsView,SalesRecordsView,
                            CreateDailyRecordView,UpdateDailyRecordView)


class MobileRegisterView(RegisterView):
    template_name = 'mobile_web/register.html'


class MobileLoginView(LoginView):
    template_name = 'mobile_web/login.html'
    form_class = auth_forms.AuthenticationForm

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('mobile:home'))

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        return HttpResponseRedirect(reverse('mobile:login'))

    def form_invalid(self, form):
        return super(LoginView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        merchant_daily_records = MerchantDailyRecord.objects.all()
        context.update({
            'merchant_daily_records': merchant_daily_records
        })
        return context

class MobileLogoutView(TemplateView):
    pass


class MobileHomePageView(HomeView):
    template_name = 'mobile_web/home.html'
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.user_profile:
                if (
                        self.request.user.user_profile.type ==
                        self.request.user.user_profile.USER_TYPE_MERCHANT
                ):
                    return HttpResponseRedirect(reverse('mobile:merchant_dashboard'))
        return super(
            HomeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        merchant_daily_records=MerchantDailyRecord.objects.all()
        context.update({
            'merchant_daily_records': merchant_daily_records
        })


class MobileUserInfo(UpdateProfile):
    template_name = 'mobile_web/user.html'

#------------------ Merchant Mobile Views -------------------- #

class MobileMerchantDashboardView(DashboardView):
    template_name ='mobile_web/merchant_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('mobile:merchant_daily_record'))
        return super(
            DashboardView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        daily_records = MerchantDailyRecord.objects.filter(
            merchant=self.request.user.user_merchant.merchant
        ).latest('id')
        sales = MerchantSalesRecords.objects.filter(
            merchant_daily_record__merchant=self.request.user.user_merchant.merchant
        )
        purchased_price = sales.aggregate(Sum('purchased_price'))
        purchased_price = purchased_price.get('purchased_price__sum')
        purchased_quantity = sales.aggregate(Sum('purchased_quantity'))
        purchased_quantity = purchased_quantity.get('purchased_quantity__sum')
        remaining_quantity = float(daily_records.item_quantity) - float(purchased_quantity)
        context.update({
            'purchased_price': purchased_price,
            'purchased_quantity': purchased_quantity,
            'daily_records': daily_records,
            'remaining_quantity': remaining_quantity
        })
        return context

class MobileMerchantDailyRecordsView(DailyRecordsView):
    template_name ='mobile_web/merchant_daily_records.html'

class MobileMerchantSalesRecordsView(SalesRecordsView):
    template_name ='mobile_web/merchant_sales_record.html'

class MobileMerchantCreateDailyRecordView(CreateDailyRecordView):
    template_name ='mobile_web/merchant_create_daily_record.html'

class MobileMerchantUpdateDailyRecordView(UpdateDailyRecordView):
    template_name ='mobile_web/merchant_update_record.html'
