# notifreception/urls.py
from django.urls import path
from .views import EchoDataView,SingleAttribute,SpendingListView, LiquidationListView, UserListView, NotificationListView

urlpatterns = [
        path('send_notif/', EchoDataView.as_view(), name='send_notif'),
        path('sendmail/', SingleAttribute.as_view(), name='sendmail'),  # New endpoint
        path('spendings/', SpendingListView.as_view(), name='spending-list'),
        path('liquidity/', LiquidationListView.as_view(), name='liquidity-list'),
        path('users/', UserListView.as_view(), name='usuarios'),
        path('getnotification/', NotificationListView.as_view(), name='notif_list'),


]
