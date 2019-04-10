from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Merchant(models.Model):
    name = models.CharField(max_length=256, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class MerchantUser(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE,
                                 related_name='merchant_profile',
                                 blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='user_merchant')

    def __unicode__(self):
        return self.merchant.name

class MerchantDailyRecord(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='merchant_record',
                               blank=True, null=True)
    upload_time = models.DateTimeField(auto_now=True, null=True, blank=True)
    image_1 = models.ImageField(upload_to="gallery", null=True, blank=True)
    image_2 = models.ImageField(upload_to="gallery", null=True, blank=True)
    image_3 = models.ImageField(upload_to="gallery", null=True, blank=True)
    image_4 = models.ImageField(upload_to="gallery", null=True, blank=True)
    video = models.FileField(upload_to="gallery", null=True, blank=True)
    item_quantity = models.CharField(max_length=200, null=True, blank=True)
    item_price = models.CharField(max_length=200, null=True, blank=True)
    expiry = models.BooleanField(default=True)

    def __unicode__(self):
        return self.merchant.name


class MerchantSalesRecords(models.Model):
    merchant_daily_record = models.ForeignKey(
        MerchantDailyRecord,
        related_name='merchant_sales',
        blank=True, null=True, on_delete=models.CASCADE
    )
    added_date = models.DateTimeField(auto_now=True ,null=True, blank=True)
    purchased_quantity = models.DecimalField(
        max_digits=65, decimal_places=2, default=0,
        blank=True, null=True,
    )
    purchased_price = models.DecimalField (
        max_digits=65, decimal_places=2, default=0,
        blank=True, null=True,
    )

    def __unicode__(self):
        return self.merchant_daily_record.merchant.name
