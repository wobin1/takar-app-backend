from django.urls import path
from .views import UserList, UserCreate, UserUpdate, UserDelete, UserVerify


urlpatterns=[
    path('list', UserList.as_view()),
    path('create/', UserCreate.as_view()),
    path('update/<int:id>', UserUpdate.as_view()),
    path('delete/<int:id>', UserDelete.as_view()),
    path('verify/<str:token>', UserVerify.as_view())
]