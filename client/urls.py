from django.urls import path
from .views import (ListMerchantDailyRecordView, MerchantDailyRecordDetailView
                    ,OrderItemView,ClientInvoice,InvoiceHistoery, ConfirmClientInvoiceAPIView)
urlpatterns = [
    path('records/list/view/<int:pk>/', ListMerchantDailyRecordView.as_view(),
         name='list_records_view'
         ),
    path('record/<int:pk>/detail/', MerchantDailyRecordDetailView.as_view(),
         name='record_detail'),

    path('order/<int:pk>/item/view/', OrderItemView.as_view(),
         name='client_order_item'),

    path('order/<int:pk>/invoice/view/', ClientInvoice.as_view(),
         name='client_order_invoice'),

    path('invoice/<int:pk>/invoice/history/', InvoiceHistoery.as_view(),
         name='invoice_history'),
    path('invoice/state/confirmed/', ConfirmClientInvoiceAPIView.as_view(),
         name='invoice_state_confirmed'
         ),

]