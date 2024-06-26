from rest_framework import generics
from .models import Device
from .serializers import DeviceSerializer

class DeviceListCreate(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class DeviceRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer