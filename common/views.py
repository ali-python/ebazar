from django.views.generic import TemplateView, RedirectView, UpdateView, ListView
from django.views.generic import FormView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.contrib.auth import forms as auth_forms
from django.db import transaction
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from common.form import UserProfileForm, FeedBackForm
from common.models import UserProfile, City
from django.contrib.auth.models import User
from django.http import Http404
from django.db import transaction
from merchant.models import MerchantDailyRecord, Merchant, MerchantUser
from client.views import InvoiceHistoery
from client.models import Invoice, Order, OrderItem


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

class MerchantRegisterView(FormView):
    form_class = auth_forms.UserCreationForm
    template_name = 'merchant/merchant_register.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))

        return super(MerchantRegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        with transaction.atomic():
            user = form.save()

            if user.user_profile:
                user.user_profile.phone = self.request.POST.get('phone')
                user.user_profile.type = user.user_profile.USER_TYPE_MERCHANT
                user.user_profile.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            auth_user = authenticate(username=username,password=raw_password)
            auth_login(self.request, auth_user)

            retialer = Merchant.objects.create(name=user.username, phone=user.user_profile.phone, 
            shop_name=self.request.POST.get('shop_name'),   address=self.request.POST.get('address'))
            retialer.save()
            retailer_user = MerchantUser.objects.create(merchant=retialer, user=user)
            retailer_user.save()

        return HttpResponseRedirect(reverse('home'))

    def form_invalid(self, form):
        print(form.errors)
        print('_____________________________________________')
        return super(MerchantRegisterView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(MerchantRegisterView, self).get_context_data(**kwargs)
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


# class HomeView(TemplateView):
#     template_name = 'index.html'

#     def dispatch(self, request, *args, **kwargs):
#         if self.request.user.is_authenticated:
#             if self.request.user.user_profile:
#                 if (
#                         self.request.user.user_profile.type ==
#                         self.request.user.user_profile.USER_TYPE_MERCHANT
#                 ):
#                     return HttpResponseRedirect(reverse('merchant:dashboard'))

#         return super(
#             HomeView, self).dispatch(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super(HomeView, self).get_context_data(**kwargs)
#         merchant_daily_records=MerchantDailyRecord.objects.all()
#         merchants = Merchant.objects.all()
#         context.update({
#             'merchant_daily_records': merchant_daily_records
#         })

#         return context

class HomeView(ListView):
    model = Merchant
    template_name = 'index.html'
    paginate_by = 100
    is_paginated = True

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.user_profile:
                if (
                        self.request.user.user_profile.type ==
                        self.request.user.user_profile.USER_TYPE_MERCHANT
                ):
                    return HttpResponseRedirect(reverse('merchant:dashboard'))
                if (
                        self.request.user.user_profile.type ==
                        self.request.user.user_profile.USER_TYPE_COMPANY
                ):
                    return HttpResponseRedirect(reverse('common:admin_dashboard'))

        return super(
            HomeView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset

        if not queryset:
            queryset = Merchant.objects.all().order_by('-id')
        if self.request.GET.get('location'):
            queryset = Merchant.objects.filter(
                location__contains=self.request.GET.get('location'))
        if self.request.GET.get('shop_name'):
            queryset = Merchant.objects.filter(
                shop_name=self.request.GET.get('shop_name').lstrip('0')
            )

        return queryset.order_by('-id')

        
class UpdateProfile(UpdateView):
    form_class = UserProfileForm
    template_name = 'update_profile.html'
    model = UserProfile
    def form_valid(self, form):
        with transaction.atomic():
            obj = form.save(commit=False)
            obj.user = User.objects.get(username=self.request.POST.get('username'))
            obj.user.save()
            obj.city=City.objects.get(city_name=self.request.POST.get('city_name'))
            # obj.city.save()
            obj.save()

            return HttpResponseRedirect(reverse('common:update', kwargs={
                            'pk': obj.user.id}))

    def form_invalid(self, form):
        return super(UpdateProfile, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(
            UpdateProfile, self).get_context_data(**kwargs)

        city=City.objects.all()
        invoices = Invoice.objects.filter(order__user=self.request.user).order_by('-id')

        try:
            user_profile = UserProfile.objects.get(id=self.kwargs.get('pk'))
        except UserProfile.DoesNotExist:
            return Http404('User does not exists')
        context.update({
            'invoices': invoices,
            'user_profile': user_profile,
            'city':city
        })

        return context

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

class FeedBack(FormView):
    template_name = 'client/feedback.html'
    form_class = FeedBackForm

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))

        return super(FeedBack, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('home'))

    def form_invalid(self, form):
        return super(FeedBack, self).form_invalid(form)


class AdminDashBoard(TemplateView):
    template_name = 'admin/admin_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('client:list_records_view'))
        return super(
            AdminDashBoard, self).dispatch(request, *args,**kwargs)


class AdminInvoiceHistory(ListView):

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))

        return super(AdminInvoiceHistory, self).dispatch(request, *args, **kwargs)
    model = Invoice
    template_name = 'admin/invoices.html'
    paginate_by = 150
    is_paginated = True

    def get_queryset(self):
        queryset = self.queryset

        if not queryset:
            queryset = Invoice.objects.all().order_by('-id')
        return queryset.order_by('-id')



class AdminClientInvoice(TemplateView):
    template_name = 'admin/invoice_view.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))

        return super(AdminClientInvoice, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AdminClientInvoice, self).get_context_data(**kwargs)
        print(self.kwargs.get('pk'))
        print("________________________________________________________pk_")
        invoice= Invoice.objects.get(id=self.kwargs.get('pk'))
        order_items = invoice.order.customer_order.all()
        item = OrderItem.objects.filter(order__id=invoice.order.id)
        print(item)

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
            'order_items':order_items,
            'total_quantity': total_quantity,
            'total_price': total_price,
            'item': item
            # 'order':order

        })
        return context

