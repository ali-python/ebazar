from django.urls import path

from .views import DailyRecordsView, CreateDailyRecordView,DashboardView,SalesRecordsView,UpdateDailyRecordView

urlpatterns = [
    path('records/view/', DailyRecordsView.as_view(), name='records_view'),
    path('sales/records/view/', SalesRecordsView.as_view(), name='sales_records_view'),
    path('create/(?P<pk>\d+)/', CreateDailyRecordView.as_view(), name='create_record'),
    path('update/(?P<pk>\d+)/', UpdateDailyRecordView.as_view(), name='update_record'),
    path('dashboard/view', DashboardView.as_view(), name='dashboard'),
]