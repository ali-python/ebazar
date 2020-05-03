from django.shortcuts import render
from django.views.generic import ListView, CreateView, TemplateView,UpdateView, FormView, View
from .models import Order,OrderItem,Invoice,Payment
from .forms import OrderForm, OrderItemForm
from merchant.models import MerchantDailyRecord, MerchantSalesRecords, Merchant
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse, HttpResponseRedirect
from common.models import UserProfile, City
from django.db import transaction
from django.db.models import Sum


class ListMerchantDailyRecordView(ListView):
    model = MerchantDailyRecord
    template_name = 'client/merchant_daily_records.html'
    paginate_by = 20
    is_paginated = True

    def get_queryset(self):
        queryset = self.queryset

        if not queryset:
            queryset = MerchantDailyRecord.objects.all().order_by('-id')
        if self.request.GET.get('item_name'):
            queryset = MerchantDailyRecord.objects.filter(
                item_name__contains=self.request.GET.get('item_name'))


        if self.request.GET.get('category'):
            queryset = MerchantDailyRecord.objects.filter(
                item_category__contains=self.request.GET.get('category'))
        return queryset.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(
            ListMerchantDailyRecordView, self).get_context_data(**kwargs)
        merchant = Merchant.objects.get(id=self.kwargs.get('pk'))
        context.update({
            'merchant': merchant,
        })
        return context


class MerchantDailyRecordDetailView(TemplateView):
    template_name = 'client/record_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('client:list_records_view'))
        return super(
            MerchantDailyRecordDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(
            MerchantDailyRecordDetailView, self).get_context_data(**kwargs)
        merchant = MerchantDailyRecord.objects.get(id=self.kwargs.get('pk'))
        merchant_sales = MerchantSalesRecords.objects.filter(
            merchant_daily_record__merchant=merchant.merchant
        )
        purchased_quantity = merchant_sales.aggregate(Sum('purchased_quantity'))
        purchased_quantity = purchased_quantity.get('purchased_quantity__sum') or 0
        remaining_quantity = float(merchant.item_quantity) - float(purchased_quantity)
        city = City.objects.all()

        context.update({
            'merchant': merchant,
            'city':city,
            'remaining_quantity': remaining_quantity
        })
        return context


class OrderItemView(FormView):
    form_class = OrderItemForm
    template_name = 'client/order.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('client:list_records_view'))
        return super(
            OrderItemView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        with transaction.atomic():
            obj = form.save(commit=False)
            obj.order = Order.objects.create(
                customer_name=self.request.POST.get('customer_name'),
                customer_phone=self.request.POST.get('customer_phone'),
                alternate_phone=self.request.POST.get('alternate_phone'),
                customer_address=self.request.POST.get('address'),
                user=self.request.user,
            )
            t_amount= obj.item_price
            p_amount = float(t_amount) * 3 / 100
            a_t_p_amount = float(p_amount) - float(t_amount)
            print(a_t_p_amount)
            print("_________________________________")

            invoice=Invoice.objects.create(
                order=obj.order,
                amount=obj.item_price,
                percentage_amount=p_amount,
                after_per_t=a_t_p_amount
            )
            invoice.save()
            merchant_sales_record=MerchantSalesRecords.objects.create(
                merchant_daily_record=obj.merchant_daily_upload,
                purchased_quantity=obj.item_quantity,
                purchased_price=obj.item_price,
                percent_ebazarr=p_amount,
                after_per_amount=a_t_p_amount
            )
            merchant_sales_record.save()
            self.request.user.user_profile.phone=self.request.POST.get('customer_phone')
            self.request.user.user_profile.alternate_phone=self.request.POST.get('alternate_phone')
            self.request.user.user_profile.address=self.request.POST.get('address')
            self.request.user.user_profile.save()
            obj.save()
            return HttpResponseRedirect(reverse('client:client_order_invoice',  kwargs={
                            'pk': invoice.id
                        }))

    def form_invalid(self, form):
        return super(OrderItemView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(OrderItemView, self).get_context_data(**kwargs)
        merchant_record = MerchantDailyRecord.objects.get(id=self.kwargs.get('pk'))

        context.update({
            'merchant_record':merchant_record,

        })
        return context


class ClientInvoice(TemplateView):
    template_name = 'client/invoice.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('client:list_records_view'))
        return super(
            ClientInvoice, self).dispatch(request, *args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(ClientInvoice, self).get_context_data(**kwargs)
        invoice= Invoice.objects.get(id=self.kwargs.get('pk'))
        order_items = invoice.order.customer_order.all()
        item = OrderItem.objects.filter(order__id=invoice.order.id)

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


class InvoiceHistoery(ListView):
    model = Order
    template_name = 'client/invoice_list.html'
    paginate_by = 150
    is_paginated = True


class ConfirmClientInvoiceAPIView(View):

    def post(self, request, *args, **kwargs):
        invoice = Invoice.objects.get(id=self.request.POST.get('invoice_id'))
        invoice.state = Invoice.STATE_TYPE_CONFIRMED
        invoice.save()

        return JsonResponse({
            'status': True,
            'invoice_state': invoice.state
        })

