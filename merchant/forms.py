from django import forms

from merchant.models import MerchantDailyRecord


class MerchantDailyRecordForm(forms.ModelForm):
    class Meta:
        model = MerchantDailyRecord
        fields = '__all__'
