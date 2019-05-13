from django.contrib import admin
from .models import Merchant, MerchantDailyRecord, MerchantSalesRecords, MerchantUser


class MerchantAdmin(admin.ModelAdmin):
    list_display = (
         'name', 'phone', 'city', 'address',
        'status'
    )

    search_fields = (
        'name', 'phone',
    )

class MerchantUserAdmin(admin.ModelAdmin):
    list_display = (
         'name', 'user',
    )

    @staticmethod
    def name(obj):
        return obj.merchant.name

    search_fields = (
        'merchant__name',
    )

    @staticmethod
    def merchant(obj):
        return obj.merchant.name

class MerchantDailyRecordAdmin(admin.ModelAdmin):
    list_display = (
        'merchant', 'upload_time','image_1','image_2','image_3',
        'image_4','video','item_quantity', 'item_price' , 'expiry','mid'
    )

    @staticmethod
    def name(obj):
        return obj.merchant.name

    search_fields = (
        'merchant__name', 'mid',
    )

class MerchantSalesRecordAdmin(admin.ModelAdmin):
    list_display = (
     'merchant_daily_record', 'added_date','purchased_quantity','purchased_price'
    )

    @staticmethod
    def name(obj):
        return obj.merchant_daily_record.merchant

    search_fields = (
        'merchant_daily_record__merchant__name',
    )


admin.site.register( Merchant,MerchantAdmin)
admin.site.register(MerchantSalesRecords, MerchantSalesRecordAdmin)
admin.site.register( MerchantDailyRecord, MerchantDailyRecordAdmin)
admin.site.register( MerchantUser, MerchantUserAdmin,)
