# notifreception/urls.py
from django.urls import path
from .views import EchoDataView,SingleAttribute,SpendingListView, LiquidationListView

urlpatterns = [
        path('echo/', EchoDataView.as_view(), name='echo'),
        path('sendmail/', SingleAttribute.as_view(), name='sendmail'),  # New endpoint
        path('spendings/', SpendingListView.as_view(), name='spending-list'),
        path('liquidity/', LiquidationListView.as_view(), name='liquidity-list'),

]
