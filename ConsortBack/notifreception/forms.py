from django import forms
from .models import Notificacion

class NotificacionForm(forms.ModelForm):
    class Meta:
        model = Notificacion
        fields = ['fecha_recepcion', 'hora_recepcion', 'entidad_emite', 'numero_cedula_expediente', 'dirigido_a', 'recepcionista', 'colaborador', 'hora_entrega', 'fecha_entrega']
