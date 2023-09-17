from django.urls import path
from .views import TransactionHistory, UserTransaction, orderTransaction, ChartData, TransactionDetail



urlpatterns=[
    path('transaction-history/', TransactionHistory.as_view()),
    path('transaction/<str:transaction_id>', TransactionDetail.as_view()),
    path('transaction-history/<str:user_id>', UserTransaction.as_view()),
    path('limited-history/<str:user_id>', orderTransaction.as_view()),
    path('chart-data/<str:user_id>', ChartData.as_view())
]