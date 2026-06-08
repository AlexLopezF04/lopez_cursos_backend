# store/views/leccion.py
from rest_framework import viewsets, permissions

from store.models import Leccion, Curso
from store.serializers import LeccionSerializer
from store.permissions import EsInstructor, EsPropietarioOAdmin


class LeccionViewSet(viewsets.ModelViewSet):
    serializer_class   = LeccionSerializer
    pagination_class   = None
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Leccion.objects.filter(
            curso__id=self.kwargs['curso_pk']
        ).order_by('orden')

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), EsInstructor()]

    def perform_create(self, serializer):
        curso = Curso.objects.get(pk=self.kwargs['curso_pk'])
        serializer.save(curso=curso)