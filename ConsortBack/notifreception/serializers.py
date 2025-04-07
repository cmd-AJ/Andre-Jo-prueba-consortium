from rest_framework import serializers
from .models import Notificacion

class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = ['fecha_recepcion', 'hora_recepcion', 'entidad', 'numero_expediente', 
                  'dirigido_a', 'recepcionista', 'usuario_asignado', 'hora_entrega']