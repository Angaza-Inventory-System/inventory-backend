from rest_framework import status, viewsets
from rest_framework.response import Response
from backend.users.decorators import permission_required

class PermissionRequiredViewSet(viewsets.ModelViewSet):
    permission_required_map = {}

    def dispatch(self, request, *args, **kwargs):
        action = self.kwargs.get('action', None)
        if action in self.permission_required_map:
            decorator = permission_required(self.permission_required_map[action])
            view_func = getattr(self, action)
            decorated_view_func = decorator(view_func)
            response = decorated_view_func(request, *args, **kwargs)
            if isinstance(response, Response) and response.status_code == status.HTTP_403_FORBIDDEN:
                return response
        return super().dispatch(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        self.perform_destroy(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
