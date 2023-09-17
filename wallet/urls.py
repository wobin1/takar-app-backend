from django.urls import path
from .views import TransferView, Wallets, GetUserWallet



urlpatterns = [
    path("wallets/", Wallets.as_view()),
    path("transfer/", TransferView.as_view()),
    path("wallet/<str:user_id>", GetUserWallet.as_view())
]