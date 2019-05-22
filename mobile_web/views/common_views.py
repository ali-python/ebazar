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
from merchant.forms import MerchantDailyRecordForm
from client.forms import OrderItemForm
from client.models import Order, Invoice
from common.views import RegisterView, LoginView,HomeView, UpdateProfile
from merchant.views import (DashboardView,DailyRecordsView,SalesRecordsView,
                            CreateDailyRecordView,UpdateDailyRecordView)
from client.views import (MerchantDailyRecordDetailView,OrderItemView ,ClientInvoice ,InvoiceHistoery)
from common.models import City

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
            MobileHomePageView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MobileHomePageView, self).get_context_data(**kwargs)
        merchant_daily_records=MerchantDailyRecord.objects.all()
        context.update({
            'merchant_daily_records': merchant_daily_records
        })
        return context


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
    model = MerchantDailyRecord
    form_class = MerchantDailyRecordForm
    template_name ='mobile_web/merchant_create_daily_record.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return HttpResponseRedirect(reverse('mobile:merchant_daily_record'))

    def form_invalid(self, form):
        return super(MobileMerchantCreateDailyRecordView, self).form_invalid(form)


class MobileMerchantUpdateDailyRecordView(UpdateDailyRecordView):
    form_class = MerchantDailyRecordForm
    template_name ='mobile_web/merchant_update_record.html'
    model = MerchantDailyRecord
    success_url = reverse_lazy('mobile:merchant_daily_record')

#-------------------client mobile views -----------------------------#

class MobileMerchantDailyRecordDetailView(TemplateView):
    template_name = 'moblie_web/merchant_record_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('mobile:login'))
        return super(
            MobileMerchantDailyRecordDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MobileMerchantDailyRecordDetailView, self).get_context_data(**kwargs)
        merchant = MerchantDailyRecord.objects.get(id=self.kwargs.get('pk'))
        city = City.objects.all()

        context.update({
            'merchant': merchant,
            'city': city
        })
        return context

class MobilerOrderItemView(FormView):
    form_class = OrderItemForm
    template_name = 'mobile_web/client_order.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('client:list_records_view'))
        return super(
            MobilerOrderItemView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        with transaction.atomic():
            obj = form.save(commit=False)

            obj.order = Order.objects.create(
                customer_name=self.request.POST.get('customer_name'),
                customer_phone=self.request.POST.get('customer_phone'),
                alternate_phone=self.request.POST.get('alternate_phone'),
                user=self.request.user,
            )

            obj.city = City.objects.get(city_name=self.request.POST.get('city'))
            obj.city.save()
            invoice = Invoice.objects.create(
                order=obj.order,
                amount=obj.item_price
            )
            invoice.save()
            merchant_sales_record = MerchantSalesRecords.objects.create(
                merchant_daily_record=obj.merchant_daily_upload,
                purchased_quantity=obj.item_quantity,
                purchased_price=obj.item_price
            )
            merchant_sales_record.save()
            self.request.user.user_profile.phone = self.request.POST.get('customer_phone')
            self.request.user.user_profile.alternate_phone = self.request.POST.get('alternate_phone')
            self.request.user.user_profile.address = self.request.POST.get('address')
            self.request.user.user_profile.save()
            obj.save()
            return HttpResponseRedirect(reverse('mobile:client_order_invoice', kwargs={
                'pk': invoice.id
            }))

    def form_invalid(self, form):
        return super(MobilerOrderItemView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(MobilerOrderItemView, self).get_context_data(**kwargs)
        merchant_record = MerchantDailyRecord.objects.get(id=self.kwargs.get('pk'))
        context.update({
            'merchant_record': merchant_record
        })
        return context

class MobileClientInvoice(TemplateView):
    template_name = 'mobile_web/client_invoice.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('mobile:home'))
        return super(
            MobileClientInvoice, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MobileClientInvoice, self).get_context_data(**kwargs)
        invoice = Invoice.objects.get(id=self.kwargs.get('pk'))
        order_items = invoice.order.customer_order.all()

        from django.db.models import Sum
        try:
            total_quantity = order_items.aggregate(Sum('item_quantity'))
            total_quantity = total_quantity.get('item_quantity__sum') or 0

            total_price = order_items.aggregate(Sum('item_price'))
            total_price = total_price.get('item_price__sum') or 0
        except:
            total_quantity = 0
            total_price = 0

        context.update({
            'invoice': invoice,
            'order_items': order_items,
            'total_quantity': total_quantity,
            'total_price': total_price
            # 'order':order

        })
        return context

class MobileInvoiceHistoery(InvoiceHistoery):
    template_name = 'mobile_web/client_invoice_list.html'