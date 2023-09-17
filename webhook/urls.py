from django.urls import path
from .views import WebhookHandler


urlpatterns= [
    path('payment/', WebhookHandler.as_view())
]