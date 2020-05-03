from django.urls import path

from .views import DailyRecordsView, CreateDailyRecordView,DashboardView,SalesRecordsView,UpdateDailyRecordView, MerchantInvoiceAPIView

urlpatterns = [
    path('records/view/<int:pk>/', DailyRecordsView.as_view(), name='records_view'),
    path('sales/records/view/<int:pk>/', SalesRecordsView.as_view(), name='sales_records_view'),
    path('create/<int:pk>/', CreateDailyRecordView.as_view(), name='create_record'),
    path('update/<int:pk>/', UpdateDailyRecordView.as_view(), name='update_record'),
    path('dashboard/view', DashboardView.as_view(), name='dashboard'),
    path('invoice/view/api', MerchantInvoiceAPIView.as_view(), name='invoice_api'),

]