from django.shortcuts import render
from django.views.generic import ListView, CreateView, TemplateView,UpdateView, FormView
from django.urls import reverse_lazy, reverse
from django.http import Http404
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Sum
from merchant.forms import MerchantDailyRecordForm
from merchant.models import MerchantDailyRecord, MerchantSalesRecords, Merchant


class DashboardView(TemplateView):
    template_name = 'merchant/dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('merchant:records_view'))
        return super(
            DashboardView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        daily_records=MerchantDailyRecord.objects.filter(
            merchant=self.request.user.user_merchant.merchant
        ).latest('id')
        sales = MerchantSalesRecords.objects.filter(
            merchant_daily_record__merchant=self.request.user.user_merchant.merchant
        )
        purchased_price = sales.aggregate(Sum('purchased_price'))
        purchased_price = purchased_price.get('purchased_price__sum')
        purchased_quantity=sales.aggregate(Sum('purchased_quantity'))
        purchased_quantity=purchased_quantity.get('purchased_quantity__sum') or 0
        remaining_quantity=float(daily_records.item_quantity) - float(purchased_quantity)
        context.update({
            'purchased_price': purchased_price,
            'purchased_quantity':purchased_quantity,
            'daily_records':daily_records,
            'remaining_quantity':remaining_quantity
        })
        return context

class DailyRecordsView(ListView):
    model = MerchantDailyRecord
    template_name = 'merchant/daily_records.html'
    paginate_by = 100
    is_paginated = True
    ordering = '-id'

class SalesRecordsView(ListView):
    model = MerchantSalesRecords
    template_name = 'merchant/sales_record.html'
    paginate_by = 3
    is_paginated = True
    ordering = '-id'


class CreateDailyRecordView(FormView):
    model = MerchantDailyRecord
    form_class = MerchantDailyRecordForm
    template_name = 'merchant/create_daily_records.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return HttpResponseRedirect(reverse('merchant:records_view'))

    def form_invalid(self, form):
        return super(CreateDailyRecordView, self).form_invalid(form)


class UpdateDailyRecordView(UpdateView):
    form_class = MerchantDailyRecordForm
    template_name = 'merchant/update_daily_records.html'
    model = MerchantDailyRecord
    success_url = reverse_lazy('merchant:records_view')
