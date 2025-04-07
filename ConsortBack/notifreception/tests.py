from django.test import TestCase
from django.contrib.auth.models import User
from .models import Notificacion
from datetime import date, time
from rest_framework.renderers import JSONRenderer
from rest_framework import serializers

# Serializer para convertir el modelo a JSON
class NotificacionSerializer(serializers.ModelSerializer):
    recepcionista = serializers.StringRelatedField()
    colaborador = serializers.StringRelatedField()

    class Meta:
        model = Notificacion
        fields = '__all__'

class NotificacionTestCase(TestCase):


    def test_crear_notificacion(self):
        notificacion = Notificacion.objects.create(
        fecha_recepcion=date.today(),
        hora_recepcion=time(9, 30),
        entidad_emite='Juzgado Civil',
        numero_cedula_expediente='EXP-000123',
        dirigido_a='Lic. Mario López',
        recepcionista="amanda",  # Asignar el usuario recepcionista
        colaborador_nombre="juan",     # Asignar el colaborador
        fecha_entrega=date.today(),
        hora_entrega=time(10, 0)
        )

        serializer = NotificacionSerializer(notificacion)
        json_data = JSONRenderer().render(serializer.data)
        print(json_data.decode('utf-8'))  # Mostrar el JSON de la notificación

        self.assertEqual(notificacion.entidad_emite, 'Juzgado Civil')
        self.assertEqual(notificacion.recepcionista, 'amanda')
        self.assertEqual(notificacion.colaborador_nombre, 'juan')
