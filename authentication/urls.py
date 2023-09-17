from django.urls import path
from .views import Login, Logout, ForgetPassword, ResetPassword, PasswordRecoveryVerify

urlpatterns=[
    path("login/", Login.as_view()),
    path("logout/", Logout.as_view()),
    path("forget-password/", ForgetPassword.as_view()),
    path("reset-password/<str:id>", ResetPassword.as_view()),
    path("verify-password-recovery/<str:token>", PasswordRecoveryVerify.as_view())
]

