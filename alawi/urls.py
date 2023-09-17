from django.urls import path
from .views import Alowance, CardPayment, FundWallet, User_Allowance
from .extra_calls import totalAlawi


urlpatterns=[
    path('alawi/', Alowance.as_view()),
    path('alawi/<str:product_id>', Alowance.as_view()),
    path('alawi/user-alawi/<str:user_id>', User_Allowance.as_view()),
    path('alawi/card-payment', CardPayment.as_view()),
    path('alawi/fund-wallet', FundWallet.as_view()),
    path('alawi-total/<str:user_id>', totalAlawi, name='totalAlawi')
]