from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Notificacion
from .serializers import NotificacionSerializer

class NotificacionListCreate(APIView):
    def get(self, request):
        notificaciones = Notificacion.objects.all()
        serializer = NotificacionSerializer(notificaciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = NotificacionSerializer(data=request.data)  # Validate the input data
        if serializer.is_valid():
            notificacion = serializer.save()  # Save the notificacion
            notificacion.enviar_correo()  # Send the email
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return success
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return error if invalid data
