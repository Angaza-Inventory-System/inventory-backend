from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import permission_classes


from backend.authen.permissions import IsNotBlacklisted, IsSuperUser
from backend.devices.pagination import CustomPagination
from backend.users.decorators import permission_required


from .models import User
from .serializers import UserPermissionsSerializer, UserSerializer


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
        "role": ["exact"],
    }
    ordering_fields = ["username", "email", "first_name", "last_name"]
    ordering = ["username"]

    @permission_required('readUsers')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @permission_required('createUsers')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @permission_required('editUsers')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @permission_required('editUsers')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @permission_required('deleteUsers')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class UpdateUserPermissionsView(viewsets.GenericViewSet, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserPermissionsSerializer
    lookup_field = "username"

    @permission_required('editUsers')
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    @permission_required('editUsers')
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @permission_required('readUsers')
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
