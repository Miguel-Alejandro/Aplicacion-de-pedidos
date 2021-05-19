from django.urls import path
from .views import hoyRxList

urlpatterns = [
    path('hoyRx/', hoyRxList.as_view(), name='hoyRx_List')
]
