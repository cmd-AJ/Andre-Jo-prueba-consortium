# notifreception/urls.py
from django.urls import path
from .views import EchoDataView,SingleAttribute

urlpatterns = [
        path('echo/', EchoDataView.as_view(), name='echo'),
        path('echos/', SingleAttribute.as_view(), name='echos'),  # New endpoint

]
