from django.db import models
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings

# Modelo para la notificación
class Notificacion(models.Model):
    fecha_recepcion = models.DateField(default=timezone.now)
    hora_recepcion = models.TimeField(default=timezone.now)
    entidad_emite = models.CharField(max_length=255)
    numero_cedula_expediente = models.CharField(max_length=255)
    dirigido_a = models.CharField(max_length=255)
    recepcionista = models.CharField(max_length=255, choices=[('Amanda González', 'Amanda González'), ('Wanda Pastor', 'Wanda Pastor')])
    colaborador_nombre = models.CharField(max_length=255, blank=True, null=True)  # Storing collab
    hora_entrega = models.TimeField(null=True, blank=True)
    fecha_entrega = models.DateField(null=True, blank=True)
    

