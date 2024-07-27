from rest_framework import filters, viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from backend.authen.permissions import IsNotBlacklisted, IsSuperUser
from backend.devices.pagination import CustomPagination
from backend.users.decorators import permission_required

from .models import User
from .serializers import UserSerializer, UserPermissionsSerializer

@permission_classes([AllowAny])
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@permission_classes([IsNotBlacklisted])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        "username": ["exact", "icontains"],
        "email": ["exact", "icontains"],
        "first_name": ["icontains"],
        "last_name": ["icontains"],
        "role": ["exact"]
    }
    ordering_fields = ["username", "email", "first_name", "last_name"]
    ordering = ["username"]

    @action(detail=False, methods=['get'])
    @permission_required(['readUsers'])
    def custom_list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['post'])
    @permission_required(['createUsers'])
    def custom_create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['put', 'patch'])
    @permission_required(['editUsers'])
    def custom_update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            return Response(self.get_serializer(instance).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    @permission_required(['deleteUsers'])
    def custom_destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        self.perform_destroy(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

@permission_classes([IsNotBlacklisted])
class UpdateUserPermissionsView(viewsets.GenericViewSet, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserPermissionsSerializer
    lookup_field = 'username'

    @action(detail=True, methods=['patch'])
    @permission_required(['editUserPermissions'])
    def update_permissions(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    @permission_required(['readUserPermissions'])
    def retrieve_permissions(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
