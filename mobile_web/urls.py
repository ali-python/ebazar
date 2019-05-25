from django.urls import path

from .views.common_views import (MobileHomePageView,MobileRegisterView, MobileLoginView,
                                 MobileUserInfo, MobileMerchantCreateDailyRecordView,
                                 MobileMerchantDashboardView, MobileMerchantDailyRecordsView,
                                 MobileMerchantSalesRecordsView, MobileMerchantUpdateDailyRecordView,
                                 MobilerOrderItemView, MobileClientInvoice, MobileMerchantDailyRecordDetailView,
                                 MobileInvoiceHistoery,
                                 )


urlpatterns = [
    path('', MobileHomePageView.as_view(), name='home'),
    path('register/', MobileRegisterView.as_view(), name='register'),
    path('login/', MobileLoginView.as_view(), name='login'),
    path('user/<int:pk>/', MobileUserInfo.as_view(), name='user_info'),
    path('merchant/dashboard/view/', MobileMerchantDashboardView.as_view(), name='merchant_dashboard'),
    path('merchant/create/<int:pk>/daily/record/', MobileMerchantCreateDailyRecordView.as_view(), name='merchant_create_record'),
    path('merchant/daily/record/view/', MobileMerchantDailyRecordsView.as_view(), name='merchant_daily_record'),
    path('merchant/sales/record/view/', MobileMerchantSalesRecordsView.as_view(), name='merchant_sales_record'),
    path('merchant/update/<int:pk>/view/', MobileMerchantUpdateDailyRecordView.as_view(), name='merchant_update_record'),
    path('merchant/record/<int:pk>/detail/', MobileMerchantDailyRecordDetailView.as_view(),name='merchant_record_detail'),
    path('client/order/<int:pk>/item/view/', MobilerOrderItemView.as_view(),name='client_order_item'),
    path('client/order/<int:pk>/invoice/view/', MobileClientInvoice.as_view(),name='client_order_invoice'),
    path('client/invoice/<int:pk>/invoice/history/', MobileInvoiceHistoery.as_view(),name='client_invoice_history'),
]
