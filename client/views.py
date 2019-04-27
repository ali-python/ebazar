from django.shortcuts import render
from django.views.generic import ListView, CreateView, TemplateView,UpdateView, FormView
from .models import Order,OrderItem,Invoice,Payment
from .forms import OrderForm, OrderItemForm
from merchant.models import MerchantDailyRecord
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse, HttpResponseRedirect
from common.models import UserProfile

class ListMerchantDailyRecordView(ListView):
    model = MerchantDailyRecord
    template_name = 'client/merchant_daily_records.html'
    paginate_by = 150
    is_paginated = True

class MerchantDailyRecordDetailView(TemplateView):
    template_name = 'client/record_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('client:list_records_view'))
        return super(
            MerchantDailyRecordDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MerchantDailyRecordDetailView, self).get_context_data(**kwargs)
        merchant = MerchantDailyRecord.objects.get(id=self.kwargs.get('pk'))

        context.update({
            'merchant': merchant
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
        obj = form.save(commit=False)
        obj.order = Order.objects.create(
            customer_name=self.request.POST.get('customer_name'),
            customer_phone=self.request.POST.get('customer_phone'),
            user=self.request.user,
        )
        invoice=Invoice.objects.create(
            order=obj.order,
            amount=obj.item_price
        )
        invoice.save()
        self.request.user.user_profile.phone=self.request.POST.get('customer_phone')
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
            'merchant_record':merchant_record
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
            'total_price': total_price
            # 'order':order

        })
        return context

class InvoiceHistoery(ListView):
    model = Order
    template_name = 'client/invoice_list.html'
    paginate_by = 150
    is_paginated = True