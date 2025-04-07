# notifreception/urls.py
from django.urls import path
from .views import NotificacionListCreate

urlpatterns = [
    path('notificaciones/', NotificacionListCreate.as_view(), name='notificacion-list-create'),
]
