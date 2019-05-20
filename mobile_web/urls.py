from django.urls import path

from .views.common_views import (MobileHomePageView,MobileRegisterView, MobileLoginView,
                                 MobileUserInfo, MobileMerchantCreateDailyRecordView,
                                 MobileMerchantDashboardView, MobileMerchantDailyRecordsView,
                                 MobileMerchantSalesRecordsView, MobileMerchantUpdateDailyRecordView
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

]
