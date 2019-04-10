from django.shortcuts import render

from django.views.generic import ListView, CreateView, TemplateView,UpdateView
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
        merchant = (
            self.request.user.user_merchant.merchant.merchant_record.all()
        )

        sales = MerchantSalesRecords.objects.filter(
            merchant_daily_record__merchant=self.request.user.user_merchant.merchant
        )
        print(sales)
        print('-----coming here----')
        print('-----coming here----')
        print('-----coming here----')
        sales_sum = sales.aggregate(
            total_quantity=Sum('purchased_quantity'),
            total_price=Sum('purchased_price')
        )
        context.update({
            'merchant': merchant,
            'sales_sum': (
                int(sales_sum.get('total_quantity')) if
                sales_sum.get('total_quantity') else 0,
                int(sales_sum.get('total_price')) if
                sales_sum.get('total_price') else 0)
        })
        return context

class DailyRecordsView(ListView):
    model = MerchantDailyRecord
    template_name = 'merchant/daily_records.html'
    paginate_by = 150
    is_paginated = True

class SalesRecordsView(ListView):
    model = MerchantSalesRecords
    template_name = 'merchant/sales_record.html'
    paginate_by = 150
    is_paginated = True


class CreateDailyRecordView(CreateView):
    model = MerchantDailyRecord
    form_class = MerchantDailyRecordForm
    template_name = 'merchant/create_daily_records.html'
    success_url = reverse_lazy('records_view')

class UpdateDailyRecordView(UpdateView):
    form_class = MerchantDailyRecordForm
    template_name = 'merchant/update_daily_records.html'
    model = MerchantDailyRecord
    success_url = reverse_lazy('merchant:records_view')
