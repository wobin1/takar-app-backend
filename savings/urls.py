from django.urls import path
from .views import SavingsProduct, SavingsDetail
from .extra_calls import totalSavings, savingsPercentage


urlpatterns=[
    path('savings/', SavingsProduct.as_view()),
    path('savings/<str:user_id>', SavingsProduct.as_view()),
    path('savings/detail/<str:savings_id>', SavingsDetail.as_view()),
    path('savings-total/<str:user_id>', totalSavings, name='totalSavings'),
    path('savings-percentage/<str:user_id>', savingsPercentage, name='savingsPercentage')
]