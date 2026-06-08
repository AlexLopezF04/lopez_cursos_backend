# store/views/progreso.py
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from store.models import Matricula, Progreso
from store.serializers import ProgresoSerializer


class ProgresoViewSet(viewsets.ModelViewSet):
    serializer_class   = ProgresoSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names  = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        user = self.request.user
        qs = Progreso.objects.select_related('matricula', 'leccion')
        if user.rol == 'admin':
            return qs.all()
        return qs.filter(matricula__usuario=user)

    def perform_create(self, serializer):
        matricula_id = serializer.validated_data.get('matricula').id
        try:
            matricula = Matricula.objects.get(id=matricula_id)
        except Matricula.DoesNotExist:
            raise PermissionDenied('Matrícula no encontrada.')
        user = self.request.user
        if user.rol != 'admin' and matricula.usuario != user:
            raise PermissionDenied('No puedes registrar progreso en esta matrícula.')
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        if user.rol != 'admin' and instance.matricula.usuario != user:
            raise PermissionDenied('No puedes eliminar este progreso.')
        instance.delete()