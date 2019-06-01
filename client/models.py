from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from common.models import Country, City
from merchant.models import MerchantDailyRecord
from django.db.models.signals import post_save
import random


class Order(models.Model):
    STATE_TYPE_PENDING = 'Pending'
    STATE_TYPE_AWAITING_PAYMENT = 'Awaiting_Payment'
    STATE_TYPE_CANCELLED = 'Cancelled'
    STATE_TYPE_AWAITING_FULLFILLMENT = 'Awaiting_Fullfillment'
    STATE_TYPE_REFUNDED = 'Refunded'
    STATE_TYPE_COMPLETED = 'Completed'

    STATE_TYPES = (
        (STATE_TYPE_PENDING, 'Pending'),
        (STATE_TYPE_AWAITING_PAYMENT, 'Awaiting_Payment'),
        (STATE_TYPE_CANCELLED, 'Cancelled'),
        (STATE_TYPE_AWAITING_FULLFILLMENT, 'Awaiting_Fullfillment'),
        (STATE_TYPE_REFUNDED, 'Refunded'),
        (STATE_TYPE_COMPLETED, 'Completed'),
    )

    state = models.CharField(
        max_length=200, choices=STATE_TYPES, default=STATE_TYPE_PENDING,
        blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='user_order', null=True, blank=True)
    customer_name=models.CharField(max_length=200, null=True, blank=True)
    customer_phone=models.CharField(max_length=100, null=True, blank=True)
    alternate_phone=models.CharField(max_length=100, null=True, blank=True)
    city=models.ForeignKey(City, on_delete=models.CASCADE,
                            related_name='order_city',null=True, blank=True
                            )
    date_created=models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.customer_name if self.customer_name else ''

class OrderItem(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE,
                            related_name='customer_order',null=True, blank=True
                            )
    merchant_daily_upload=models.ForeignKey(MerchantDailyRecord,
                                            on_delete=models.CASCADE,
                                            related_name='merchant_daily_record',
                                            null=True, blank=True
                                            )
    item_quantity=models.IntegerField(default=0, null=True, blank=True)
    item_price=models.IntegerField(default=0, null=True, blank=True)
    date_added=models.DateTimeField(auto_now=True, null=True, blank=True)
    #
    # def __str__(self):
    #     return self.order.customer_name if self.order.customer_name else ''

class Invoice(models.Model):
    STATE_TYPE_PENDING = 'Pending'
    STATE_TYPE_CANCELLED = 'Cancelled'
    STATE_TYPE_PAID = 'Paid'
    STATE_TYPE_CONFIRMED = 'Confirmed'
    STATE_TYPE_RECEIVED = 'Received'


    # Confirmed
    # Received

    # support_status boolean field default False
    # transport_status boolean field default False
    # cash_on_delivery boolean field default True
    support_status=models.BooleanField(default=False)
    transport_status=models.BooleanField(default=False)
    cash_on_delivery=models.BooleanField(default=True)
    STATE_TYPES = (
        (STATE_TYPE_PENDING, 'Pending'),
        (STATE_TYPE_CANCELLED, 'Cancelled'),
        (STATE_TYPE_PAID, 'Paid'),
    )

    receipt_no = models.CharField(
        max_length=20, unique=True, blank=True, null=True
    )
    state = models.CharField(
        max_length=200, choices=STATE_TYPES, default=STATE_TYPE_PENDING,
        blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='invoice_order'
                              )
    amount=models.IntegerField(default=0, null=True, blank=True)
    is_payment=models.BooleanField(default=True)


    def __str__(self):
        return self.order.customer_name if self.order.customer_name else ''

class Payment(models.Model):
    STATE_TYPE_ACCEPTED = 'Accepted'
    STATE_TYPE_ERROR = 'Error'
    STATE_TYPE_DECLINED = 'Declined'
    STATE_TYPE_REJECTED = 'rejected'

    STATE_TYPES = (
        (STATE_TYPE_ACCEPTED ,'Accepted'),
        (STATE_TYPE_ERROR , 'Error'),
        (STATE_TYPE_DECLINED , 'Declined'),
        (STATE_TYPE_REJECTED , 'rejected')
         )
    state = models.CharField(
        max_length=200, choices=STATE_TYPES, default=STATE_TYPE_ACCEPTED,
        blank=True, null=True)
    invoice=models.ForeignKey(Invoice, on_delete=models.CASCADE,
                              related_name="invoice")
    amount=models.IntegerField(default=0, null=True, blank=True)
    date_created=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.invoice.order.customer_name if self.invoice.order.customer_name else ''


# Signals Function
def create_save_receipt_no(sender, instance, created, **kwargs):
    if created and not instance.receipt_no:
        while True:
            random_code = random.randint(1000000, 9999999)
            if (
                not Invoice.objects.filter(
                    receipt_no=random_code).exists()
            ):
                break

        instance.receipt_no = random_code
        instance.save()


# Signal Calls
post_save.connect(create_save_receipt_no, sender=Invoice)