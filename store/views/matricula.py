# store/views/matricula.py
from rest_framework import viewsets, permissions

from store.models import Matricula
from store.serializers import MatriculaSerializer
from store.pagination import StandardPagination
from store.permissions import EsAdminDjango
from store.filters import MatriculaFilter

class MatriculaViewSet(viewsets.ModelViewSet):
    serializer_class   = MatriculaSerializer
    pagination_class   = StandardPagination
    filterset_class = MatriculaFilter
    permission_classes = [permissions.IsAuthenticated]
    http_method_names  = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        user = self.request.user
        if user.rol == 'admin':
            return Matricula.objects.select_related('usuario', 'curso').all()
        return Matricula.objects.select_related('usuario', 'curso').filter(usuario=user)

    def get_permissions(self):
        if self.action == 'destroy':
            return [EsAdminDjango()]
        return super().get_permissions()