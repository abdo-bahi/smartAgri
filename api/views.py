# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from .models import SensorData, Action, MCU
from .serializers import SensorDataSerializer, ActionSerializer, MCUSerializer
# from .views import MCUViewSet

class MCUViewSet(viewsets.ModelViewSet):
    queryset = MCU.objects.all()
    serializer_class = MCUSerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['id']
    def update(self, request, pk=None):
        # Get the object instance based on the primary key (pk)
        sensor_data = self.get_object()

        # Update the model instance with data from the request body
        serializer = self.get_serializer(sensor_data, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Return a serialized response with the updated data
        return Response(serializer.data, status=HTTP_200_OK)
    # Permission check: Only authenticated users can access MCU data
    # permission_classes = [IsAuthenticated]

class SensorDataViewSet(viewsets.ModelViewSet):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['mcuId']
    # Permission check: Only authenticated users can access sensor data
    # permission_classes = [IsAuthenticated]

class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer

    # Permission check: Only authenticated users can perform actions
    # permission_classes = [IsAuthenticated]

