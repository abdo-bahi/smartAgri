from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import MCUViewSet


from .views import SensorDataViewSet, ActionViewSet

router = DefaultRouter()
router.register('sensordata', SensorDataViewSet)
router.register('actions', ActionViewSet)
router.register('mcu',MCUViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api/sensordata/<int:pk>/', SensorDataViewSet.as_view({'put': 'update'}), name='sensor-data-detail'),

]