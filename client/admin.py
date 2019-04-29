from django.contrib import admin
from .models import Order, OrderItem, Invoice, Payment


class OrderAdmin(admin.ModelAdmin):
    list_display = (
         '__str__','user', 'state', 'customer_name', 'customer_phone',
        'date_created'
    )

    search_fields = (
        'customer_name', 'customer_phone',
    )

class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
         '__str__','order', 'merchant_daily_upload', 'item_quantity', 'item_price',
        'date_added'
    )

    search_fields = (
        'order__customer_name', 'order__customer_phone',
    )

class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
         '__str__', 'receipt_no', 'order', 'state', 'amount', 'is_payment',
    )

    search_fields = (
        'order__customer_name', 'receipt_no', 'order__customer_phone',
    )

class PaymentAdmin(admin.ModelAdmin):
    list_display = (
         '__str__','state', 'invoice', 'amount', 'date_created',
    )

    search_fields = (
        'invoice__order__customer_name', 'invoice__order__customer_phone',
    )

admin.site.register( Order,OrderAdmin)
admin.site.register( OrderItem,OrderItemAdmin)
admin.site.register( Invoice,InvoiceAdmin)
admin.site.register( Payment,PaymentAdmin)
