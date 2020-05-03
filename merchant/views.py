from django.shortcuts import render
from django.views.generic import ListView, CreateView, TemplateView,UpdateView, FormView, View
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

    # def get_context_data(self, **kwargs):
    #     context = super(DashboardView, self).get_context_data(**kwargs)
    #     daily_records=MerchantDailyRecord.objects.get(
    #         merchant=self.request.user.user_merchant.merchant
    #     )
    #     print(daily_records)
    #     print("________________________________________________")
    #     sales = MerchantSalesRecords.objects.filter(
    #         merchant_daily_record__merchant=self.request.user.user_merchant.merchant
    #     )
    #     print(sales)
    #     context.update({
    #         'records': daily_records,
    #         'sales': sales
    #     })
    #     return context

# class DailyRecordsView(ListView):
#     model = MerchantDailyRecord
#     template_name = 'merchant/daily_records.html'
#     paginate_by = 100
#     is_paginated = True

#     def get_queryset(self):
#         queryset = self.queryset
#         if not queryset:
#             queryset = MerchantDailyRecord.objects.get(
#                 merchant=self.kwargs.get('pk'))

#         return queryset
class DailyRecordsView(ListView):
    template_name = 'merchant/daily_records.html'
    paginate_by = 200
    model = MerchantDailyRecord

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        return super(
            DailyRecordsView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset
        if not queryset:
            queryset = MerchantDailyRecord.objects.filter(
                merchant__id=self.kwargs.get('pk'))

        return queryset.order_by('-id')

# class SalesRecordsView(ListView):
#     model = MerchantSalesRecords
#     template_name = 'merchant/sales_record.html'
#     paginate_by = 3
#     is_paginated = True
#     ordering = '-id'

class SalesRecordsView(ListView):
    template_name = 'merchant/sales_record.html'
    paginate_by = 200
    model = MerchantSalesRecords

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        return super(
            SalesRecordsView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset
        if not queryset:
            queryset = MerchantSalesRecords.objects.filter(
                merchant_daily_record__merchant__id=self.kwargs.get('pk'))

        return queryset.order_by('-id')

class CreateDailyRecordView(FormView):
    model = MerchantDailyRecord
    form_class = MerchantDailyRecordForm
    template_name = 'merchant/create_daily_records.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return HttpResponseRedirect(reverse('merchant:dashboard'))

    def form_invalid(self, form):
        return super(CreateDailyRecordView, self).form_invalid(form)


class UpdateDailyRecordView(UpdateView):
    form_class = MerchantDailyRecordForm
    template_name = 'merchant/update_daily_records.html'
    model = MerchantDailyRecord
    success_url = reverse_lazy('merchant:records_view')


class MerchantInvoiceAPIView(View):
    def post(self, request, *args, **kwargs):
        merArr =[]
        merchant = MerchantSalesRecords.objects.filter(
            merchant_daily_record__merchant__id=self.request.POST.get('merchant_id'))
        for r in merchant:
            merArr.append(r)

        return JsonResponse({
            'merchant': merArr,
        })

